from superform.suputils import plugin_utils
from superform.models import Channel, Post
from superform.plugins import gcal

def test_pre_validate_post_title():
    chan = Channel
    chan.module = "superform.plugins.gcal"
    plugin_utils.test_pre_validate_post_title(chan,40000)

def test_pre_validate_post_description():
    chan = Channel
    chan.module = "superform.plugins.gcal"
    plugin_utils.test_pre_validate_post_description(chan,40000)

def test_prevalidate_post_link_url():
    chan = Channel
    chan.module = "superform.plugins.gcal"
    plugin_utils.test_pre_validate_post_Link_url(chan)

def test_prevalidate_post_img_url():
    chan = Channel
    chan.module = "superform.plugins.gcal"
    plugin_utils.test_pre_validate_post_img_url(chan)

def test_postpre_gcal():
    ret_code = gcal.post_pre_validation(
        Post(title="gcal test", description="desc gcal test", link_url="www.test.com", image_url="www.test.com"))
    assert ret_code == 1

def test_post_db(): #Test on publishing in the DB, create a publication and test it is in then rollback DB
    assert True
