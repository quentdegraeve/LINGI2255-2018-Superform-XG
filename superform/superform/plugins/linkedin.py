from linkedin import linkedin
from superform import utils
from flask import redirect
import json

FIELDS_UNAVAILABLE = []

CONFIG_FIELDS = ["profile_email", "channel_name"]

API_KEY = '861s90686z5fuz'
API_SECRET = 'xHDD886NZNkWVuN4'
RETURN_URL = 'http://localhost:5000/linkedin/verify'

authentication = linkedin.LinkedInAuthentication(
    API_KEY,
    API_SECRET,
    RETURN_URL,
    ['r_basicprofile', 'r_emailaddress', 'w_share', 'rw_company_admin']
)


def authenticate(channel_name, publishing_id):
    previous_token = LinkedinTokens.get_token(LinkedinTokens, channel_name)
    print("previoustoken ", str(previous_token))
    print("channel ",channel_name)

    if previous_token is None or previous_token.expires_in <= 0:
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
    LinkedinTokens.put_token(LinkedinTokens, channel_name, result)


def share_post(channel_name,comment,submitted_url,submitted_image_url,visibility_code):
    token = LinkedinTokens.get_token(LinkedinTokens, channel_name)
    print(' share_post token ', token)
    application = linkedin.LinkedInApplication(token=token.access_token)

    application.submit_share(comment=comment, title="Sharing from Superform", submitted_url=submitted_url,
                             submitted_image_url=submitted_image_url, description="This is a sharing from Superform",visibility_code=visibility_code)


def run(publishing,channel_config):
    print("publishing Linkedin", publishing)
    print("channel-conf", type(channel_config), channel_config)
    conf = json.loads(channel_config)
    print("conf run", conf, type(conf))
    channel_name = conf['channel_name']
    authenticate(channel_name, (publishing.post_id, publishing.channel_id))
    share_post(channel_name, publishing.description, publishing.link_url, publishing.image_url, "anyone")


class LinkedinTokens:
    tokens = {}

    def get_token(self, channel):
        if channel in self.tokens:
            return self.tokens[channel]
        return None

    def put_token(self, channel, token):
        self.tokens[channel] = token