from flask import redirect, url_for, request, Blueprint
from superform.models import db, Post, Publishing, Channel
from superform.utils import login_required

"""
delete(id, idc) first show a pop-up window to ask confirmation to the user. If the lattest clicks 'OK',
then it will query the plugin and its channel from the the database, using @id and @idc, in order to 
get the concerned module.
It then calls the deletable() method of the concerned module. If true, the delete(pub) method is called
from the module, and then delete it from the database. Otherwise, it will call can_be_deleted(id, idc) to 
ask the module if the publishing can be deleted from the database anyway.
Eventually, delete(id, idc) tries to query any publishing from the post which id is @id. If the result
is null, then the post is deleted from database.
"""

del_page = Blueprint('delete', __name__)


@del_page.route('/delete/<int:id>', methods=["GET","POST"])
@login_required()
def delete(id):
    # show a pop-up window that asks confirmation
    for pub in db.session.query(Publishing).filter(Publishing.post_id == id):
        chan = db.session.query(Channel).filter(Channel.id == pub.channel_id).first()
        plugin_name = chan.module
        from importlib import import_module
        plugin = import_module(plugin_name)
        if plugin.deletable():
            plugin.delete(pub)
            # database deletion
            db.session.delete(pub)
        elif not(can_be_deleted(pub)):
            #display error message
            print("Error : this publishing cannot be deleted")
        else:
            # database deletion
            db.session.delete(pub)
    post = db.session.query(Post).filter(Post.id == id).first()
    if can_be_deleted(post):
        print("Post successfully deleted")
        db.session.delete(post)
    else:
        print("Post couldn't be deleted because some publishing couldn't be deleted")
    db.session.commit()
    return redirect(url_for('index'))
    # html correction
    # reload the index page without the deleted publishing
    # show a pop-up saying that it is a success (or a fail), with a OK button


def can_be_deleted(publishing):
    return publishing.state != 1


def can_be_deleted(post):
    return db.session.query(Publishing).filter(Publishing.post_id == post.id).first() is None
