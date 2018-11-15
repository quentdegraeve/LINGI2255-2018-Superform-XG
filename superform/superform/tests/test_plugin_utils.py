
from superform.suputils import plugin_utils
from superform import Post

def test_pre_validate_post_title():

    post = Post
    post.title = "x" * 200
    post.description = "x"
    post.link_url = "https://www.test.com"
    post.image_url ="https://www.test.com"
    assert plugin_utils.post_pre_validation_plugins(post,200,256) == 1
    post.title += "x"
    assert  plugin_utils.post_pre_validation_plugins(post,200,256) == 0
    post.title = ""
    assert  plugin_utils.post_pre_validation_plugins(post,200,256) == 0


def test_pre_validate_post_description():
    post = Post
    post.title = "x"
    post.description = "x" * 256
    post.link_url = "https://www.test.com"
    post.image_url = "https://www.test.com"
    assert  plugin_utils.post_pre_validation_plugins(post,200,256) == 1
    post.description += "x"
    assert  plugin_utils.post_pre_validation_plugins(post,200,256) == 0
    post.description = ""
    assert  plugin_utils.post_pre_validation_plugins(post,200,256) == 0

def test_pre_validate_post_Link_url():
    post = Post
    post.title = "x"
    post.description = "x"
    post.link_url = "https://www.test.com"
    post.image_url = "https://www.test.com"
    assert  plugin_utils.post_pre_validation_plugins(post,200,256) == 1
    post.link_url = "test error link"
    assert  plugin_utils.post_pre_validation_plugins(post,200,256) == 0
    post.link_url = ""
    assert plugin_utils.post_pre_validation_plugins(post, 200, 256) == 1

def test_pre_validate_post_img_url():
    post = Post
    post.title = "x"
    post.description = "x"
    post.link_url = "https://www.test.com"
    post.image_url = "https://www.test.com"
    assert  plugin_utils.post_pre_validation_plugins(post,200,256) == 1
    post.image_url = "test error link"
    assert  plugin_utils.post_pre_validation_plugins(post,200,256) == 0
    post.link_url = ""
    assert plugin_utils.post_pre_validation_plugins(post, 200, 256) == 1

