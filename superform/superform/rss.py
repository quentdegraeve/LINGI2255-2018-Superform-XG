from flask import Blueprint, url_for, request, redirect, render_template, send_file
from superform.utils import datetime_converter, str_converter
from superform.models import db, Publishing, Channel, Rss
import io


rss_page = Blueprint('rss', __name__)


@rss_page.route('/rss/<int:id>.xml', methods=["GET"])
def display_rss_feed(id):

    RSSdb = db.session.query(Rss).filter(Rss.channel_id == id).first()

    feed = bytearray(RSSdb.xml_file, 'utf-8')

    return send_file(io.BytesIO(feed))
    #strIO = io.StringIO()
    #strIO.write(str(RSSdb.xml_file))
    #strIO.seek(0)
    #return send_file(strIO,
     #                attachment_filename="testing.xml",
      #               as_attachment=True)

    #return send_file(RSSdb.xml_file)
        #render_template('rss.html', xml=RSSdb.xml_file)



