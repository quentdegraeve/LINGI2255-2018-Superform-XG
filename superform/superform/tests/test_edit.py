import datetime
import os
import tempfile

import pytest

from superform.models import Authorization, Channel, User
from superform import app, db, Post, Publishing
from superform.utils import datetime_converter, str_converter, get_module_full_name
from superform.users import is_moderator, get_moderate_channels_for_user, channels_available_for_user

@pytest.fixture
def client():
    app.app_context().push()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def login(client, login):

    with client as c:
        with c.session_transaction() as sess:
            if login is not "myself":
                sess["admin"] = True
            else:
                sess["admin"] = False

            sess["logged_in"] = True
            sess["first_name"] = "gen_login"
            sess["name"] = "myname_gen"
            sess["email"] = "hello@genemail.com"
            sess['user_id'] = login

## Testing Functions ##


def test_edit_access(client):
    login(client,"myself")
    rv = client.post('/new',data=dict(titlepost='A new test post', descriptionpost="A description", linkurlpost="http://www.test.com", imagepost="image.jpg",datefrompost="2018-07-01",dateuntilpost="2018-07-01"))
    assert rv.status_code ==302
    posts = db.session.query(Post).all()
    assert len(posts)>0
    last_add = posts[-1]
    url = '/edit/'+str(last_add.id)
    rv = client.get(url)
    assert rv.status_code == 200
    db.session.query(Post).filter(Post.id == last_add.id).delete()
    db.session.commit()


def test_edit_new_post(client):
    login(client,"myself")
    rv = client.post('/new',data=dict(titlepost='A new test post', descriptionpost="A description", linkurlpost="http://www.test.com", imagepost="image.jpg",datefrompost="2018-07-01",dateuntilpost="2018-07-01"))
    assert rv.status_code ==302
    posts = db.session.query(Post).all()
    last_add = posts[-1]
    url = '/edit/publish_edit_post/'+str(last_add.id)
    rv = client.post(url,data=dict(titlepost='An edited test post', descriptionpost="A description", linkurlpost="http://www.test.com", imagepost="image.jpg",datefrompost="2018-07-01",dateuntilpost="2018-07-01"))
    assert rv.status_code != 302
    edited_posts = db.session.query(Post).all()
    assert len(posts) == len(edited_posts)
    edited_post = edited_posts[-1]
    assert edited_post.title != 'An edited test post'
    assert last_add.id == edited_post.id
    assert edited_post.description == "A description"
    db.session.query(Post).filter(Post.id == last_add.id).delete()
    db.session.commit()


def test_edit_forbidden(client):
    login(client,"myself")
    rv = client.post('/new',data=dict(titlepost='A new test post', descriptionpost="A description", linkurlpost="http://www.test.com", imagepost="image.jpg",datefrompost="2018-07-01",dateuntilpost="2018-07-01"))
    assert rv.status_code == 302
    posts = db.session.query(Post).all()
    last_add = posts[-1]
    url_get = '/edit/'+str(last_add.id)
    url_post = '/edit/publish_edit_post/'+str(last_add.id)
    login(client, "alterego")
    rv = client.get(url_get)
    assert rv.status_code == 200
    rv = client.post(url_post,data=dict(titlepost='An edited test post', descriptionpost="A description", linkurlpost="http://www.test.com", imagepost="image.jpg",datefrompost="2018-07-01",dateuntilpost="2018-07-01"))
    #assert rv.status_code != 302
    edited_posts = db.session.query(Post).all()
    assert len(posts) == len(edited_posts)
    edited_post = edited_posts[-1]
    assert edited_post.title == 'A new test post'
    assert last_add.id == edited_post.id
    assert edited_post.description == "A description"
    db.session.query(Post).filter(Post.id == last_add.id).delete()
    db.session.commit()