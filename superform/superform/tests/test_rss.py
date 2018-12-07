from superform.suputils import plugin_utils
from superform.models import Channel, Post, Publishing
from superform.plugins import rss
from superform.models import db

def test_pre_validate_post_title():
    chan = Channel
    chan.module = "superform.plugins.rss"
    plugin_utils.test_pre_validate_post_title(chan,40000)

def test_pre_validate_post_description():
    chan = Channel
    chan.module = "superform.plugins.rss"
    plugin_utils.test_pre_validate_post_description(chan,40000)

def test_prevalidate_post_link_url():
    chan = Channel
    chan.module = "superform.plugins.rss"
    plugin_utils.test_pre_validate_post_Link_url(chan)

def test_prevalidate_post_img_url():
    chan = Channel
    chan.module = "superform.plugins.rss"
    plugin_utils.test_pre_validate_post_img_url(chan)

def test_postpre_rss():
    ret_code = rss.post_pre_validation(
        Post(title="rss test", description="desc rss test", link_url="www.test.com", image_url="www.test.com"))
    assert ret_code == 1

def test_authenticate():
    ret_code = rss.authenticate(0,0)
    assert ret_code == 'AlreadyAuthenticated'

def test_deletable():
    ret_code = rss.deletable()
    assert ret_code == True

# def test_post_db(): #Test on publishing in the DB, create a publication and test it is in then rollback DB
#     cursor = db.cursor()
#     sql_command = """
#             INSERT INTO publishing (state)
#             VALUES (0);
#             """
#     cursor.execute(sql_command)
#     db.session.commit()
#
#     pub = db.session.query(Publishing).filter((Publishing.state == 0))
#     rss.run(pub, "config")
#
#     assert db.session.query(Publishing).filter((Publishing.state == 1))
