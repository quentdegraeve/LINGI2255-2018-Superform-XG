import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from flask import current_app
import json

SCOPES = 'https://www.googleapis.com/auth/calendar'
FIELDS_UNAVAILABLE = []

CONFIG_FIELDS = ["token"]

def run(gcal_publishing,channel_config):
    json_data = json.loads(channel_config)
    token = json_data['token']

    credentials = None
    try:
        credentials = client.Credentials.new_from_json(token)
    except ValueError:
        pass
    service = build('calendar', 'v3', http=credentials.authorize(Http()))
    template = {}
    template['summary'] = gcal_publishing.title
    template['location'] = gcal_publishing.location
    template['description'] = gcal_publishing.description
    template['start'] = {'dateTime': '{}-{}-{}T{}:00:00'.format(gcal_publishing.date_start.year, gcal_publishing.date_start.month, gcal_publishing.date_start.day,gcal_publishing.hour_start.hour), 'timeZone': 'Europe/Brussels'}
    template['end'] = {'dateTime': '{}-{}-{}T{}:00:00'.format(gcal_publishing.date_end.year, gcal_publishing.date_end.month, gcal_publishing.date_end.day,gcal_publishing.hour_end.hour), 'timeZone': 'Europe/Brussels'}
    template['colorId'] = gcal_publishing.color_id
    template['visibility'] = gcal_publishing.visibility
    template['attendees'] = gcal_publishing.guests
    template['source'] = {"url": gcal_publishing.link_url, "title": 'link'}
    try:
        event = service.events().insert(calendarId='primary', body=template).execute()
    except Exception as e:
        #TODO should add log here
        print(e)