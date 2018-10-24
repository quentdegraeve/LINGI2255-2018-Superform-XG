from linkedin import linkedin
from superform import utils

FIELDS_UNAVAILABLE = []

CONFIG_FIELDS = ["profile_email"]

API_KEY = '861s90686z5fuz'
API_SECRET = 'xHDD886NZNkWVuN4'
RETURN_URL = 'http://localhost:5000/linkedin/verify'

authentication = linkedin.LinkedInAuthentication(
    API_KEY,
    API_SECRET,
    RETURN_URL,
    ['r_basicprofile', 'r_emailaddress', 'w_share', 'rw_company_admin']
)


def authenticate(channel_name):
    previous_token = LinkedinTokens.get_token(LinkedinTokens, channel_name)
    print("previoustoken ", str(previous_token))
    if previous_token == None or previous_token.expires_in <= 0:
        authentication.state = channel_name
        return authentication.authorization_url  # open this url on your browser
    else:
        return "alreadyAuthenticated"


def setAccessToken(channel_name, code):
    authentication.authorization_code = code

    print(authentication.authorization_code)
    result = authentication.get_access_token()

    print("Access Token:", result.access_token)
    print("Expires in (seconds):", result.expires_in)
    LinkedinTokens.put_token(LinkedinTokens, channel_name, result)

    application = linkedin.LinkedInApplication(token=result.access_token)
    profile_email = application.get_profile(selectors=['email-address']);
    print(profile_email.get("emailAddress"))
    return profile_email.get("emailAddress")



def Share_post(channel_name,comment,title,submitted_url,submitted_image_url,description,visibility_code):

    token = LinkedinTokens.get_token(LinkedinTokens, channel_name);

    application = linkedin.LinkedInApplication(token=token)

    application.submit_share(comment=comment, title=title, submitted_url=submitted_url,
                             submitted_image_url=submitted_image_url, description=description,visibility_code=visibility_code)

#Client_id =861s90686z5fuz
#Client_secret=xHDD886NZNkWVuN4


def run(publishing,channel_config):
    """
    authentication = linkedin.LinkedInDeveloperAuthentication(
        "861s90686z5fuz", #CONSUMER_KEY
        "xHDD886NZNkWVuN4", #CONSUMER_SECRET
        "test, "#USER_TOKEN
        "pass?", #USER_SECRET
        "return url?", #RETURN_URL
        linkedin.PERMISSIONS.enums.values()
    )
    """
    previous_token = LinkedinTokens.get_token(LinkedinTokens, "Test2")
    print("previoustoken ", str(previous_token))
    print("utils ", utils.get_config("LinkedinSection", "authorization_code"))
    if previous_token == None or previous_token.expires_in <= 0:
        setAccessToken(utils.get_config("LinkedinSection", "authorization_code"))
        #authentication.authorization_code = utils.get_config("LinkedinSection", "authorization_code")
    #application = linkedin.LinkedInApplication(token.access_token)
    print("enum" + str(linkedin.PERMISSIONS.enums.values()))
    #print("Dans run linkedin", token)
    return



class LinkedinTokens:
    tokens = {}

    def get_token(self, channel):
        if channel in self.tokens:
            return self.tokens[channel]
        return None

    def put_token(self, channel, token):
        self.tokens[channel] = token