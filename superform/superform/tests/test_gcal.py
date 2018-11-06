import datetime
import os
import tempfile

import pytest

from superform import app, db
from superform.models import Publishing, Post, PubGCal
import superform.posts

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

def test_build_pubgcal(client):
    #TODO Basic creation of a gcal publishing
    pubg = PubGCal(post_id=123, channel_id=1,state=0, title="test", date_start="2018-01-01", date_end="2018-01-01")
    assert pubg.post_id == 123
    assert pubg.channel_id == 1
    assert pubg.state == 0
    assert pubg.title == "test"
    assert pubg.date_start == "2018-01-01"
    assert pubg.date_end == "2018-01-01"
''' A reviser...
    login(client, "superego")
    rv = client.post('/new',data=dict(post_id=123, channel_id=1,state=0, title="test", date_start="2018-01-01", date_end="2018-01-01"))
    assert rv.status_code ==302
    posts = db.session.query(Post).all()
    assert len(posts) > 0
    last_add = posts[-1]
    assert last_add.title == "test"
    db.session.query(Publishing).filter(Publishing.id == last_add.id).delete()
    db.session.commit()
    #superform.posts.create_a_post()
'''

def test_invalid_gcal(client):
    #TODO Test excetpion with bad gcal pub
    assert True == True #Test python test