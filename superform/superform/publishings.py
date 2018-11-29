from flask import Blueprint, url_for, request, redirect, session, render_template
from superform.utils import login_required, datetime_converter, str_converter
from superform.models import db, User, Publishing, Channel, PubGCal, Comment, State
from superform.users import get_moderate_channels_for_user
from superform.posts import get_post_form_validations

pub_page = Blueprint('publishings', __name__)


@pub_page.route('/moderate', methods=["GET"])
@login_required()
def moderate():
    user = User.query.get(session.get("user_id", "")) if session.get("logged_in", False) else None
    flattened_list_pubs = []
    if user is not None:
        chans = get_moderate_channels_for_user(user)
        pubs_per_chan = (db.session.query(Publishing).filter((Publishing.channel_id == c.id) & (Publishing.state == 0))
                         for c in chans)
        flattened_list_pubs = [y for x in pubs_per_chan for y in x]
    return render_template("moderate.html", publishings=flattened_list_pubs)


@pub_page.route('/moderate/<int:id>/<string:idc>', methods=["GET", "POST"])
@login_required()
def moderate_publishing(id, idc):

    chn = db.session.query(Channel).filter(Channel.id == idc).first()
    """ FROM THIS : 
    SHOULD BE IN THE if request.method == 'GET' (BUT pub.date_from = str_converter(pub.date_from) PREVENT US)"""
    pub_versions = db.session.query(Publishing).filter(Publishing.post_id == id, Publishing.channel_id == idc). \
        order_by(Publishing.num_version.desc()).all()
    pub_comments = []
    for pub_ver in pub_versions:
        com = db.session.query(Comment).filter(Comment.publishing_id == pub_ver.publishing_id).first()
        pub_comments.insert(0, com)
    """TO THIS"""
    if chn.module == 'superform.plugins.gcal':
        pub = db.session.query(PubGCal).filter(PubGCal.post_id == id, PubGCal.channel_id == idc).first()
        pub.date_start = str_converter(pub.date_start)
        pub.date_end = str_converter(pub.date_end)
    else:
        pub = db.session.query(Publishing).filter(Publishing.post_id == id, Publishing.channel_id == idc).order_by(Publishing.num_version.desc()).first()
        pub.date_from = str_converter(pub.date_from)
        pub.date_until = str_converter(pub.date_until)
    if request.method == "GET":
        """SHOULD PREPARE THE pub_versions AND pub_comments"""
        for pub_ver in pub_versions:
            if pub_ver.publishing_id != pub.publishing_id:
                pub_ver.date_from = str_converter(pub_ver.date_from)
                pub_ver.date_until = str_converter(pub_ver  .date_until)
                #setattr(pub_ver, "date_from_str", str_converter(pub_ver.date_from))
                #setattr(pub_ver, "date_until_str", str_converter(pub_ver.date_until))

        print("pub", pub_versions)

        post_form_validations = get_post_form_validations()

        return render_template('moderate_post.html', pub=pub, channel=chn, pub_versions=pub_versions, comments=pub_comments, post_form_validations=post_form_validations)
    else:
        pub.title = request.form.get('titlepost')
        pub.description = request.form.get('descrpost')
        pub.link_url = request.form.get('linkurlpost')
        pub.image_url = request.form.get('imagepost')
        if chn.module == 'superform.plugins.gcal':
            pub.date_start = datetime_converter(request.form.get('datedebut'))
            pub.hour_start = request.form.get('heuredebut')
            pub.date_end = datetime_converter(request.form.get('datefin'))
            pub.hour_end = request.form.get('heurefin')
            pub.location = request.form.get('location')
            pub.color = request.form.get('color')
            pub.visibility = request.form.get('visibility')
            pub.availability = request.form.get('availability')
        else:
            pub.date_from = datetime_converter(request.form.get('datefrompost'))
            pub.date_until = datetime_converter(request.form.get('dateuntilpost'))
        # state is shared & validated
        """pub.state = 1
        db.session.commit()
        """
        # running the plugin here
        c = db.session.query(Channel).filter(Channel.id == pub.channel_id).first()
        plugin_name = c.module
        c_conf = c.config
        from importlib import import_module
        plugin = import_module(plugin_name)

        # every plugin should implement the autheticate method that redirect to the plugin authentication process
        # if it is required or necessary (no token available or expired)!

        url = plugin.authenticate(c.id, (id, idc))
        if url != "AlreadyAuthenticated":
            print("url", url)
            return plugin.auto_auth(url, pub.channel_id)
        print('publishing publishings.py', pub)
        plugin.run(pub, c_conf)

    return redirect(url_for('index'))


@pub_page.route('/moderate/unvalidate/<int:id>', methods=["GET", "POST"])
@login_required()
def unvalidate_publishing(id):
    """SAVOIR SI ON FAIT POST_ID ET CHANNEL_ID OU PUBLISHING_ID DIRECTLY"""

    print("pub-id to unvalidate ", id)
    pub = db.session.query(Publishing).filter(Publishing.publishing_id == id).first()
    pub.state = State.REFUSED.value

    """TESTER SI MODERATOR_COMMENT EST NONE"""
    moderator_comment = ""
    if request.form.get('moderator_comment'):
        moderator_comment = request.form.get('moderator_comment')

    comm = db.session.query(Comment).filter(Comment.publishing_id == pub.publishing_id).first()

    if comm:
        comm.moderator_comment=moderator_comment
    else:
        comm = Comment(publishing_id=pub.publishing_id, moderator_comment=moderator_comment)
        db.session.add(comm)

    db.session.commit()
    return redirect(url_for('index'))