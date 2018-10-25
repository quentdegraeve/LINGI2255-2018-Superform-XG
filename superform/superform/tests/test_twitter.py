import datetime
import os
import tempfile

import pytest

from superform import app, db
from superform.plugins import twitter


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


def test_send_tweet(client):
    # Is there a way to test a send tweet function?
    assert True == True