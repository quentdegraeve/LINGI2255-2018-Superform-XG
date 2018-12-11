import json
import requests
import time;
from superform import db


FIELDS_UNAVAILABLE = ["link_url"]
CONFIG_FIELDS = ["server_url", "api_key","channel_id"]
AUTH_FIELDS = False
POST_FORM_VALIDATIONS = {}


def can_edit(publishing, channel_config):
    """
    Return true if a publishing can be edited
    :param publishing: an ictv publishing
    :param channel_config: the ictv channel configuration
    :return: TRUE if the publishing can be edited, FALSE otherwise
    """
    if publishing.state == 0:
        return True
    json_data = json.loads(channel_config)

    for field in CONFIG_FIELDS:
        if json_data.get(field) is None:
            print("Missing : {0}".format(field))
            return

    url = "http://" + json_data.get("server_url") + "/channels/" + json_data.get("channel_id") + "/api/capsules"
    header_get = {'accept': 'application/json', 'X-ICTV-editor-API-Key': json_data.get('api_key')}
    capsule_title = "Superform_post" + str(publishing.post_id) + ":" + publishing.title
    capsule_id = get_capsule_id(url, header_get, capsule_title)
    if capsule_id == -1:
        return False
    return True


def creates_a_capsule(url,header,date_from,date_until,title):
    """
    Create a partial ictv capsule and send it to the server
    :param url: url to send the request to
    :param header: header of the request
    :param date_from: date after witch the capsule should be displayed
    :param date_until: date after witch the capsule should not be displayed anymore
    :param title: title of the capsule, should be of the format Superform_post[post_id]:[any text you want here]
    :return: response of the server after the capsule creation
    """
    date_until=str(date_until)
    date_from=str(date_from)
    val_until=int(time.mktime(time.strptime(date_until,'%Y-%m-%d %H:%M:%S'))) - time.timezone
    val_from = int(time.mktime(time.strptime(date_from, '%Y-%m-%d %H:%M:%S'))) - time.timezone
    partial_capsules = json.dumps({"name": title, "theme": "ictv", "validity": [val_from,val_until]})
    return requests.post(url, data=partial_capsules, headers=header)


def create_a_slide(duration, template, title, subtitle, text, logo, image):
    """
    Create an ictv slide to be inserted into an ictv capsule
    :param duration: the duration in second the slide should be displayed on screen, -1 for default channel duration
    :param template: the template the slide should use
    :param title: the title of the slide
    :param subtitle: the subtitle of the slide
    :param text: the body of the slide
    :param logo: a link to a logo image
    :param image: a link to an image
    :return: a dict containing the slide
    """
    content = dict()
    content["title-1"] = {"text": title}
    content["subtitle-1"] = {"text": subtitle}
    content["text-1"] = {"text": text}
    if logo is not "":
        content["logo-1"] = {"src": logo}
    if image is not "":
        content["image-1"] = {"src": image}
    partial_slide = {"duration": duration, "template": template, "content": content}
    return partial_slide


def delete(publishing, channel_config):
    """
    Delete a publishing form the ictv server
    :param publishing: the publishing to be deleted
    :param channel_config: the channel configuration
    :return: nothing
    """

    json_data = json.loads(channel_config)

    for field in CONFIG_FIELDS:
        if json_data.get(field) is None:
            print("Missing : {0}".format(field))
            return

    url = "http://" + json_data.get("server_url") + "/channels/" + json_data.get("channel_id") + "/api/capsules"
    header_get = {'accept': 'application/json', 'X-ICTV-editor-API-Key': json_data.get('api_key')}
    header_delete = {'accept': 'application/json','Content-Type': 'application/json', 'X-ICTV-editor-API-Key': json_data.get('api_key')}
    capsule_title = "Superform_post" + str(publishing.post_id) + ":" + publishing.title
    capsule_id = get_capsule_id(url, header_get, capsule_title)
    if capsule_id == -1:
        return
    requests.delete(url + "/" + str(capsule_id), headers=header_delete)


def edit(publishing, channel_config):
    """
    Edit a publishing on the ictv server
    :param publishing: the publishing to be edited
    :param channel_config: the channel configuration
    :return: nothing
    """

    json_data = json.loads(channel_config)

    for field in CONFIG_FIELDS:
        if json_data.get(field) is None:
            print("Missing : {0}".format(field))
            return

    url = "http://" + json_data.get("server_url") + "/channels/" + json_data.get("channel_id") + "/api/capsules"
    header_get = {'accept': 'application/json', 'X-ICTV-editor-API-Key': json_data.get('api_key')}
    header_patch = {'accept': 'application/json','Content-Type': 'application/json', 'X-ICTV-editor-API-Key': json_data.get('api_key')}
    capsule_title = "Superform_post" + str(publishing.post_id) + ":"
    capsule_id = get_capsule_id(url, header_get, capsule_title)
    if capsule_id == -1:
        return
    duration = int(publishing.duration)
    title = publishing.title
    subtitle = publishing.subtitle
    image_url = publishing.image_url
    date_until = publishing.date_until
    date_from = publishing.date_from
    text = publishing.description
    logo = publishing.logo

    date_until=str(date_until)
    date_from=str(date_from)
    val_until=int(time.mktime(time.strptime(date_until,'%Y-%m-%d %H:%M:%S'))) - time.timezone
    val_from = int(time.mktime(time.strptime(date_from, '%Y-%m-%d %H:%M:%S'))) - time.timezone
    partial_capsules = json.dumps({"name": capsule_title+title, "theme": "ictv", "validity": [val_from,val_until]})
    response = requests.patch(url + "/" + str(capsule_id), data=partial_capsules, headers=header_patch)
    if response.status_code != 204:
        print("HttpError_edit1: " + str(response.status_code))
        return
    template = template_selector(image_url)
    slide = create_a_slide(duration, template, title, subtitle, text, logo, image_url)
    slide_id = get_slide_id(url, header_get, capsule_id)
    print("slide_id :" + str(slide_id))
    response = requests.patch(url + "/" + str(capsule_id) + "/slides/" + str(slide_id), data=json.dumps(slide), headers=header_patch)
    if response.status_code != 204:
        print("HttpError_edit2: " + str(response.status_code))
        return


def get_capsule_id(url, header, capsule_title):
    """
    Return the capsule id associated with capsule_title
    :param url: url to send the request to
    :param header: header of the request
    :param capsule_title: the title or part of the title of the capsule we want the id from
    :return: the capsule id or -1 if no capsule were found/an error occurred
    """
    all_capsules = requests.get(url, headers=header)
    if all_capsules.status_code != 200:
        print("HttpError_get_capsule_id: " + all_capsules.status_code)
        return -1
    capsules = all_capsules.json()
    for elem in capsules:
        if capsule_title in elem.get("name"):
            return str(elem.get("id"))
    return -1


def get_slide_id(url, header, capsule_id):
    """
    Return the slide id of the first slide in the capsule given by capsule id
    :param url: the url to send the request to
    :param header: the header of the request
    :param capsule_id: the id of the capsule we want to retrieve the id of the first slide from
    :return: the id of the first slide in the capsule given by capsule id or -1 if an error occurred
    """
    all_capsules = requests.get(url, headers=header)
    if all_capsules.status_code != 200:
        print("HttpError_get_capsule_id: " + all_capsules.status_code)
        return -1
    capsules = all_capsules.json()
    for elem in capsules:
        if str(capsule_id) == str(elem.get("id")):
            return str(elem.get("slides")[0].get("id"))
    return -1


def run(publishing, channel_config):
    """
    Create or edit a capsule and a slide on the ictv server
    :param publishing: the publishing to be posted on the ictv server
    :param channel_config: the channel configuration
    :return: nothing
    """

    json_data = json.loads(channel_config)

    for field in CONFIG_FIELDS:
        if json_data.get(field) is None:
            print("Missing : {0}".format(field))
            return
    duration = int(publishing.duration)
    title = publishing.title
    subtitle = publishing.subtitle
    image_url = publishing.image_url
    date_until = publishing.date_until
    date_from = publishing.date_from
    text = publishing.description
    logo = publishing.logo
    url = "http://" + json_data.get("server_url") + "/channels/" + json_data.get("channel_id") + "/api/capsules"
    header_get = {'accept': 'application/json', 'X-ICTV-editor-API-Key': json_data.get('api_key')}
    header_post = {'accept': 'application/json','Content-Type': 'application/json', 'X-ICTV-editor-API-Key': json_data.get('api_key')}
    capsule_title = "Superform_post" + str(publishing.post_id) + ":" + title

    if get_capsule_id(url, header_get, "Superform_post" + str(publishing.post_id) + ":") != -1:
        edit(publishing, channel_config)
        publishing.state = 1
        db.session.commit()
        return

    try:
        full_capsule = creates_a_capsule(url,header_post,date_from,date_until,capsule_title)
        if full_capsule.status_code != 201:
            print("HttpError_run1: " + str(full_capsule.status_code))
            return
        capsule_id = get_capsule_id(url,header_get,capsule_title)
        if capsule_id == -1:
            return
        template = template_selector(image_url)
        slide = create_a_slide(duration, template, title, subtitle, text, logo, image_url)
        slide_url = str(url + "/" + capsule_id + "/slides")
        completed_capsule = requests.post(slide_url, headers=header_post, data=json.dumps(slide))
        if completed_capsule.status_code != 201:
            print("HttpError_run2: " + str(completed_capsule.status_code))
            delete(publishing, channel_config)
            return
    except requests.exceptions.HTTPError as e:
        print(e)
    except requests.exceptions.RequestException as e:
        print("Connection error :\n")
        print(e)
    publishing.state = 1
    db.session.commit()


def template_selector(image):
    """
    Return the appropriate template to use
    :param image: a link to an image
    :return: the template to use
    """
    if image is '':
        return "template-text-center"
    return "template-text-image"


# Methods from other groups :

def post_pre_validation(post):
    return 1;


def authenticate(channel_name, publishing_id):
    return 'AlreadyAuthenticated'
