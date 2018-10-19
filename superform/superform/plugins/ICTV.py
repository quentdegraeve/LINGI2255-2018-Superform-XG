import json
import requests

FIELDS_UNAVAILABLE = ['Title', 'Description']
CONFIG_FIELDS = ['api_url', 'api_token']


def run(publishing, channel_config):

    # To do : Error management

    json_data = json.loads(channel_config)

    for field in CONFIG_FIELDS:
        if json_data.get(field) is None:
            print('Missing : {0}'.format(field))
            return

    try:
        response = requests.post(json_data.get("api_url"), data={
            'image_url': publishing.image_url,
            'token': json_data.get("api_token")
        })
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('Status code of the request : {0}'.format(response.status_code))
    except requests.exceptions.RequestException as e:
        print("Connection error")
