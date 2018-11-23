import json
import os
import re

import requests
import tweepy


FIELDS_UNAVAILABLE = ["Title"]
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
    link_url = publishing.link_url
    text = publishing.description
    if link_url is not '':
        text = text + ' '
        text = text + link_url
    tweets = tweet_split(text, (',', '!', '?', ':', ';', '\n'))

    image_url = publishing.image_url
    if image_url is '':
        try:
            for tweet in reversed(tweets):
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

            i = len(tweets)-1
            while i > 0:
                api.update_status(status=tweets[i])
                i -= 1
            api.update_with_media(filename, status=tweets[0])
            os.remove(filename)
        else:
            print("Cant load the image")


def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)


def get_urls(text):
    pattern = r'((?:http[s]?:/{2})?(?:w{3}\.)?(?:\w+\.)+(?:com|fr|be|io|gov|net|tv|uk|ch|de|nl|lu)(?:/[^\s]+)?)'
    return re.findall(pattern, text)


def tweet_split(text, separators):
    my_str = text

    tweets = []
    limit = 280

    if len(text) <= limit:
        tweets += [text]
    else:
        limit -= 4
        urls = get_urls(text)
        url_index = []
        url_len = []
        for url in urls:
            url_index.append(text.find(url))
            url_len.append(len(url))

        for sep in separators:
            my_str = my_str.replace(sep, '.')

        sentences = my_str.split(".")
        index = 0  # index général dans text
        nbTweet = 0  # nombre de tweets
        count = 0  # taille du tweet actuel
        temp = ""  # tweet temporaire
        for s in sentences:
            if (len(s) + 1) > limit:
                if separators == ' ':
                    print("Split between characters")
                    return [text[i:i+280] for i in range(0, len(text), 280)]
                else:
                    print("Split between words")
                    return tweet_split(text, ' ')
            else:
                if not url_index:  # si pas d'url
                    if (count + len(s) + 1) < limit:  # tweet small enough
                        temp += text[index: index + len(s) + 1]
                        count += len(s) + 1
                        index += len(s) + 1
                    else:
                        tweets += [temp]
                        if text[index] == ' ':
                            temp = text[index + 1: index + len(s) + 1]
                            count = len(s)
                            index += len(s) + 1
                        else:
                            temp = text[index: index + len(s) + 1]
                            count = len(s) + 1
                            index += len(s) + 1
                        nbTweet += 1
                else:  # si url
                    for (i, l) in zip(url_index, url_len):
                        if (i <= index <= i + l) or (i <= index + len(s) + 1 <= i + l):  # url in this part
                            if limit - count <= l + i - index + 1:  # no room in this tweet to put entire url
                                temp += text[index: i]
                                tweets += [temp]
                                nbTweet += 1
                                index += len(s) + 1
                                temp = text[i: index]  # start of a new tweet
                                count = index - i
                            else:  # url can be put in full in this tweet
                                if len(s) > limit - count:  # full sentence can't be put in tweet
                                    temp += text[index: i + l]
                                    tweets += [temp]
                                    nbTweet += 1
                                    temp = text[i + l + 1: index + len(s) + 1]
                                    index += len(s) + 1
                                    count = index - i
                                else:
                                    temp += text[index: index + len(s) + 1]
                                    count += len(s) + 1
                                    index += len(s) + 1
                        else:  # url not in this part
                            if (count + len(s) + 1) < limit:  # tweet small enough to put a sentence
                                temp += text[index: index + len(s) + 1]
                                count += len(s) + 1
                                index += len(s) + 1
                            else:  # tweet too big
                                tweets += [temp]
                                if text[index] == ' ':
                                    temp = text[index + 1: index + len(s) + 1]
                                    count = len(s)
                                    index += len(s) + 1
                                else:
                                    temp = text[index: index + len(s) + 1]
                                    count = len(s) + 1
                                    index += len(s) + 1
                                nbTweet += 1

        tweets += [temp]

    if not len(tweets) == 1:
        for i in range(0, len(tweets)):
            tweets[i] = str(i + 1) + '/' + str(len(tweets)) + ' ' + tweets[i]

    return tweets

# Methods from other groups :

def post_pre_validation(post):
    return 1;

def authenticate(channel_name, publishing_id):
    return 'AlreadyAuthenticated'