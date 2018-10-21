from flask import current_app
from flask_oauthlib.client import OAuth

#Client_id =861s90686z5fuz
#Client_secret=xHDD886NZNkWVuN4
def run(publishing,channel_config):
    oauth = OAuth(current_app)
    #Config ici ou prendre dans param?
    remote = oauth.remote_app(
        'dev',
        consumer_key='dev',
        consumer_secret='dev',
        request_token_params={'scope': 'email'},
        base_url='http://127.0.0.1:5000/api/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='http://127.0.0.1:5000/oauth/token',
        authorize_url='http://127.0.0.1:5000/oauth/authorize'
    )
    print("Dans run linkedin")
    return;