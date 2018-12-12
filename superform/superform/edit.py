import os
from flask import Blueprint, json, jsonify, request, redirect, render_template, session
from superform.utils import login_required, datetime_converter
import json
from superform.models import db, Post, Publishing, Channel, User, PubGCal
from superform.users import channels_available_for_user

from datetime import date, timedelta

#from users import channels_available_for_user

edit_page = Blueprint('edit', __name__)

@edit_page.route('/edit/<int:post_id>', methods=['GET'])
@login_required()
def edit_post(post_id):
    """
    Method called in the home page, when the user clicks on the 'Edit' button on a post.
    Generate the layout of the page, with the fields of the post filled with the values stored in the database.
    :param post_id: The id of the post in the database
    :return: The template of the html edition page
    """
    return render_template('edit.html', post_id=post_id)

@edit_page.route('/edit/publish_edit_post/<int:post_id>', methods=['POST'])
@login_required()
def publish_edit_post(post_id):
    """
    Method called in the edition page, when the user clicks on the 'Save and publish' button.
    It is called with an http post request.
    The method will save the changes to the post fields in the database.
    :param post_id: The id of the post in the database
    :return: An http error/sucess code
    """
    data = request.get_json(force=True)

    current_user_id = session.get("user_id", "")

    post = db.session.query(Post).filter(Post.id == post_id, Post.user_id == current_user_id).first()  # retrieve old post
    pubs = db.session.query(Publishing).filter(Publishing.post_id == post_id).all()  # retrieve old publishings
    if post is None:
        return redirect('/403')

    for d in data:  # d is a post/publication
        name = d.get('name')
        fields = d.get('fields')
        if d.get('name') == 'General':
            keys = fields.keys()
            for k in keys:
                if (k == 'date_from') and (fields.get(k) is ''):
                    setattr(post, k, date.today())
                elif (k == 'date_until') and (fields.get(k) is ''):
                    setattr(post, k, date.today() + timedelta(days=7))
                elif k in {'date_from', 'date_until'}:
                    setattr(post, k, datetime_converter(fields.get(k)))
                else:
                    setattr(post, k, fields.get(k))
            db.session.commit()

        else:
            for pub in pubs:
                chans = db.session.query(Channel).filter(Channel.id == pub.channel_id).all()
                if pub.state == 1:
                    setattr(pub, 'state', 4)
                for chn in chans:
                    if chn.name == name:
                        keys = fields.keys()
                        for k in keys:
                            if (k == 'date_from') and (fields.get(k) is ''):
                                setattr(pub, k, date.today())
                            elif (k == 'date_until') and (fields.get(k) is ''):
                                setattr(pub, k, date.today()+timedelta(days=7))
                            elif k in {'date_from', 'date_until', 'date_start', 'date_end'}:
                                setattr(pub, k, datetime_converter(fields.get(k)))
                            else:
                                setattr(pub, k, fields.get(k))
                        db.session.commit()

    return ('', 200)


@edit_page.route('/edit/layout/<int:post_id>', methods=['GET'])
@login_required()
def create_data_json(post_id):
    """
    This method is called when loading the edition page.
    It is responsible for getting the post and publication data from the database and encoding it inside a json.
    :param post_id: The id of the post in the database
    :return: The data related to the post/publication, in json format
    """
    current_user_id = session.get("user_id", "")

    json_output = dict()
    dic_second = dict()

    query_post = db.session.query(Post).filter(Post.id == post_id, Post.user_id == current_user_id).first()
    query_pubs = db.session.query(Publishing).filter(Publishing.post_id == post_id).all()
    list_of_channels = channels_available_for_user(current_user_id)

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
        if p in list_of_channels:
            list_of_channels.remove(p)
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

    for chan in list_of_channels:
        channel = dict()
        channel["name"] = chan.name
        channel["module"] = chan.module
        channel["state"] = -1
        module.append(channel)

    json_output["channels"] = module
    return jsonify(json_output)
