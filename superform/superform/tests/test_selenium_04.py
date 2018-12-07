import datetime
import os
from time import sleep
import tempfile

import pytest

from superform.suputils import selenium_utils
from superform import app, db, Post, Publishing, Channel


TWITTER_NAME = 'test_twitter123'
ICTV_NAME = 'test_ICTV123'

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

@pytest.fixture(scope='session', autouse=True)
def prepare():
    pytest.driver = selenium_utils.get_chrome()
    pytest.now = datetime.datetime.now().strftime("%d%m%Y")

    selenium_utils.login(pytest.driver, "superego", "superego")

    selenium_utils.create_channel(pytest.driver, TWITTER_NAME, 'twitter')
    selenium_utils.create_channel(pytest.driver, ICTV_NAME, 'ICTV')

    selenium_utils.add_authorization(pytest.driver, TWITTER_NAME, "superego", 2)
    selenium_utils.add_authorization(pytest.driver, ICTV_NAME, "superego", 2)

    yield

    pytest.driver.close()



def test_edit_post(client):
    title = 'test_edit titre 1'
    description = 'test_edit description'
    selenium_utils.add_new_post(pytest.driver, [TWITTER_NAME], title, description, pytest.now, pytest.now)
    sleep(1)
    posts = db.session.query(Post).all()
    assert len(posts) > 0
    post = posts[-1]
    sleep(1)
    selenium_utils.edit_post(pytest.driver, post.id, title, description, pytest.now, pytest.now)




def test_ictv_post(client):
    title = 'test_ictv titre 1'
    description = 'test_edit description'
    selenium_utils.add_new_post(pytest.driver, [ICTV_NAME], title, description, pytest.now, pytest.now)
    sleep(1)
    posts = db.session.query(Post).all()
    assert len(posts) > 0
    post = posts[-1]




def test_twitter_post(client):
    description = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.'
    channels = db.session.query(Channel).filter(Channel.name == TWITTER_NAME)
    channel_id = channels[0].id
    selenium_utils.add_new_twitter_publishing(pytest.driver, [TWITTER_NAME], channel_id, description, pytest.now, pytest.now, 'www.google.com')
    sleep(1)
    posts = db.session.query(Post).all()
    assert len(posts) > 0
    post = posts[-1]



def test_ictv_post(client):
    title = 'test_ictv titre 2'
    description = 'Little ICTV post description'
    channels =  db.session.query(Channel).filter(Channel.name == ICTV_NAME)
    channel_id = channels[0].id
    selenium_utils.add_new_ictv_publishing(pytest.driver, [ICTV_NAME], channel_id, title, description, pytest.now, pytest.now, 'www.google.com', 1)
    sleep(1)
    posts = db.session.query(Post).all()
    assert len(posts) > 0
    post = posts[-1]


