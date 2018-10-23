import smtplib

from flask import current_app
import json

FIELDS_UNAVAILABLE = []

CONFIG_FIELDS = ["email","password"]

def run(publishing,channel_config):
    json_data = json.loads(channel_config)
    sender = json_data['sender']
    receivers = json_data['receiver']


    try:
        smtpObj = smtplib.SMTP(current_app.config["SMTP_HOST"],current_app.config["SMTP_PORT"])
        if current_app.config["SMTP_STARTTLS"]:
            smtpObj.starttls()
        text = msg.as_string()
        smtpObj.sendmail(sender, receivers, text)
        smtpObj.quit()
    except Exception as e:
        #TODO should add log here
        print(e)