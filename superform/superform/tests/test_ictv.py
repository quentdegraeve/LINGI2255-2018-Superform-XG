import pytest
from superform.plugins import ICTV

@pytest.fixture
def test_template_selector():
    template = ICTV.template_selector("")
    assert template == "template-text-center"
    template = ICTV.template_selector("www.animage.jpeg")
    assert template == "template-text-image"


def test_create_a_slide():
    slide = ICTV.create_a_slide(-1, "template-text-center", "A title", "a subtitle", "a text", "www.alogo.jpeg", "")
    assert slide.get("duration") == -1
    assert slide.get("template") == "template-text-center"
    assert slide.get("content").get("title-1").get("text") == "A title"
    assert slide.get("content").get("subtitle-1").get("text") == "a subtitle"
    assert slide.get("content").get("text-1").get("text") == "a text"
    assert slide.get("content").get("logo-1").get("src") == "www.alogo.jpeg"
    assert slide.get("content").get("image-1") is None
    slide = ICTV.create_a_slide(5, "template-text-center", "A title", "a subtitle", "a text", "", "www.animage.png")
    assert slide.get("duration") == 5
    assert slide.get("template") == "template-text-center"
    assert slide.get("content").get("title-1").get("text") == "A title"
    assert slide.get("content").get("subtitle-1").get("text") == "a subtitle"
    assert slide.get("content").get("text-1").get("text") == "a text"
    assert slide.get("content").get("image-1").get("src") == "www.animage.png"
    assert slide.get("content").get("logo-1") is None
