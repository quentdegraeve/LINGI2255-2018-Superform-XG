from linkedin import linkedin
from superform import db, Channel
from datetime import datetime, timedelta
import json
from superform.utils import get_module_full_name, get_config

FIELDS_UNAVAILABLE = []

CONFIG_FIELDS = ["profile_email", "channel_name", "linkedin_access_token", "linkedin_token_expiration_date"]

RETURN_URL = 'http://localhost:5000/linkedin/verify'

authentication = linkedin.LinkedInAuthentication(
    get_config("LinkedinSection", "API_KEY"),
    get_config("LinkedinSection", "API_SECRET"),
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

    #Add
    #channel = Channel.query.filter_by(name=channel_name, module=get_module_full_name("linkedin")).first()
    # add the configuration to the channel
    conf = dict()
    conf["profile_email"] = "" #Do api call to have the profile email
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


def run(publishing,channel_config):
    print("publishing Linkedin", publishing)
    print("channel-conf", type(channel_config), channel_config)
    print("conf run", channel_config, type(channel_config))
    channel_name = channel_config['channel_name']
    authenticate(channel_name, (publishing.post_id, publishing.channel_id))
    share_post(channel_name, publishing.description, publishing.title, publishing.link_url, publishing.image_url, "anyone")


class LinkedinTokens:

    def get_token(self, channel_name):

        channel = Channel.query.filter_by(name=channel_name, module=get_module_full_name("linkedin")).first()

        if channel and channel.config:
            print("put token", channel.config)
            conf = json.loads(channel.config)
            date_string = conf.get("linkedin_token_expiration_date")
            date_expiration = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
            print("date_expiration", conf.get("linkedin_access_token"), date_expiration)
            return (conf.get("linkedin_access_token"), date_expiration)

        return (None, None)

    def put_token(self, channel_name, config_json):
        c = Channel.query.filter_by(name=channel_name, module=get_module_full_name("linkedin")).first()
        c.config = json.dumps(config_json)
        print("put token", config_json)
        db.session.commit()
