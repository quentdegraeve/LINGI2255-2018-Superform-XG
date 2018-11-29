from flask import Flask, render_template, session
import pkgutil
import importlib
from flask import request

import superform.plugins
from superform.publishings import pub_page
from superform.models import db, Post, Publishing, Channel, State
from superform.authentication import authentication_page
from superform.authorizations import authorizations_page
from superform.channels import channels_page
from superform.posts import posts_page
from superform.api import api_page
from superform.edit import edit_page
from superform.suputils.keepass import keypass_error_callback_page
from superform.plugins.slack import slack_error_callback_page, slack_verify_callback_page
from superform.users import get_moderate_channels_for_user, is_moderator

from superform.plugins.linkedin import linkedin_verify_callback_page

app = Flask(__name__)
app.config.from_json("config.json")

# Register blueprints
app.register_blueprint(authentication_page)
app.register_blueprint(authorizations_page)
app.register_blueprint(channels_page)
app.register_blueprint(posts_page)
app.register_blueprint(pub_page)
app.register_blueprint(linkedin_verify_callback_page)
app.register_blueprint(keypass_error_callback_page)
app.register_blueprint(slack_error_callback_page)
app.register_blueprint(slack_verify_callback_page)
app.register_blueprint(api_page)
app.register_blueprint(edit_page)

# Init dbsx
db.init_app(app)

# List available channels in config
app.config["PLUGINS"] = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules(superform.plugins.__path__, superform.plugins.__name__ + ".")
}


@app.route('/', methods=["GET"])
def index():
    page = request.args.get("page")
    if page is None or not page.isnumeric():
        page = 1
    else:
        page = int(page)
    user_id = session.get("user_id", "") if session.get("logged_in", False) else -1
    posts = []
    pubs_unvalidated = []
    if user_id != -1:
        # AJOUTER Post.user_id == user_id dans posts DANS QUERY?
        posts = Post.query.order_by(Post.date_created.desc()).paginate(page, 5, error_out=False)
        for post in posts.items:
            publishings = db.session.query(Publishing).filter(Publishing.post_id == post.id).all()
            channels = []
            for publishing in publishings:
                channels.append(db.session.query(Channel).filter(Channel.id == publishing.channel_id).first())
            setattr(post, "channels", channels)

        posts_user = db.session.query(Post).filter(Post.user_id == user_id).all()
        print("posts_user", posts_user)
        pubs_unvalidated = db.session.query(Publishing).filter(Publishing.state == State.REFUSED.value).\
            order_by(Publishing.post_id).order_by(Publishing.channel_id).all()
        print('pubs_unv', pubs_unvalidated)
        post_ids = [p.id for p in posts_user]
        pubs = []

        for pub_unvalidated in pubs_unvalidated:
            if pub_unvalidated.post_id in post_ids:
                channels = [db.session.query(Channel).filter(Channel.id == publishing.channel_id).first()]
                setattr(pub_unvalidated, "channels", channels)
                pubs.append(pubs_unvalidated)
    return render_template("index.html", posts=posts, pubs_unvalidated=pubs_unvalidated)


@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403


@app.errorhandler(404)
def notfound(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
