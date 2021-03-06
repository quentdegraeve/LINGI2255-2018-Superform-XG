from flask import Blueprint, url_for, request, redirect, render_template, session

from superform.utils import login_required, datetime_converter, str_converter
from superform.models import db, Channel, PubGCal

pub_page = Blueprint('publishings', __name__)
@pub_page.route('/moderate/<int:id>/<string:idc>',methods=["GET","POST"])
@login_required()
def moderate_publishing(id,idc):
    pub = db.session.query(PubGCal).filter(PubGCal.post_id==id,PubGCal.channel_id==idc).first()
    pub.date_from = str_converter(pub.date_from)
    pub.date_until = str_converter(pub.date_until)
    if request.method=="GET":
        return render_template('moderate_post.html', pub=pub)
    else:
        pub.title = request.form.get('titlepost')
        pub.description = request.form.get('descrpost')
        pub.link_url = request.form.get('linkurlpost')
        pub.datedebut=datetime_converter(request.form.get('datedebut'))
        pub.heuredebut=request.form.get('heuredebut')
        pub.datefin=datetime_converter(request.form.get('datefin'))
        pub.heurefin=request.form.get('heurefin')
        pub.location = request.form.get('location')
        pub.color = request.form.get('color')
        pub.visibility = request.form.get('visibility')
        pub.availability = request.form.get('availability')
        pub.guests = request.form.get('guests')
        pub.image_url = request.form.get('imagepost')
        pub.date_from = datetime_converter(request.form.get('datefrompost'))
        pub.date_until = datetime_converter(request.form.get('dateuntilpost'))
        #state is shared & validated
        pub.state = 1
        db.session.commit()
        #running the plugin here
        c=db.session.query(Channel).filter(Channel.name == pub.channel_id).first()
        plugin_name = c.module
        c_conf = c.config
        from importlib import import_module
        plugin = import_module(plugin_name)
        plugin.run(pub, c_conf)

        return redirect(url_for('index'))
