from superform.plugins import linkedin
import os
import tempfile

from datetime import datetime, timedelta

import pytest

from superform.models import Channel
from superform import app, db, Post, posts
from superform.utils import get_module_full_name

API_KEY = '861s90686z5fuz'
API_SECRET = 'xHDD886NZNkWVuN4'
RETURN_URL = 'http://localhost:5000'

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

def test_pre_validate_post_title():
    chan = Channel
    post = Post
    post.title = "x" * 200
    post.description = "x"
    chan.module = "superform.plugins.linkedin"
    assert posts.pre_validate_post(chan, post) == 1
    post.title += "x"
    assert posts.pre_validate_post(chan, post) == 0
    post.title = ""
    assert posts.pre_validate_post(chan, post) == 0

def test_pre_validate_post_description():
    chan = Channel
    post = Post
    post.title = "x"
    post.description = "x" * 256
    chan.module = "superform.plugins.linkedin"
    assert posts.pre_validate_post(chan, post) == 1
    post.description += "x"
    assert posts.pre_validate_post(chan, post) == 0
    post.description = ""
    assert posts.pre_validate_post(chan, post) == 0

def test_authenticate(client):
    false_post_id = -1
    false_channel_id = -1
    url = linkedin.authenticate("name_test", (false_post_id, false_channel_id))
    assert url != 'AlreadyAuthenticated'

def test_authenticate2(client):
    linkedin_access_token = "test_token"
    linkedin_token_expiration_date = datetime.now() + timedelta(seconds=60)
    channel_name = "channel_test"
    c_test = Channel(name=channel_name, module=get_module_full_name("linkedin"), config="{}", linkedin_access_token=linkedin_access_token, linkedin_token_expiration_date=linkedin_token_expiration_date)

    db.session.add(c_test)
    linkedin.LinkedinTokens.put_token(linkedin.LinkedinTokens, "channel_test", linkedin_access_token,
                                      linkedin_token_expiration_date)
    false_post_id = -1
    false_channel_id = -1
    url = linkedin.authenticate(channel_name, (false_post_id, false_channel_id))
    assert url == 'AlreadyAuthenticated'
