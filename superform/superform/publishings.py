from flask import Blueprint, url_for, request, redirect, render_template
from superform.utils import login_required, datetime_converter, str_converter
from superform.models import db, Publishing, Channel
from importlib import import_module
import json

pub_page = Blueprint('publishings', __name__)


@pub_page.route('/moderate/<int:id>/<int:idc>', methods=["GET", "POST"])
@login_required()
def moderate_publishing(id, idc):
    pub = db.session.query(Publishing).filter(Publishing.post_id == id, Publishing.channel_id == idc).first()
    chan = db.session.query(Channel).filter(Channel.id == idc).first()
    pub.date_from = str_converter(pub.date_from)
    pub.date_until = str_converter(pub.date_until)
    if request.method == "GET":
        plugin = import_module(chan.module)
        if pub.misc is not None:
            misc = json.loads(pub.misc) #   adding extra fields to context (might be empty)
        else:
            misc = {}
        print('get moderate_publishing')
        return render_template('moderate_post.html', extra=misc, template=plugin.get_template_mod(), pub=pub, chan=chan)
    else:
        print('post moderate_publishing')
        pub.title = request.form.get('titlepost')
        pub.description = request.form.get('descrpost')
        pub.link_url = request.form.get('linkurlpost')
        pub.image_url = request.form.get('imagepost')
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
        plugin = import_module(plugin_name)

        #every plugin should implement the autheticate method that redirect to the plugin authentication process
        #if it is required or necessary (no token available or expired)!

        url = plugin.authenticate(c.name, (id, idc))
        if url != "AlreadyAuthenticated":
            print("url", url)
            return plugin.auto_auth(url, pub.channel_id)
        print('publishing publishings.py', pub)
        plugin.run(pub, c_conf)

        return redirect(url_for('index'))
