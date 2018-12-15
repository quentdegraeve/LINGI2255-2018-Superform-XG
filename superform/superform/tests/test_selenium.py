import datetime
import tempfile
import os

import pytest

from superform.suputils import selenium_utils
from superform.suputils import keepass
from superform import app, db, Post


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

    pytest.linkedin_title_max = 200
    pytest.linkedin_description_max = 256
    pytest.slack_title_max = 40000
    pytest.slack_description_max = 40000

    keepass.set_entry_from_keepass('account_superform')
    selenium_utils.login(pytest.driver, keepass.KeepassEntry.username, keepass.KeepassEntry.password)

    keepass.set_entry_from_keepass('account_linkedin')
    selenium_utils.create_channel(pytest.driver, 'test_linkedin', 'linkedin', keepass.KeepassEntry.username, keepass.KeepassEntry.password)
    pytest.linkedin_channel_id = 1

    keepass.set_entry_from_keepass('account_slack')
    selenium_utils.create_channel(pytest.driver, 'test_slack', 'slack', keepass.KeepassEntry.username, keepass.KeepassEntry.password)
    pytest.slack_channel_id = 2
    selenium_utils.modify_config(pytest.driver, pytest.slack_channel_id, 'testlingi2255team8', 'general')


    selenium_utils.add_authorization(pytest.driver, 'test_linkedin', 'superego', pytest.slack_channel_id)
    selenium_utils.add_authorization(pytest.driver, 'test_slack', 'superego', pytest.slack_channel_id)

    yield

    pytest.driver.close()


def test_add_post_linkedin(client):
    title = 'test_linkedin title'
    description = 'test_linkedin description'
    selenium_utils.add_new_post(pytest.driver, ['test_linkedin'], title, description, pytest.now, pytest.now, 'https://www.google.be/')
    pytest.driver.get(selenium_utils.moderate_url)
    posts = db.session.query(Post).all()
    last = posts[-1]
    assert pytest.driver.find_elements_by_css_selector('a[href="/moderate/' + str(last.id) + '/' +
                                                       str(pytest.linkedin_channel_id) + '"]')


def test_add_post_slack(client):
    title = 'test_slack title'
    description = 'test_slack description'
    selenium_utils.add_new_post(pytest.driver, ['test_slack'], title, description, pytest.now, pytest.now, 'https://www.google.be/')
    pytest.driver.get(selenium_utils.moderate_url)
    posts = db.session.query(Post).all()
    last = posts[-1]
    assert pytest.driver.find_elements_by_css_selector('a[href="/moderate/' + str(last.id) + '/'
                                                       + str(pytest.slack_channel_id) + '"]')


def test_publish_post_linkedin_1():
    selenium_utils.moderate_post(pytest.driver, 1, 1)
    pytest.driver.get(selenium_utils.moderate_url)

    assert not pytest.driver.find_elements_by_css_selector('a[href="/moderate/1/1"]')


def test_publish_post_slack_1():
    selenium_utils.moderate_post(pytest.driver, 2, 2)
    pytest.driver.get(selenium_utils.moderate_url)

    assert not pytest.driver.find_elements_by_css_selector('a[href="/moderate/2/2"]')


def test_add_post_linkedin_slack():
    title = 'test_linkedin_slack title'
    description = 'test_linkedin_slack description'
    selenium_utils.add_new_post(pytest.driver, ['test_linkedin', 'test_slack'], title, description, pytest.now, pytest.now, 'https://www.google.be/')
    pytest.driver.get(selenium_utils.moderate_url)

    assert pytest.driver.find_elements_by_css_selector('a[href="/moderate/3/1"]')
    assert pytest.driver.find_elements_by_css_selector('a[href="/moderate/3/2"]')


def test_publish_post_linkedin_2():
    selenium_utils.moderate_post(pytest.driver, 1, 3)
    pytest.driver.get(selenium_utils.moderate_url)

    assert not pytest.driver.find_elements_by_css_selector('a[href="/moderate/3/1"]')


def test_publish_post_slack_2():
    selenium_utils.moderate_post(pytest.driver, 2, 3)
    pytest.driver.get(selenium_utils.moderate_url)

    assert not pytest.driver.find_elements_by_css_selector('a[href="/moderate/3/2"]')


def test_add_post_linkedin_empty_title():
    title = ''
    description = 'test_slack description'
    selenium_utils.add_new_post(pytest.driver, ['test_linkedin'], title, description, pytest.now, pytest.now)

    assert pytest.driver.find_elements_by_css_selector('div[id="error_test_linkedin_titlepost"]')


def test_add_post_slack_empty_title():
    title = ''
    description = 'test_linkedin description'
    selenium_utils.add_new_post(pytest.driver, ['test_slack'], title, description, pytest.now, pytest.now)

    assert pytest.driver.find_elements_by_css_selector('div[id="error_test_slack_titlepost"]')


def test_add_post_linkedin_empty_description():
    title = 'test_linkedin title'
    description = ''
    selenium_utils.add_new_post(pytest.driver, ['test_linkedin'], title, description, pytest.now, pytest.now)

    assert pytest.driver.find_elements_by_css_selector('div[id="error_test_linkedin_descriptionpost"]')


def test_add_post_slack_empty_description():
    title = 'test_slack title'
    description = ''
    selenium_utils.add_new_post(pytest.driver, ['test_slack'], title, description, pytest.now, pytest.now)

    assert pytest.driver.find_elements_by_css_selector('div[id="error_test_slack_descriptionpost"]')


def test_add_post_linkedin_wrong_title():
    title = "x" * (pytest.linkedin_title_max + 1)
    description = 'test_slack description'
    selenium_utils.add_new_post(pytest.driver, ['test_linkedin'], title, description, pytest.now, pytest.now)

    assert pytest.driver.find_elements_by_css_selector('div[id="error_test_linkedin_titlepost"]')


def test_add_post_linkedin_wrong_description():
    title = 'test_linkedin title'
    description = "x" * (pytest.linkedin_description_max + 1)
    selenium_utils.add_new_post(pytest.driver, ['test_linkedin'], title, description, pytest.now, pytest.now)

    assert pytest.driver.find_elements_by_css_selector('div[id="error_test_linkedin_descriptionpost"]')


def test_add_post_linkedin_wrong_link():
    title = 'test_linkedin title'
    description = 'test_linkedin description'
    link = 'test'
    selenium_utils.add_new_post(pytest.driver, ['test_linkedin'], title, description, pytest.now, pytest.now, link=link)

    assert pytest.driver.find_elements_by_css_selector('div[id="error_test_linkedin_linkurlpost"]')


def test_add_post_slack_wrong_link():
    title = 'test_linkedin title'
    description = 'test_linkedin description'
    link = 'test'
    selenium_utils.add_new_post(pytest.driver, ['test_slack'], title, description, pytest.now, pytest.now, link=link)

    assert pytest.driver.find_elements_by_css_selector('div[id="error_test_slack_linkurlpost"]')


"""
def test_add_post_linkedin_empty_begining_date():
    title = 'test_linkedin title'
    description = 'test_linkedin description'
    selenium_utils.add_new_post(pytest.driver, ['test_linkedin'], title, description, '', pytest.now)

    assert pytest.driver.find_elements_by_css_selector('div[id="error_test_linkedin_datefrompost"]')


def test_add_post_linkedin_empty_ending_date():
    title = 'test_linkedin title'
    description = 'test_linkedin description'
    selenium_utils.add_new_post(pytest.driver, ['test_linkedin'], title, description, pytest.now, '')

    assert pytest.driver.find_elements_by_css_selector('div[id="error_test_linkedin_dateuntilpost"]')
    
    
def test_add_post_slack_empty_begining_date():
    title = 'test_slack title'
    description = 'test_slack description'
    selenium_utils.add_new_post(pytest.driver, ['test_linkedin'], title, description, '', pytest.now)

    assert pytest.driver.find_elements_by_css_selector('div[id="error_datefrompost"]')


def test_add_post_slack_empty_ending_date():
    title = 'test_slack title'
    description = 'test_slack description'
    selenium_utils.add_new_post(pytest.driver, ['test_linkedin'], title, description, pytest.now, '')

    assert pytest.driver.find_elements_by_css_selector('div[id="error_dateuntilpost"]')
"""


def test_add_post_linkedin_wrong_begining_ending_date():
    title = 'test_linkedin title'
    description = 'test_linkedin description'
    end_date = datetime.datetime.now() - datetime.timedelta(days=2)
    selenium_utils.add_new_post(pytest.driver, ['test_linkedin'], title, description, pytest.now, end_date.strftime("%d%m%Y"))

    assert pytest.driver.find_elements_by_css_selector('div[id="error_test_linkedin_dateuntilpost"]')


def test_add_post_slack_wrong_begining_ending_date():
    title = 'test_slack title'
    description = 'test_slack description'
    end_date = datetime.datetime.now() - datetime.timedelta(days=2)
    selenium_utils.add_new_post(pytest.driver, ['test_slack'], title, description, pytest.now, end_date.strftime("%d%m%Y"))

    assert pytest.driver.find_elements_by_css_selector('div[id="error_test_slack_dateuntilpost"]')


def test_resubmit_post():
    title = 'test_linkedin_sjs'
    description = 'test_linkedin descriptiondss'
    selenium_utils.add_new_post(pytest.driver, ['test_linkedin'], title, description, pytest.now, pytest.now,
                                'https://www.google.be/')
    #TO DO
    pytest.driver.get(selenium_utils.moderate_url)

    assert pytest.driver.find_elements_by_css_selector('a[href="/moderate/4/1"]')

    selenium_utils.moderate_post_with_reject(pytest.driver, 1, 4, "your post not good")

    #check that the post have been really refused
    assert not pytest.driver.find_elements_by_css_selector('a[href="/moderate/4/1"]')

    pytest.driver.get(selenium_utils.index_url)
    assert pytest.driver.find_elements_by_css_selector('a[href="/publishing/resubmit/5"]')

    selenium_utils.resubmit_post(pytest.driver, 5, "oups i forgot")

    #check that the post is in the posts to be moderated again
    pytest.driver.get(selenium_utils.moderate_url)

    assert pytest.driver.find_elements_by_css_selector('a[href="/moderate/4/1"]')


def test_comments_displayed():
    #check if all commemments are displayed at the moderation
    #are all two comment displayed
    pytest.driver.get(selenium_utils.moderate_url+"/4/" + str(pytest.linkedin_channel_id))
    assert pytest.driver.find_elements_by_css_selector('div[id="mod_1"]')

    selenium_utils.moderate_post_with_reject(pytest.driver, 1, 4, "hahha no way, you troll")

    pytest.driver.get(selenium_utils.index_url)
    assert pytest.driver.find_elements_by_css_selector('a[href="/publishing/resubmit/6"]')

    # check if all commemments are displayed at the moderation
    # are all two comment displayed
    pytest.driver.get(selenium_utils.resubmit_url+"/6")
    assert pytest.driver.find_elements_by_css_selector('div[id="user_2"]')
    assert pytest.driver.find_elements_by_css_selector('div[id="mod_2"]')


