import json
import twitter

FIELDS_UNAVAILABLE = ['Title']
CONFIG_FIELDS = ['consumer_key', 'consumer_secret', 'access_token_key', 'access_token_secret']


def run(publishing, channel_config):

    # To do : Error management

    json_data = json.loads(channel_config)

    for field in CONFIG_FIELDS:
        if json_data.get(field) is None:
            print('Missing : {0}'.format(field))
            return

    api = twitter.Api(consumer_key=json_data.get('consumer_key'),
                      consumer_secret=json_data.get('consumer_secret'),
                      access_token_key=json_data.get('access_token_key'),
                      access_token_secret=json_data.get('access_token_secret'))

    description = publishing.description

    try:
        status = api.PostUpdate(description)
        print(status)
        print(status)
    except:
        print("Error during the authentification")
