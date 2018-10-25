from linkedin import linkedin


API_KEY = '861s90686z5fuz'
API_SECRET = 'xHDD886NZNkWVuN4'
RETURN_URL = 'http://localhost:5000'


def testAuthentification():

    authentication = linkedin.LinkedInAuthentication(
        API_KEY,
        API_SECRET,
        RETURN_URL,
        ['r_basicprofile', 'r_emailaddress', 'w_share', 'rw_company_admin']
    )

    # Optionally one can send custom "state" value that will be returned from OAuth server
    # It can be used to track your user state or something else (it's up to you)
    # Be aware that this value is sent to OAuth server AS IS - make sure to encode or hash it
    # authorization.state = 'your_encoded_message'

    print(authentication.authorization_url)  # open this url on your browser

    authentication.authorization_code = 'AQQzhS4qza4ycMCjNoSSch4RTtMqk3nS1tTK9I7CeYeD8AX5qAZx4yPO__rH_dHygNIgmaffd1S-oXtdyAWlJpOdw8StL1gA64Gtp0DPJDRRNak7FznBpBKNumxp2KGx9G6PXKQLs535nT1ZLUsoDjmaEMuJXsqGt5rv4LZJ7wk8cgy3UOCcWuKNSO2tAA&state=0b3762e79ca305a75ee3d44a098a58a6'
    result = authentication.get_access_token()

    print("Access Token:", result.access_token)
    print("Expires in (seconds):", result.expires_in)
