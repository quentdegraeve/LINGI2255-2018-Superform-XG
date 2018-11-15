import re
from superform.posts import pre_validate_post
from superform.models import Post


def post_pre_validation_plugins(post, maxLengthTitle, maxLengthDescription):
    pattern = '^(?:(?:https?|http?|wwww?):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$';
    if len(post.title) > maxLengthTitle or len(post.title) == 0: return 0
    if len(post.description) > maxLengthDescription or len(post.description) == 0: return 0
    if post.link_url is not None and post.link_url and len(post.link_url) > 0:
        if re.match(pattern, post.link_url, 0) is None: return 0
    if post.image_url is not None and len(post.image_url) > 0:
        if re.match(pattern, post.image_url, 0) is None: return 0
    return 1

def test_pre_validate_post_title(channel,maxLengthTitle):

    post = Post
    post.title = "x" * maxLengthTitle
    post.description = "x"
    post.link_url = "https://www.test.com"
    post.image_url ="https://www.test.com"
    assert pre_validate_post(channel, post) == 1
    post.title += "x"
    assert  pre_validate_post(channel,post) == 0
    post.title = ""
    assert  pre_validate_post(channel,post) == 0


def test_pre_validate_post_description(channel, maxLengthDescription):
    post = Post
    post.title = "x"
    post.description = "x" * maxLengthDescription
    post.link_url = "https://www.test.com"
    post.image_url = "https://www.test.com"
    assert  pre_validate_post(channel,post) == 1
    post.description += "x"
    assert  pre_validate_post(channel,post) == 0
    post.description = ""
    assert  pre_validate_post(channel,post) == 0

def test_pre_validate_post_Link_url(channel):
    post = Post
    post.title = "x"
    post.description = "x"
    post.link_url = "https://www.test.com"
    post.image_url = "https://www.test.com"
    assert  pre_validate_post(channel,post) == 1
    post.link_url = "test error link"
    assert  pre_validate_post(channel,post) == 0
    post.link_url = ""
    assert pre_validate_post(channel,post) == 1

def test_pre_validate_post_img_url(channel):
    post = Post
    post.title = "x"
    post.description = "x"
    post.link_url = "https://www.test.com"
    post.image_url = "https://www.test.com"
    assert  pre_validate_post(channel,post) == 1
    post.image_url = "test error link"
    assert  pre_validate_post(channel,post) == 0
    post.image_url = ""
    assert pre_validate_post(channel,post) == 1

