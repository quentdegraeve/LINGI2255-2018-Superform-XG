import os
from slackclient import SlackClient
import webbrowser

from superform import db, Channel
from datetime import datetime, timedelta
from flask import current_app
import json
from superform.utils import get_module_full_name


# https://testlingi2255team8.slack.com/oauth/474267347719.dd54c0ce528d262ea8362fa1213db37ab4fa3aedb3940096389a6df65011ae40
# code=469959460081.474267347719.1754a91ee3f17336b5b237f869f6a8bd8fe235a4790258034c7b41bb72f83c6f
# https://testlingi2255team8.slack.com/api/oauth.access?client_id=469959460081.474308725254&client_secret=82014fbbb03ddff0cde2e0e93b20f64d&code=469959460081.474267347719.1754a91ee3f17336b5b237f869f6a8bd8fe235a4790258034c7b41bb72f83c6f


# doc pour authentification : https://api.slack.com/docs/oauth

#link_authorize = "https://slack.com/oauth/authorize"
#webbrowser.open(link_authorize)

# slack_token = os.environ["SLACK_API_TOKEN"] # dans var d env

CONFIG_FIELDS = ["user_id", "team_slack_name", "slack_token"]


app_id = "ADY92MB7G"
client_id ="469959460081.474308725254"
client_secret = "82014fbbb03ddff0cde2e0e93b20f64d"


slack_token = "xoxp-469959460081-470566021026-469830078256-0fe9a739c9d02ffeaaed820bc885756e"

sc = SlackClient(slack_token)

channel="CDUNHNL85"
text="Hello from Python! :tada: TEST TEST XS"
as_user="raphael.hacha"

def run(publishing,channel_config):
    print("publishing Slack", publishing)
    print("channel-conf", type(channel_config), channel_config)
    #print("conf run", channel_config, type(channel_config)
    #channel_name = channel_config['channel_name']
    #authenticate(channel_name, (publishing.post_id, publishing.channel_id))
    #share_post(


def share_post ( text , link_names , channel , as_user) :
    postMessage = "chat.postMessage"
    sc.api_call( postMessage , channel=channel, text=text, as_user=as_user , link_names=link_names)


share_post(text, "", channel, as_user)
