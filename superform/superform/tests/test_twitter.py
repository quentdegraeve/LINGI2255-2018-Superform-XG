import datetime
import os
import tempfile
import sys
import contextlib

import pytest

from superform import app, db, Publishing
from superform.models import Channel
from superform.plugins import twitter
from io import StringIO


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

def test_send_tweet_bad_config(client):
    name = "unittest_twitter"
    module = "superform.plugins.twitter"
    P = Publishing(post_id=0,channel_id=name,state=0,title='test',description='unit test')
    C = Channel(name=name, module=module, config="{}")
    db.session.add(C)
    db.session.add(P)
    db.session.commit()
    pub = db.session.query(Publishing).filter(Publishing.post_id == 0, Publishing.channel_id == name).first()
    c = db.session.query(Channel).filter(Channel.name == pub.channel_id).first()
    temp_stdout = StringIO()
    with contextlib.redirect_stdout(temp_stdout):
        twitter.run(pub,c.config)
    output = temp_stdout.getvalue().strip()
    db.session.query(Publishing).filter(Publishing.post_id == 0).delete()
    db.session.query(Channel).filter(Channel.name == name).delete()
    db.session.commit()
    assert 'Missing' in output
    #we only test how the plugin handle bad config as this doesn't send real tweet
