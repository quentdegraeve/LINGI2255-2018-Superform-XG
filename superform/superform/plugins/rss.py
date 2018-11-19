from datetime import datetime, timedelta
from flask import flash, Blueprint, redirect, url_for, request
import json
from xml.sax import saxutils
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
        link=publishing.image_url,
        description=publishing.description,
        author="Superform", #channel_config['channel_author'],
        guid=Guid("https://www.cyberciti.biz/tips/my-10-unix-command-line-mistakes.html"),
        pubDate=publishing.date_from) #datetime(2017, 8, 1, 4, 0))

    feed = Feed(
        title="Superform",
        link=publishing.link_url, #channel_config['channel_location'],
        description="Posts", #channel_config['channel_decription'],
        language="en-US",
        lastBuildDate=datetime.now(),
        items=[item1])

    RSSdb = db.session.query(Rss).filter(Rss.channel_id == publishing.channel_id).first()
    if RSSdb is not None: # charge it and modify it
        output = StringIO()
        handler = saxutils.XMLGenerator(output, 'UTF-8')
        item1.publish(handler)
        handler.endElement("channel")
        handler.endElement("rss")
        handler.endDocument()
        generated_file = output.getvalue()

        existing = RSSdb.xml_file
        db.session.delete(RSSdb)
        rss = Rss(channel_id=publishing.channel_id, xml_file=generated_file)
        rss.xml_file = existing[0:-16]+rss.xml_file
        db.session.add(rss)
        publishing.state = 1
    else:
        generated_file = feed.rss()
        rss = Rss(channel_id=publishing.channel_id, xml_file=generated_file)
        db.session.add(rss)
        publishing.state = 1
    print(generated_file)

    db.session.commit()
