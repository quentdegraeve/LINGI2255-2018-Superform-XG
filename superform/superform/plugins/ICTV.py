import json
import requests
import time;
from superform import db


FIELDS_UNAVAILABLE = ["link_url"]
CONFIG_FIELDS = ["server_url", "api_key","channel_id"]
AUTH_FIELDS = False
POST_FORM_VALIDATIONS = {}


def creates_a_capsule(url,header,date_from,date_until,title):
    date_until=str(date_until)
    date_from=str(date_from)
    val_until=int(time.mktime(time.strptime(date_until,'%Y-%m-%d %H:%M:%S'))) - time.timezone
    val_from = int(time.mktime(time.strptime(date_from, '%Y-%m-%d %H:%M:%S'))) - time.timezone
    partial_capsules = json.dumps({"name": title, "theme": "ictv", "validity": [val_from,val_until]})
    return requests.post(url, data=partial_capsules, headers=header)


def create_a_slide(duration, template, title, subtitle, text, logo, image, background):
    content = dict()
    if title is not None :
        content["title-1"] = {"text": title}
    else:
        content["title-1"] = {"text": ""}
    if subtitle is not None :
        content["subtitle-1"] = {"text": subtitle}
    else:
        content["subtitle-1"] = {"text": ""}
    if text is not None :
        content["text-1"] = {"text": text}
    else:
        content["text-1"] = {"text": ""}
    if logo is not None :
        content["logo-1"] = {"src": logo}
    if image is not None :
        content["image-1"] = {"src": image}
    if background is not None :
        content["background-1"] = {"src": background}

    partial_slide = {"duration": duration, "template": template, "content": content}
    return partial_slide


def get_capsule_id(url, header, capsule_title):
    all_capsules = requests.get(url, headers=header)
    if all_capsules.status_code != 200:
        print("HttpError: " + all_capsules.status_code)
        return -1
    capsules = all_capsules.json()
    for elem in capsules:
        if elem.get("name") == capsule_title:
            return str(elem.get("id"))


def run(publishing, channel_config):
    # To do : Error management

    json_data = json.loads(channel_config)

    for field in CONFIG_FIELDS:
        if json_data.get(field) is None:
            print("Missing : {0}".format(field))
            return

    duration = publishing.duration
    template = publishing.template
    title = publishing.title
    subtitle = publishing.subtitle
    image_url = publishing.image_url
    date_until = publishing.date_until
    date_from = publishing.date_from
    text = publishing.description
    logo = publishing.logo
    background = publishing.background
    url = "http://" + json_data.get("server_url") + "/channels/" + json_data.get("channel_id") + "/api/capsules"
    header_get = {'accept': 'application/json', 'X-ICTV-editor-API-Key': json_data.get('api_key')}
    header_post = {'accept': 'application/json','Content-Type': 'application/json', 'X-ICTV-editor-API-Key': json_data.get('api_key')}
    capsule_title = "Superform_post" + str(publishing.post_id) + ":" + title

    try:
        full_capsule = creates_a_capsule(url,header_post,date_from,date_until,capsule_title)
        if full_capsule.status_code != 201:
            print("HttpError: " + str(full_capsule.status_code))
            return
        capsule_id = get_capsule_id(url,header_get,capsule_title)
        if capsule_id == -1:
            return
        slide = create_a_slide(duration, template, title, subtitle, text, logo, image_url, background)
        slide_url = str(url + "/" + capsule_id + "/slides")
        completed_capsule = requests.post(slide_url, headers=header_post, data=json.dumps(slide))
        if completed_capsule.status_code != 201:
            print("HttpError: " + str(completed_capsule.status_code))
            return
    except requests.exceptions.HTTPError as e:
        print(e)
    except requests.exceptions.RequestException as e:
        print("Connection error :\n")
        print(e)
    publishing.state = 1
    db.session.commit()

# Methods from other groups :

def post_pre_validation(post):
    return 1;

def authenticate(channel_name, publishing_id):
    return 'AlreadyAuthenticated'