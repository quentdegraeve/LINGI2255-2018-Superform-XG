from superform.plugins import linkedin
import os
import tempfile

from datetime import datetime, timedelta

import pytest

from superform.models import Authorization, Channel
from superform import app, db, Post, User
from superform.utils import datetime_converter, str_converter, get_module_full_name
from superform.users import  is_moderator, get_moderate_channels_for_user,channels_available_for_user

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

def test_authenticate(client):
    false_post_id = -1
    false_channel_id = -1
    url = linkedin.authenticate("name_test", (false_post_id, false_channel_id))
    assert url != 'AlreadyAuthenticated'

def test_authenticate2(client):
    linkedin_access_token = "test_token"
    linkedin_token_expiration_date = datetime.now() +timedelta(seconds=60)
    channel_name = "channel_test"
    c_test = Channel(id=1, name=channel_name, module=get_module_full_name("linkedin"), config="{}", linkedin_access_token=linkedin_access_token, linkedin_token_expiration_date=linkedin_token_expiration_date)
    db.session.add(c_test)
    linkedin.LinkedinTokens.put_token(linkedin.LinkedinTokens, "channel_test", linkedin_access_token, linkedin_token_expiration_date)
    false_post_id = -1
    false_channel_id = -1
    url = linkedin.authenticate(channel_name, (false_post_id, false_channel_id))
    assert url == 'AlreadyAuthenticated'
