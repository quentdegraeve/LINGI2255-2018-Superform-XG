from superform.models import Channel
from superform.suputils import plugin_utils


def test_pre_validate_post_title():
    chan = Channel
    chan.module = "superform.plugins.slack"
    plugin_utils.test_pre_validate_post_title(chan,40000)


def test_pre_validate_post_description():
    chan = Channel
    chan.module = "superform.plugins.slack"
    plugin_utils.test_pre_validate_post_description(chan,40000)

def test_prevalidate_post_link_url():
    chan = Channel
    chan.module = "superform.plugins.slack"
    plugin_utils.test_pre_validate_post_Link_url(chan)

def test_prevalidate_post_img_url():
    chan = Channel
    chan.module = "superform.plugins.slack"
    plugin_utils.test_pre_validate_post_img_url(chan)
