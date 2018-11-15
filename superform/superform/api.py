from flask import Blueprint, jsonify, request
from superform.utils import login_required
from superform.models import db, User, Channel
from superform.plugins.twitter import tweet_split

api_page = Blueprint('api', __name__)

@api_page.route('/api/search', methods=["GET"])
@login_required()
def search():

    name = request.args.get("name")

    if len(name) == 0:
        return jsonify()

    query = db.session.query(User).filter(User.id.like("{0}%".format(name)))
    users = query.limit(5).all()
    data = []

    for user in users:
        data.append({
            "id": user.id,
            "name": user.name,
            "first_name": user.first_name
        })

    return jsonify(data)


@api_page.route('/api/get_split', methods=["GET"])
@login_required()
def get_split(): # how to make a post ?
    print('here')
    form = request.args.get("form")
    for elem in form:
        if elem.startswith("chan_option_"):
            def substr(elem):
                import re
                return re.sub('^chan\_option\_', '', elem)

            c = Channel.query.get(substr(elem))
            chan = str(c.name)

            descr = form.get(chan + '_descriptionpost')
            print(descr)

    tweets = tweet_split(descr, (',', '!', '?', ':', ';', '\n'))
    return jsonify(
        tweetpreview=tweets
    )
