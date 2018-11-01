import json
import time
import platform
import os
import sys
from datetime import datetime, timedelta
from flask import redirect, url_for
from linkedin import linkedin
from selenium import webdriver, common

from superform.models import db, Channel
from superform.utils import get_module_full_name
from suputils import keepass

FIELDS_UNAVAILABLE = []

CONFIG_FIELDS = ["profile_email", "channel_name"]

API_KEY = keepass.get_password_from_keepass('superform_key')
API_SECRET = keepass.get_password_from_keepass('superform_secret')
RETURN_URL = 'http://localhost:5000/linkedin/verify'

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


def set_access_token(channel_name, code):
    authentication.authorization_code = code

    print(authentication.authorization_code)
    result = authentication.get_access_token()

    print("Access Token:", result.access_token)
    print("Expires in (seconds):", result.expires_in)
    LinkedinTokens.put_token(LinkedinTokens, channel_name, result.access_token, (datetime.now() +timedelta(seconds=result.expires_in)))


def share_post(channel_name, comment, title, submitted_url,submitted_image_url,visibility_code):

    token = LinkedinTokens.get_token(LinkedinTokens, channel_name).__getitem__(0)
    print(' share_post token ', token)
    application = linkedin.LinkedInApplication(token=token)
    print('submitted_url', submitted_url)
    if submitted_url is '':
        submitted_url = None
    if submitted_image_url is '':
        submitted_image_url = None

    application.submit_share(comment=comment, title=title, submitted_url=submitted_url,
                             submitted_image_url=submitted_image_url, description="This is a sharing from Superform",visibility_code=visibility_code)


def auto_auth(url, channel_id):
    if keepass.set_entry_from_keepass(str(channel_id)) is 0:
        return redirect(url_for('error_keepass'))
    dir_path = os.path.dirname(os.path.realpath(__file__))

    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    chrome = 'chromedriver'
    if platform.system() == 'Windows':
        chrome += '.exe'

    try:
        driver = webdriver.Chrome(dir_path + '\chrome\\' + chrome, chrome_options=options)
    except common.exceptions.WebDriverException:
        sys.exit('Can not find a valid chrome driver. it should be named cheromedriver on linux or cheromedriver.exe '
                 'on windows and it should be located in the plugins/chrome folder see this page for download : '
                 'https://sites.google.com/a/chromium.org/chromedriver/downloads')

    driver.get(url)
    username = driver.find_element_by_name("session_key")
    password = driver.find_element_by_name("session_password")

    username.send_keys(keepass.KeepassEntry.username)
    password.send_keys(keepass.KeepassEntry.password)

    driver.find_element_by_name("signin").click()

    while 'linkedin' in driver.current_url:
        time.sleep(.50)
    driver.close()
    return redirect(url_for('index'))


def run(publishing,channel_config):
    print("publishing Linkedin", publishing)
    print("channel-conf", type(channel_config), channel_config)
    conf = json.loads(channel_config)
    print("conf run", conf, type(conf))
    channel_name = conf['channel_name']
    authenticate(channel_name, (publishing.post_id, publishing.channel_id))
    share_post(channel_name, publishing.description, publishing.title, publishing.link_url, publishing.image_url, "anyone")


class LinkedinTokens:
    tokens = {}

    def get_token(self, channel_name):

        channel = Channel.query.filter_by(name=channel_name, module=get_module_full_name("linkedin")).first()

        if channel :
            return (channel.linkedin_access_token, channel.linkedin_token_expiration_date)

        return (None, None)

    def put_token(self, channel_name, token,expiration_date):

        c = Channel.query.filter_by(name=channel_name, module=get_module_full_name("linkedin")).first()
        c.linkedin_access_token = token
        c.linkedin_token_expiration_date = expiration_date
        db.session.commit()

