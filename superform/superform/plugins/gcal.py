import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from superform.suputils import plugin_utils
from superform.models import db, Publishing, Channel
from flask import current_app
import json

SCOPES = 'https://www.googleapis.com/auth/calendar'
FIELDS_UNAVAILABLE = []

CONFIG_FIELDS = ['token']

def run(gcal_publishing,channel_config):

    data = json.loads(channel_config)
    token = data['token']

    #token = {"access_token": "ya29.GlxFBgl-MEOI2NojpWSffhjjcfLPhIT55MNauXbQGD4JZQttj45NUKTtaGEd6GpA1GqRUAAhcDYNnK6s7Dyxpx_50N0EPGiKZJrUcPujhrx2eFaRHO94nGrVDpOlVg", "client_id": "408596117278-fkeuv3g0rdkrdpqsch2i1u18h0lgsakm.apps.googleusercontent.com", "client_secret": "EEZoDYXiIq3q-6zoSUrl9ec8", "refresh_token": "1/OEYHMvVkUmfS9C_CVqYccME6zKCANhB_YcU3SwzA2I3VjsBTr4ecnN1CqSchdDXs", "token_expiry": "2018-10-29T17:15:53Z", "token_uri": "https://www.googleapis.com/oauth2/v3/token", "user_agent": None, "revoke_uri": "https://oauth2.googleapis.com/revoke", "id_token": None, "id_token_jwt": None, "token_response": {"access_token": "ya29.GlxFBgl-MEOI2NojpWSffhjjcfLPhIT55MNauXbQGD4JZQttj45NUKTtaGEd6GpA1GqRUAAhcDYNnK6s7Dyxpx_50N0EPGiKZJrUcPujhrx2eFaRHO94nGrVDpOlVg", "expires_in": 3600, "scope": "https://www.googleapis.com/auth/calendar", "token_type": "Bearer"}, "scopes": ["https://www.googleapis.com/auth/calendar"], "token_info_uri": "https://oauth2.googleapis.com/tokeninfo", "invalid": False, "_class": "OAuth2Credentials", "_module": "oauth2client.client"}
    credentials = None
    try:
        credentials = client.Credentials.new_from_json(json.dumps(token))
    except ValueError:
        pass
    service = build('calendar', 'v3', http=credentials.authorize(Http()))
    template = {}
    template['summary'] = gcal_publishing.title
    template['location'] = gcal_publishing.location
    template['description'] = gcal_publishing.description
    template['start'] = {'dateTime': '{}-{}-{}T{}:00.000'.format(gcal_publishing.date_start.year, gcal_publishing.date_start.month, gcal_publishing.date_start.day,gcal_publishing.hour_start), 'timeZone': 'Europe/Brussels'}
    template['end'] = {'dateTime': '{}-{}-{}T{}:00.000'.format(gcal_publishing.date_end.year, gcal_publishing.date_end.month, gcal_publishing.date_end.day,gcal_publishing.hour_end), 'timeZone': 'Europe/Brussels'}
    template['colorId'] = gcal_publishing.color_id
    #if gcal_publishing.visibility:
    #    template['visibility'] = 'public'
    #else:
    #    template['visibility'] = 'private'
    template['attendees'] = gcal_publishing.guests
    #template['source'] = {"url": gcal_publishing.link_url, "title": 'link'}
    try:
        event = service.events().insert(calendarId='primary', body=template).execute()

        """
        Handling of the future deletion.
        It is put in comment for now to avoid errors, but should be tested
        """
        #gcal_publishing.misc['id'] = event.get('id')
        #db.session.commit()
    except Exception as e:
        #TODO should add log here
        print(e)

# this function add all extra fields inside a json file and return it.
def saveExtraFields(channel, form):
    fields = {}
    fields["date_start"] = form.get(channel + '_datedebut')
    fields["date_end"] = form.get(channel + '_datefin')
    fields["time_start"] = form.get(channel + '_heuredebut')
    fields["time_end"] = form.get(channel + '_heurefin')
    fields["location"] = form.get(channel + '_location')
    fields["color"] = form.get(channel + '_color')
    fields["visibility"] = form.get(channel + '_visibility')
    fields["availability"] = form.get(channel + '_availability')
    fields["guests"] = form.get(channel + '_guests')
    str = json.dumps(fields)
    return str

def post_pre_validation(post):
    return 1

def get_template_new():
    return 'gcal_form.html'

def get_template_mod():
    return 'filled_gcal_form.html'

# pas utile
def make_template_html():
    template = "<p>Starting Date<input type=\"date\" name=\"start_date\"</p>" \
               "<p>Ending Date<input type=\"date\" name=\"end_date\"></p>" \
               "<p>Starting hour<input type=\"time\" name=\"start_hour\"</p>" \
               "<p>Ending hour<input type=\"time\" name=\"end_hour\"</p>" \
               "<p>Location<input type=\"text\" name=\"location\"></p>" \
               "<p>Color<select name=\"color\">" \
               "<option value=\"tomato\">Tomato</option>" \
               "<option value=\"flamingo\">Flamingo</option>" \
               "<option value=\"tangerine\">Tangerine</option>"\
               "<option value=\"banana\">Banana</option>" \
               "<option value=\"sage\">Sage</option>" \
               "<option value=\"basil\">Basil</option>" \
               "<option value=\"peacock\">Peacock</option>"\
               "<option value=\"blueberry\">Blueberry</option>" \
               "<option value=\"lavender\" selected>Lavender</option>" \
               "<option value=\"grape\">Grape</option>" \
               "<option value=\"graphite\">Graphite</option>" \
               "</select></p>" \
               "<p>Visibility<select name=\"visibility\">" \
               "<option value=\"public\">Public</option>" \
               "<option value=\"private\" selected>Private</option>" \
               "</select></p>" \
               "<p>Availability<select name=\"availability\">" \
               "<option value=\"busy\" selected>Busy</option>" \
               "<option value=\"available\">available</option>" \
               "</select></p>"
    return template

def post_pre_validation(post):
    return plugin_utils.post_pre_validation_plugins(post, 40000, 40000)


def deletable():
    return True


#To make delete(pub) work, the 'pass' should be replaced by the code
#in comment beneath it.
def delete(pub):
    pass
"""
    c = db.session.query(Channel).filter(Channel.id == pub.channel_id).first()
    data = json.loads(c.config)
    token = data['token']
    credentials = None
    try:
        credentials = client.Credentials.new_from_json(json.dumps(token))
        service = build('calendar', 'v3', http=credentials.authorize(Http()))
        service.events().delete(calendarId='primary', eventId=pub.misc.get('id')).execute()
    except ValueError:
        pass
    except Exception as e:
        print(e)
"""
