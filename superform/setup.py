from setuptools import setup

setup(
    name='superform',
    packages=['superform'],
    include_package_data=True,
    install_requires=[
        'flask',
        'python3-saml',
        'sqlalchemy',
        'flask-sqlalchemy',
        'tweepy',
        'python3-linkedin',
        'pykeepass',
        'rfeed',
        'slackclient',
        'selenium',
        'pytest',
        'oauth2client',
        'google-api-python-client'
    ],
)