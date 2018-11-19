from datetime import datetime, timedelta
from flask import flash, Blueprint, redirect, url_for, request
import json
from superform.models import Publishing, db, Rss
from superform.suputils import selenium_utils, plugin_utils
from rfeed import *

FIELDS_UNAVAILABLE = ['Publication Date']
CONFIG_FIELDS = ["channel_title", "channel_decription", "channel_location", "channel_author"]
POST_FORM_VALIDATIONS = {
    'title_max_length': 40000,
    'description_max_length': 40000,
    'image_type': 'url'
}

slack_error_callback_page = Blueprint('slack_error', 'channels')
slack_verify_callback_page = Blueprint('slack', 'channels')


def post_pre_validation(post):
    return plugin_utils.post_pre_validation_plugins(post, 40000, 40000)

def authenticate(channel_id, publishing_id):
    return 'AlreadyAuthenticated'

def run(publishing, channel_config):
    print(channel_config)
    item1 = Item(
        title=publishing.title,
        link=publishing.link_url,
        description=publishing.description,
        author="Superform", #channel_config['channel_author'],
        guid=Guid("https://www.cyberciti.biz/tips/my-10-unix-command-line-mistakes.html"),
        pubDate=publishing.date_from) #datetime(2017, 8, 1, 4, 0))

    feed = Feed(
        title="nixCraft Updated Tutorials/Posts",
        link="www.goog", #channel_config['channel_location'],
        description="descripto", #channel_config['channel_decription'],
        language="en-US",
        lastBuildDate=datetime.now(),
        items=[item1])

    generated_file = feed.rss()

    rss = Rss(channel_id="16", xml_file=generated_file)
    db.session.add(rss)

    print(generated_file)

    publishing.state = 1
    db.session.commit()
