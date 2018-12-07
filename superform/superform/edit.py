import os
from flask import Blueprint, json, jsonify, request, redirect, render_template, session
from superform.utils import login_required, datetime_converter
import json
from superform.models import db, Post, Publishing, Channel, User, PubGCal, PubICTV
from superform.users import channels_available_for_user

from datetime import date, timedelta

#from users import channels_available_for_user

edit_page = Blueprint('edit', __name__)

def load_layout():
    path = os.path.realpath(os.path.dirname(__file__))
    url = os.path.join(path, "static/form", "layout.json")
    return json.load(open(url))

def is_in_channels(channels, name):
    for channel in channels:
        if channel.get("name") == name:
            return True
    return False

#@edit_page.route('/edit/layout/<int:post_id>', methods=['GET'])
#@login_required()
def generate_layout_with_data(post_id):

    user_id = session.get("user_id", "") if session.get("logged_in", False) else -1
    post = db.session.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
    publishings = db.session.query(Publishing).filter(Publishing.post_id == post.id).all()

    layout = load_layout()

    default_fields = {}
    for field in layout.get("default").get("fields"):
        name = field.get("name")
        value = getattr(post, name)
        default_fields[name] = value

    channels = []
    for publishing in publishings:
        channel_db = db.session.query(Channel).filter(Channel.id == publishing.channel_id).first()
        channels.append({
            "module": channel_db.module,
            "name": channel_db.name,
            "state": publishing.state
        })
        fields = {}
        for channel_json in layout.get("channels"):
            if channel_json.get("module") == channel_db.module:
                for field in layout.get("default").get("fields"):
                    name = field.get("name")
                    if name not in channel_json.get("disabled_fields"):
                        value = getattr(publishing, name)
                        fields[name] = value
                for field in channel_json.get("additional_fields"):
                    name = field.get("name")
                    value = getattr(publishing, name)
                    fields[name] = value

        channels[-1]["fields"] = fields

    available_channels = channels_available_for_user(user_id)
    for channel in available_channels:
        if not is_in_channels(channels, channel.name):
            channels.append({
                "module": channel.module,
                "name": channel.name,
                "state": -1,
                "fields": {}
            })

    return jsonify({
        "default": {
            "fields": default_fields
        },
        "channels": channels
    })

@edit_page.route('/edit/<int:post_id>', methods=['GET'])
@login_required()
def edit_post(post_id):
    return render_template('edit.html', post_id=post_id)

@edit_page.route('/edit/publish_edit_post/<int:post_id>', methods=['POST'])
@login_required()
def publish_edit_post(post_id):
    data = request.get_json(force=True)

    current_user_id = session.get("user_id", "")

    post = db.session.query(Post).filter(Post.id == post_id, Post.user_id == current_user_id).first()  # retrieve old post
    pubs = (db.session.query(Publishing).filter((Publishing.post_id == post_id)))  # retrieve old publishings
    if post is None:
        return redirect('/403')

    for d in data:  # d is a post/publication
        print(d)
        name = d.get('name')
        fields = d.get('fields')
        if d.get('name') == 'General':
            post.title = fields.get('title')
            post.description = fields.get('description')
            post.link_url = fields.get('link_url')
            post.image_url = fields.get('image_url')
            if fields.get('date_from') is '':
                # set default date if no date was chosen
                post.date_from = date.today()
            else:
                post.date_from = datetime_converter(fields.get('date_from'))
            if fields.get('date_until') is '':
                post.date_until = date.today() + timedelta(days=7)
            else:
                post.date_until = datetime_converter(fields.get('date_until'))
            db.session.commit()

        else:
            for p in pubs:
                chans = (db.session.query(Channel).filter((Channel.id == p.channel_id))).all()

                for chn in chans:
                    if chn.name == name:

                        db.session.delete(p)  # remove old publication

                        # create new updated publication:
                        title_post = fields.get('title') if (
                            fields.get('title') is not None) else post.title
                        descr_post = fields.get('description') if fields.get(
                            'description') is not None else post.description
                        link_post = fields.get('link_url') if fields.get('link_url') is not None else post.link_url
                        image_post = fields.get('image_url') if fields.get('image_url') is not None else post.image_url

                        if chn.module == 'superform.plugins.gcal':
                            date_start = datetime_converter(fields.get('starting_date')) if datetime_converter(
                                fields.get('starting_date')) is not None else post.date_from  # !! not in json
                            date_end = datetime_converter( fields.get('ending_date')) if datetime_converter(
                                fields.get('ending_date')) is not None else post.date_until  # not in json !
                            hour_start = fields.get('starting_time')\
                                if fields.get('starting_time') is not None else '00:00'
                            hour_end = fields.get('ending_time') if fields.get('ending_time') is not None else '00:00'
                            location = fields.get('location')  # !! not in json
                            color_id = fields.get('color')
                            guests = fields.get('guest_email')
                            visibility = fields.get('visibility')
                            availability = fields.get('availability')

                            pub = PubGCal(post_id=post.id, channel_id=chn.id, state=0, title=title_post,
                                          description=descr_post,
                                          link_url=link_post, image_url=image_post,
                                          date_from=None, date_until=None, date_start=date_start, date_end=date_end,
                                          location=location, color_id=color_id, hour_start=hour_start,
                                          hour_end=hour_end,
                                          guests=guests, visibility=visibility, availability=availability)

                        else:
                            if fields.get('date_from') is '':
                                date_from = date.today()
                            else:
                                date_from = datetime_converter(fields.get('date_from')) if datetime_converter(
                                    fields.get('date_from')) is not None else post.date_from
                            if fields.get('date_until') is '':
                                date_until = date.today() + timedelta(days=7)
                            else:
                                date_until = datetime_converter(
                                    fields.get('date_until')) if datetime_converter(
                                    fields.get('date_until')) is not None else post.date_until
                            if chn.module == 'superform.plugins.ICTV':
                                logo = fields.get('logo')
                                subtitle = fields.get('subtitle')
                                duration = fields.get('duration')

                                pub = PubICTV(post_id=post.id, channel_id=chn.id, state=0, title=title_post,
                                              description=descr_post,
                                              link_url=link_post, image_url=image_post,
                                              date_from=date_from, date_until=date_until, logo=logo, subtitle=subtitle,
                                              duration=duration)
                            else:
                                pub = Publishing(post_id=post.id, channel_id=chn.id, state=0, title=title_post,
                                                 description=descr_post,
                                                 link_url=link_post, image_url=image_post,
                                                 date_from=date_from, date_until=date_until)

                        db.session.add(pub)
                        db.session.commit()


                        """
                        p.title = fields.get('title') if fields.get('title') is not None else title
                        p.description = fields.get('description')
                        p.link_url = fields.get('link_url')
                        p.image_url = fields.get('image_url')
                        if fields.get('date_from') is '':
                            # set default date if no date was chosen
                            p.date_from = date.today()
                        else:
                            p.date_from = datetime_converter(fields.get('date_from'))
                        if fields.get('date_until') is '':
                            p.date_until = date.today() + timedelta(days=7)
                        else:
                            p.date_until = datetime_converter(fields.get('date_until'))
                        db.session.commit()
                        """

    return ('', 200)


@edit_page.route('/edit/layout/<int:post_id>', methods=['GET'])
@login_required()
def create_data_json(post_id):
    current_user_id = session.get("user_id", "")

    json_output = dict()
    dic_second = dict()

    query_post = db.session.query(Post).filter(Post.id == post_id, Post.user_id == current_user_id).first()
    query_pubs = db.session.query(Publishing and PubICTV).filter(Publishing.post_id == post_id).all()

    fields = dict((col, getattr(query_post, col)) for col in query_post.__table__.columns.keys())
    entries_to_delete = ('id', 'user_id', 'date_created')
    for entries in entries_to_delete:
        del fields[entries]

    dic_second["fields"] = fields
    json_output["default"] = dic_second

    module = list()
    for pub in query_pubs:
        channel = dict()
        p = (db.session.query(Channel).filter((Channel.id == pub.channel_id))).first()
        elem = dict((col, getattr(p, col)) for col in p.__table__.columns.keys())
        for e in elem:
            if e == "module" or e == "name":
                channel[e] = elem[e]
        fields = dict()
        for col in pub.__table__.columns.keys():
            try:
                val = getattr(pub, col)
                if col == "state":
                    channel[col] = val
                elif not col == "post_id" and not col == "channel_id":
                    fields[col] = val
            except AttributeError as error:
                pass
        channel["fields"] = fields
        module.append(channel)
    json_output["channels"] = module
    return jsonify(json_output)
