import smtplib
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
    template['start'] = {'dateTime': '2018-10-25T09:00:00', 'timeZone': 'Europe/Brussels'}
    template['end'] = {'dateTime': '2018-10-25T17:00:00', 'timeZone': 'Europe/Brussels'}
    try:
        event = service.events().insert(calendarId='primary', body=template).execute()
    except Exception as e:
        #TODO should add log here
        print(e)