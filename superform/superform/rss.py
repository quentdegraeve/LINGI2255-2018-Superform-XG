from flask import Blueprint, send_file
from superform.models import db, Rss
import io


rss_page = Blueprint('rss', __name__)


@rss_page.route('/rss/<int:id>.xml', methods=["GET"])
def display_rss_feed(id):

    RSSdb = db.session.query(Rss).filter(Rss.channel_id == id).first()
    feed = RSSdb.xml_file

    proxy = io.StringIO()
    proxy.write(feed)

    mem = io.BytesIO()
    mem.write(proxy.getvalue().encode('utf-8'))

    mem.seek(0)
    proxy.close()

    return send_file(
        mem,
        as_attachment=True,
        attachment_filename='feed.xml',
        mimetype='text/xml'
    )