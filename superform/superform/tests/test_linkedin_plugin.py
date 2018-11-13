import importlib
import pkgutil

import superform
from superform.plugins import linkedin
import os
import tempfile

from superform.suputils import keepass
from datetime import datetime, timedelta

import pytest

from flask import Flask
from superform.models import Channel
from superform import app, db, Post, posts
from superform.utils import get_module_full_name
from superform.models import db as _db
from superform.plugins import linkedin

API_KEY = keepass.get_password_from_keepass('linkedin_key')
API_SECRET = keepass.get_password_from_keepass('linkedin_secret')
RETURN_URL = 'http://localhost:5000'

TESTDB = 'test_superform.db'
TESTDB_PATH = "/{}".format(TESTDB)
TEST_DATABASE_URI = 'sqlite:///' + TESTDB_PATH


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
    app.config['TESTING'] = True
    app.config["PLUGINS"] = {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in pkgutil.iter_modules(superform.plugins.__path__, superform.plugins.__name__ + ".")
    }
    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    if os.path.exists(TESTDB_PATH):
        os.unlink(TESTDB_PATH)

    def teardown():
        _db.drop_all()
        os.unlink(TESTDB_PATH)

    _db.init_app(app)
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session

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


def test_authenticate(session):
    false_post_id = -1
    false_channel_id = -1
    url = linkedin.authenticate("name_test", (false_post_id, false_channel_id))
    assert url != 'AlreadyAuthenticated'


def test_authenticate2(session):
    linkedin_access_token = "test_token"
    linkedin_token_expiration_date = datetime.now() + timedelta(seconds=60)
    channel_name = "channel_test"
    c_test = Channel(name=channel_name, module=get_module_full_name("linkedin"), config="{}")

    session.add(c_test)
    conf = dict()
    conf["channel_name"] = channel_name
    conf["linkedin_access_token"] = linkedin_access_token
    conf["linkedin_token_expiration_date"] = linkedin_token_expiration_date.__str__()
    linkedin.LinkedinTokens.put_token(linkedin.LinkedinTokens, "channel_test", conf)
    false_post_id = -1
    false_channel_id = -1
    url = linkedin.authenticate(channel_name, (false_post_id, false_channel_id))
    assert url == 'AlreadyAuthenticated'
