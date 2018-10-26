import json
import os

import requests
import tweepy

from separation import tweet_split

FIELDS_UNAVAILABLE = ['Title']
CONFIG_FIELDS = ["consumer_key", "consumer_secret", "access_token_key", "access_token_secret"]


def run(publishing, channel_config):

    # To do : Error management

    json_data = json.loads(channel_config)

    for field in CONFIG_FIELDS:
        if json_data.get(field) is None:
            print("Missing : {0}".format(field))
            return

    cfg = {
        "consumer_key": str(json_data['consumer_key']),
        "consumer_secret": str(json_data['consumer_secret']),
        "access_token": str(json_data['access_token_key']),
        "access_token_secret": str(json_data['access_token_secret'])
    }
    api = get_api(cfg)
    tweets = tweet_split(publishing.description, (',', '!', '?', ':', ';'))

    image_url = publishing.image_url
    if image_url is '':
        try:
            for tweet in tweets:
                api.update_status(status=tweet)
        except tweepy.TweepError as e:
            print(e.reason)
    else:
        filename = 'img.jpg'
        request = requests.get(image_url, stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for req in request:
                    image.write(req)

            for i in range(len(tweets)):
                if i == 0:
                    api.update_with_media(filename, status=tweets[i])
                else:
                    api.update_status(status=tweets[i])
            os.remove(filename)
        else:
            print("Cant load the image")



def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)



