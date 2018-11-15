import json
import time
import re
from flask import redirect, url_for, request, Blueprint, flash
from linkedin import linkedin
from superform.suputils import selenium_utils
from datetime import datetime, timedelta

from superform.suputils.keepass import keypass_error_callback_page

from superform.models import db, Channel, Publishing
from superform.utils import get_module_full_name
from superform.suputils import keepass

linkedin_verify_callback_page = Blueprint('linkedin', 'channels')

FIELDS_UNAVAILABLE = []
AUTH_FIELDS = True

CONFIG_FIELDS = ["channel_name", "linkedin_access_token", "linkedin_token_expiration_date"]

API_KEY = keepass.get_password_from_keepass('linkedin_key')
API_SECRET = keepass.get_password_from_keepass('linkedin_secret')
RETURN_URL = keepass.get_username_from_keepass('linkedin_return_url')

authentication = linkedin.LinkedInAuthentication(
    API_KEY,
    API_SECRET,
    RETURN_URL,
    ['r_basicprofile', 'r_emailaddress', 'w_share', 'rw_company_admin']
)


def authenticate(channel_name, publishing_id):

    previous_token = LinkedinTokens.get_token(LinkedinTokens, channel_name)

    if previous_token.__getitem__(0) is None or (datetime.now() > previous_token.__getitem__(1)) :
        conf = dict()
        conf["channel_name"] = channel_name
        conf["publishing_id"] = publishing_id

        authentication.state = json.dumps(conf)
        print("authorization_url", authentication.authorization_url)
        return authentication.authorization_url  # open this url on your browser
    else:
        return 'AlreadyAuthenticated'


def set_access_token(channel_id, code):
    authentication.authorization_code = code

    print(authentication.authorization_code)
    result = authentication.get_access_token()

    print("Access Token:", result.access_token)
    print("Expires in (seconds):", result.expires_in)
    #Add
    channel = Channel.query.get(channel_id)
    channel_name = channel.name
    # add the configuration to the channel
    conf = dict()
    conf["channel_name"] = channel_name
    conf["linkedin_access_token"] = result.access_token
    conf["linkedin_token_expiration_date"] = (datetime.now() +timedelta(seconds=result.expires_in)).__str__()
    
    LinkedinTokens.put_token(LinkedinTokens, channel_name, conf)
    return conf


def share_post(channel_name, comment, title, submitted_url,submitted_image_url,visibility_code):

    token = LinkedinTokens.get_token(LinkedinTokens, channel_name).__getitem__(0)
    print('share_post token ', token)
    application = linkedin.LinkedInApplication(token=token)
    print('submitted_url', submitted_url)
    if submitted_url is '':
        submitted_url = None
    if submitted_image_url is '':
        submitted_image_url = None

    application.submit_share(comment=comment, title=title, submitted_url=submitted_url,
                             submitted_image_url=submitted_image_url, description="This is a sharing from Superform",visibility_code=visibility_code)
    return True


def auto_auth(url, channel_id):

    if keepass.set_entry_from_keepass(str(channel_id)) is 0:
        print('Error : cant get keepass entry :', str(channel_id), 'for linkedin plugin')
        return redirect(url_for('keepass.error_channel_keepass', chan_id=channel_id))

    driver = selenium_utils.get_chrome()

    driver.get(url)
    username = driver.find_element_by_name("session_key")
    password = driver.find_element_by_name("session_password")

    username.send_keys(keepass.KeepassEntry.username)
    password.send_keys(keepass.KeepassEntry.password)

    driver.find_element_by_name("signin").click()

    if not selenium_utils.wait_redirect(driver, 'linkedin'):
        driver.close()
        return redirect(url_for('keepass.error_channel_keepass', chan_id=channel_id))

    driver.close()
    return redirect(url_for('index'))


def run(publishing, channel_config):
    print("publishing Linkedin", publishing)
    print("channel-conf", type(channel_config), channel_config)
    print("conf run", channel_config, type(channel_config))
    conf = json.loads(channel_config)
    channel_name = conf['channel_name']
    authenticate(channel_name, (publishing.post_id, publishing.channel_id))

    if share_post(channel_name, publishing.description, publishing.title, publishing.link_url, publishing.image_url, "anyone"):
        publishing.state = 1
        db.session.commit()


def post_pre_validation(post):
    pattern = '^(?:(?:https?|http?|wwww?):\/\/)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/\S*)?$';
    if len(post.title) > 200 or len(post.title) == 0:
        return 0
    if len(post.description) > 256 or len(post.description) == 0:
        return 0
    if not(post.link_url is None or len(post.link_url) == 0):
         if( re.match(pattern,post.link_url,0) == None ):
             return 0;
    if not(post.image_url is None or len(post.image_url) == 0):
        if (re.match(pattern, post.image_url, 0) == None):
            return 0;
    print(" prevalidation linkedin is ok")
    return 1


class LinkedinTokens:

    def get_token(self, channel_name):

        channel = Channel.query.filter_by(name=channel_name, module=get_module_full_name("linkedin")).first()

        if channel and channel.config:
            print("put token", channel.config)
            conf = json.loads(channel.config)
            date_string = conf.get("linkedin_token_expiration_date")

            if date_string == "None" or date_string is None:
                return (None, None)

            date_expiration = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
            print("date_expiration", conf.get("linkedin_access_token"), date_expiration)
            return (conf.get("linkedin_access_token"), date_expiration)

        return (None, None)

    def put_token(self, channel_name, config_json):
        c = Channel.query.filter_by(name=channel_name, module=get_module_full_name("linkedin")).first()
        c.config = json.dumps(config_json)
        print("put token", config_json)
        db.session.commit()

@linkedin_verify_callback_page.route("/linkedin/verify", methods=['GET'])
def linkedin_verify_authorization():
    code = request.args.get('code')
    conf_publishing = json.loads(request.args.get('state'))
    channel_name = conf_publishing['channel_name']
    publishing_id = conf_publishing['publishing_id']
    post_id = publishing_id.__getitem__(0)
    channel_id = publishing_id.__getitem__(1)
    print("code", code)
    print("post id, channel id", post_id, channel_id)
    channel_config = {}
    if code:
        channel_config = set_access_token(channel_id,code)
    print("channel_config", channel_config)
    #normally should redirect to the channel page or to the page that publish a post
    publishing = Publishing.query.filter_by(post_id=post_id, channel_id=channel_id).first()
    print("init publishing", publishing)
    run(publishing, json.dumps(channel_config))
    return redirect(url_for('index'))
