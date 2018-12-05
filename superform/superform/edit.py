from flask import Blueprint, url_for, request, redirect, render_template, session

from superform.utils import login_required, datetime_converter
from superform.models import db, Post, Publishing, Channel, User

from datetime import date, timedelta

edit_page = Blueprint('edit', __name__)

@edit_page.route('/edit/<int:post_id>', methods=['GET'])
@login_required()
def edit_post(post_id):
    return render_template('edit.html', post_id=post_id)

@edit_page.route('/edit/publish_edit_post/<int:post_id>', methods=['POST'])
@login_required()
def publish_edit_post(post_id):
    data = request.get_json(force=True)

    print(data)

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
            title = post.title
            post.description = fields.get('description')
            post.link_url = fields.get('link')
            post.image_url = fields.get('image')
            if fields.get('publication_date') is '':
                # set default date if no date was chosen
                post.date_from = date.today()
            else:
                post.date_from = datetime_converter(fields.get('publication_date'))
            if fields.get('publication_until') is '':
                post.date_until = date.today() + timedelta(days=7)
            else:
                post.date_until = datetime_converter(fields.get('publication_until'))
            db.session.commit()

        else:
            for p in pubs:
                chan_name = (db.session.query(Channel).filter((Channel.id == p.channel_id))).first().name
                chan_name = 'My first Twitter account'  # to change !!!!
                if chan_name == name:
                    p.title = fields.get('title') if fields.get('title') is not None else title
                    p.description = fields.get('description')
                    p.link_url = fields.get('link')
                    p.image_url = fields.get('image')
                    if fields.get('publication_date') is '':
                        # set default date if no date was chosen
                        p.date_from = date.today()
                    else:
                        p.date_from = datetime_converter(fields.get('publication_date'))
                    if fields.get('publication_until') is '':
                        p.date_until = date.today() + timedelta(days=7)
                    else:
                        p.date_until = datetime_converter(fields.get('publication_until'))
                    db.session.commit()

    return redirect(url_for('index'))
