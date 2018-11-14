from datetime import datetime, timedelta, time

from flask import flash, Blueprint, redirect, url_for, request, render_template
from slackclient import SlackClient
import json
from superform.models import Channel, Publishing, db
from superform.utils import get_module_full_name
from superform.suputils import keepass
from suputils import selenium_utils


FIELDS_UNAVAILABLE = ['Publication Date']
CONFIG_FIELDS = ["channel_name", "slack_channel_name", "slack_domain_name", "slack_access_token", "slack_token_expiration_date"]
AUTH_FIELDS = True

API_CLIENT_KEY = keepass.get_password_from_keepass('slack_client_key')
API_SECRET = keepass.get_password_from_keepass('slack_secret')
API_CLIENT_ID = keepass.get_password_from_keepass('slack_client_id')

slack_error_callback_page = Blueprint('slack_error', 'channels')
slack_verify_callback_page = Blueprint('slack', 'channels')

slackClient = SlackClient()


def authenticate(channel_name, publishing_id):
    previous_token = SlackTokens.get_token(SlackTokens, channel_name)

    if previous_token.__getitem__(0) is None or (datetime.now() > previous_token.__getitem__(1)):

        conf = dict()
        conf["channel_name"] = channel_name
        conf["publishing_id"] = publishing_id

        state = json.dumps(conf)
        return "https://slack.com/oauth/authorize?scope=identity.basic&client_id=" + API_CLIENT_ID + "&state=" + state  # open this url on your browser
    else:
        return 'AlreadyAuthenticated'


def set_access_token(channel_id, code):
    # An empty string is a valid token for this request
    sc = SlackClient("")

    # Request the auth tokens from Slack
    auth_response = sc.api_call(
        "oauth.access",
        client_id=API_CLIENT_ID,
        client_secret=API_SECRET,
        code=code
    )

    # Add
    channel = Channel.query.get(channel_id)
    channel_name = channel.name
    slack_channel_name = json.loads(channel.config).get("slack_channel_name")
    if (not slack_channel_name) or slack_channel_name is '':
        slack_channel_name = "general"

    # add the configuration to the channel
    conf = json.loads(channel.config)

    conf["channel_name"] = channel_name
    conf["slack_channel_name"] = slack_channel_name
    conf["slack_access_token"] = auth_response['access_token']
    conf["slack_token_expiration_date"] = (datetime.now() + timedelta(hours=24 * 365)).__str__()

    SlackTokens.put_token(SlackTokens, channel_name, conf)
    return conf


def auto_auth(url, channel_id):
    if keepass.set_entry_from_keepass(str(channel_id)) is 0:
        print('Error : cant get keepass entry :', str(channel_id), 'for slack plugin')
        return redirect(url_for('keepass.error_channel_keepass', chan_id=channel_id))

    conf = Channel.query.get(channel_id).config
    if not conf or conf == '{}':
        return redirect(url_for('slack_error.error_config_slack', chan_id=channel_id))

    dom = json.loads(conf)['slack_domain_name']

    if dom == 'None' or dom == '':
        return redirect(url_for('slack_error.error_config_slack', chan_id=channel_id))

    driver = selenium_utils.get_chrome()
    driver.get(url)
    domain = driver.find_element_by_name("domain")
    domain.send_keys(dom)
    driver.find_elements_by_css_selector('button[id="submit_team_domain"]')[0].click()

    if not selenium_utils.wait_redirect(driver, 'signin'):
        driver.close()
        return redirect(url_for('slack_error.error_config_slack', chan_id=channel_id))

    email = driver.find_element_by_name("email")
    password = driver.find_element_by_name("password")
    email.send_keys(keepass.KeepassEntry.username)
    password.send_keys(keepass.KeepassEntry.password)
    driver.find_elements_by_css_selector('button[id="signin_btn"]')[0].click()

    if not selenium_utils.wait_redirect_after(driver, 'testlingi2255team8.slack.com/oauth'):
        driver.close()
        return redirect(url_for('keepass.error_channel_keepass', chan_id=channel_id))

    driver.find_elements_by_css_selector('button[id="oauth_authorizify"]')[0].click()

    if not selenium_utils.wait_redirect(driver, 'testlingi2255team8.slack.com'):
        driver.close()
        return redirect(url_for('slack_error.error_config_slack', chan_id=channel_id))

    driver.close()
    return redirect(url_for('index'))


def share_post(channel_name, slack_channel_name, title, description, link, link_image):
    token = SlackTokens.get_token(SlackTokens, channel_name).__getitem__(0)

    if not slack_channel_name or slack_channel_name == 'None':
        slack_channel_name = "general"

    print('slack_channel_nam  ', slack_channel_name)
    sc = SlackClient(token)
    res = sc.api_call(
        "chat.postMessage",
        channel=slack_channel_name,
        attachments=[
            {
                "pretext": title,
                "title": link,
                "title_link": link,
                "image_url": link_image,
                "text": description
            }
        ]
    )
    print("res share post", res)
    if not res['ok']:
        print("Error", res["error"])
        flash("Error " + ' '.join(res["error"].split('_')))
        return False
    return True


def run(publishing, channel_config):
    channel_config = json.loads(channel_config);
    print("publishing slack", publishing)
    print("channel-conf", type(channel_config), channel_config)
    print("conf run", channel_config, type(channel_config))
    channel_name = channel_config['channel_name']
    slack_channel_name = channel_config['slack_channel_name']

    authenticate(channel_name, (publishing.post_id, publishing.channel_id))
    if share_post(channel_name, slack_channel_name, publishing.title, publishing.description, publishing.link_url,
                  publishing.image_url):
        publishing.state = 1
        db.session.commit()


@slack_verify_callback_page.route("/slack/verify", methods=['GET'])
def slack_verify_authorization():
    # Retrieve the auth code from the request params
    auth_code = request.args['code']
    conf_publishing = json.loads(request.args.get('state'))
    channel_name = conf_publishing['channel_name']
    publishing_id = conf_publishing['publishing_id']
    post_id = publishing_id.__getitem__(0)
    channel_id = publishing_id.__getitem__(1)
    print(auth_code)

    if auth_code:
        channel_config = set_access_token(channel_id, auth_code)

    print("channel_config", channel_config)
    # normally should redirect to the channel page or to the page that publish a post
    publishing = Publishing.query.filter_by(post_id=post_id, channel_id=channel_id).first()
    print("init publishing", publishing)
    run(publishing, json.dumps(channel_config))

    return redirect(url_for('index'))


class SlackTokens:

    def get_token(self, channel_name):

        print('channel_name', channel_name)

        channel = Channel.query.filter_by(name=channel_name, module=get_module_full_name("slack")).first()

        print('channel', channel)

        if channel and channel.config:
            print('channel.config', channel.config)
            conf = json.loads(channel.config)
            date_string = conf.get("slack_token_expiration_date")

            if not date_string or date_string is None or date_string == "None":
                return (None, None)

            date_expiration = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
            print("date_expiration", conf.get("slack_access_token"), date_expiration)
            return (conf.get("slack_access_token"), date_expiration)

        return (None, None)

    def put_token(self, channel_name, config_json):
        print("type config json : -> ", type(config_json))
        c = Channel.query.filter_by(name=channel_name, module=get_module_full_name("slack")).first()
        c.config = json.dumps(config_json)
        print("put token", config_json)
        db.session.commit()

    def post_pre_validation(post):
        if len(post.title) > 40000 or len(post.title) == 0: return 0;
        if len(post.description) > 40000 or len(post.description) == 0: return 0;
        return 1;


@slack_error_callback_page.route('/error_config_slack/<int:chan_id>')
def error_config_slack(chan_id):
    chan_name = Channel.query.get(chan_id).name
    return render_template('error_config_slack.html', channel=chan_name)
