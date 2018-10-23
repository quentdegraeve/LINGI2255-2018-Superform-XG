from linkedin import linkedin


API_KEY = '861s90686z5fuz'
API_SECRET = 'xHDD886NZNkWVuN4'
RETURN_URL = 'http://localhost:5000'

authentication = linkedin.LinkedInAuthentication(
    API_KEY,
    API_SECRET,
    RETURN_URL,
    ['r_basicprofile', 'r_emailaddress', 'w_share', 'rw_company_admin']
)

application = None

def authenticate():


    # Optionally one can send custom "state" value that will be returned from OAuth server
    # It can be used to track your user state or something else (it's up to you)
    # Be aware that this value is sent to OAuth server AS IS - make sure to encode or hash it
    # authorization.state = 'your_encoded_message'

    return authentication.authorization_url  # open this url on your browser


def setAccessToken(code):
    authentication.authorization_code = code

    print(authentication.authorization_code)
    result = authentication.get_access_token()

    print("Access Token:", result.access_token)
    print("Expires in (seconds):", result.expires_in)
    initialiseLinkendinApp(result.access_token)

def initialiseLinkendinApp(token):
    application = linkedin.LinkedInApplication(token='token')
    application.submit_share('Posting from the API using Python', 'A title for your share', None,
                             'https://www.linkedin.com', None,'anyone')
