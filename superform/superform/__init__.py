from flask import Flask, render_template, session,url_for, redirect
import pkgutil
import importlib
from flask import request

import superform.plugins
from superform.publishings import pub_page
from superform.models import db, User, Post,Publishing,Channel
from superform.authentication import authentication_page
from superform.authorizations import authorizations_page
from superform.channels import channels_page
from superform.posts import posts_page
from superform.users import get_moderate_channels_for_user, is_moderator
from superform.utils import get_module_full_name

from superform.plugins.linkedin import setAccessToken

app = Flask(__name__)
app.config.from_json("config.json")

# Register blueprints
app.register_blueprint(authentication_page)
app.register_blueprint(authorizations_page)
app.register_blueprint(channels_page)
app.register_blueprint(posts_page)
app.register_blueprint(pub_page)

# Init dbs
db.init_app(app)

# List available channels in config
app.config["PLUGINS"] = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules(superform.plugins.__path__, superform.plugins.__name__ + ".")
}


@app.route('/')
def index():
    user = User.query.get(session.get("user_id", "")) if session.get("logged_in", False) else None
    posts=[]
    flattened_list_pubs =[]
    if user is not None:
        setattr(user,'is_mod',is_moderator(user))
        posts = db.session.query(Post).filter(Post.user_id==session.get("user_id", ""))
        chans = get_moderate_channels_for_user(user)
        pubs_per_chan = (db.session.query(Publishing).filter((Publishing.channel_id == c.id) & (Publishing.state == 0)) for c in chans)
        flattened_list_pubs = [y for x in pubs_per_chan for y in x]

    return render_template("index.html", user=user,posts=posts,publishings = flattened_list_pubs)


@app.route('/linkedin/verify')
def linkedin_verify_authorization():
    code = request.args.get('code')
    channel_name = request.args.get('state')
    if code != None:
        profile_email = setAccessToken(channel_name,code)

        channel = Channel.query.filter_by(name=channel_name,module=get_module_full_name("linkedin")).first()
        print(channel)
        #add the configuration to the channel
        str_conf = "{"
        str_conf += "\"profile_email\" : \"" + profile_email + "\""
        str_conf += "}"

        channel.config = str_conf
        db.session.commit()

    #normally should redirect to the channel page or to the page that publish a post
    return redirect(url_for('channels.channel_list'))

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403


@app.errorhandler(404)
def notfound(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
