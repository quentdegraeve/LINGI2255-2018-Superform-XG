import datetime
import os
import tempfile

import pytest

from superform import app, db
from superform.plugins import gcal

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

def test_run_gcal(client):
    #TODO Basic creation of a gcal publishing
    assert True == True #Test python test

def test_invalid_gcal(client):
    #TODO Test excetpion with bad gcal pub
    assert True == True #Test python test