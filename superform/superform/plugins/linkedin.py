from linkedin import linkedin
from superform import utils


API_KEY = '861s90686z5fuz'
API_SECRET = 'xHDD886NZNkWVuN4'
RETURN_URL = 'http://localhost:5000/linkedin/verify'

authentication = linkedin.LinkedInAuthentication(
    API_KEY,
    API_SECRET,
    RETURN_URL,
    ['r_basicprofile', 'r_emailaddress', 'w_share', 'rw_company_admin']
)

application = None

def authenticate(channel_name):
    previous_token = Linkedin.get_token(Linkedin, "Test2")
    print("previoustoken ", str(previous_token))
    if previous_token == None or previous_token.expires_in <= 0:
        # Optionally one can send custom "state" value that will be returned from OAuth server
        # It can be used to track your user state or something else (it's up to you)
        # Be aware that this value is sent to OAuth server AS IS - make sure to encode or hash it
        # authorization.state = 'your_encoded_message'
        return authentication.authorization_url  # open this url on your browser
    else:
        initialiseLinkendinApp(previous_token.access_token)

def setAccessToken(code):
    authentication.authorization_code = code

    print(authentication.authorization_code)
    result = authentication.get_access_token()

    print("Access Token:", result.access_token)
    print("Expires in (seconds):", result.expires_in)
    initialiseLinkendinApp(result.access_token)
    Linkedin.put_token(Linkedin, "Test2", result)

def initialiseLinkendinApp(token):
    application = linkedin.LinkedInApplication(token=token)
    application.submit_share(comment='Test python comment', title='Test python title', submitted_url=None,
                             submitted_image_url=None, description="Test python description",visibility_code='anyone')

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
    previous_token = Linkedin.get_token(Linkedin, "Test2")
    print("previoustoken ", str(previous_token))
    print("utils ", utils.get_config("LinkedinSection", "authorization_code"))
    if previous_token == None or previous_token.expires_in <= 0:
        setAccessToken(utils.get_config("LinkedinSection", "authorization_code"))
        #authentication.authorization_code = utils.get_config("LinkedinSection", "authorization_code")
    #application = linkedin.LinkedInApplication(token.access_token)
    print("enum" + str(linkedin.PERMISSIONS.enums.values()))
    #print("Dans run linkedin", token)
    return


class Linkedin:
    tokens = {}

    def get_token(self, channel):
        if channel in self.tokens:
            return self.tokens[channel]
        return None

    def put_token(self, channel, token):
        self.tokens[channel] = token