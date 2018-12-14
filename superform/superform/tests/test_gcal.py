from superform.models import Channel, Post
from superform.plugins import gcal
from superform.posts import pre_validate_post


def test_pre_validate_post_title():
    chan = Channel
    chan.module = "superform.plugins.gcal"
    pre_validate_post_title(chan,40000)

def test_pre_validate_post_description():
    chan = Channel
    chan.module = "superform.plugins.gcal"
    pre_validate_post_description(chan,40000)

def test_prevalidate_post_link_url():
    chan = Channel
    chan.module = "superform.plugins.gcal"
    pre_validate_post_Link_url(chan)

def test_prevalidate_post_img_url():
    chan = Channel
    chan.module = "superform.plugins.gcal"
    pre_validate_post_img_url(chan)

def test_postpre_gcal():
    ret_code = gcal.post_pre_validation(
        Post(title="gcal test", description="desc gcal test", link_url="www.test.com", image_url="www.test.com"))
    assert ret_code == 1

def test_authenticate():
    ret_code = gcal.authenticate(0,0)
    assert ret_code == 'AlreadyAuthenticated'

def test_deletable():
    ret_code = gcal.deletable()
    assert ret_code == True

def pre_validate_post_title(channel,maxLengthTitle):

    post = Post
    post.title = "x" * maxLengthTitle
    post.description = "x"
    post.link_url = "https://www.test.com"
    post.image_url ="https://www.test.com"
    assert pre_validate_post(channel, post) == 1
    post.title += "x"
    assert pre_validate_post(channel, post) == 0
    post.title = ""
    assert pre_validate_post(channel, post) == 0


def pre_validate_post_description(channel, maxLengthDescription):
    post = Post
    post.title = "x"
    post.description = "x" * maxLengthDescription
    post.link_url = "https://www.test.com"
    post.image_url = "https://www.test.com"
    assert pre_validate_post(channel, post) == 1
    post.description += "x"
    assert pre_validate_post(channel, post) == 0
    post.description = ""
    assert pre_validate_post(channel, post) == 0

def pre_validate_post_Link_url(channel):
    post = Post
    post.title = "x"
    post.description = "x"
    post.link_url = "https://www.test.com"
    post.image_url = "https://www.test.com"
    assert pre_validate_post(channel, post) == 1
    post.link_url = "test error link"
    assert pre_validate_post(channel, post) == 0
    post.link_url = ""
    assert pre_validate_post(channel, post) == 1

def pre_validate_post_img_url(channel):
    post = Post
    post.title = "x"
    post.description = "x"
    post.link_url = "https://www.test.com"
    post.image_url = "https://www.test.com"
    assert pre_validate_post(channel, post) == 1
    post.image_url = "test error link"
    assert pre_validate_post(channel, post) == 0
    post.image_url = ""
    assert pre_validate_post(channel, post) == 1

