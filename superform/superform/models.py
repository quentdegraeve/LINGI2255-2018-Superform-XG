from flask_sqlalchemy import SQLAlchemy
from enum import Enum
import datetime

from sqlalchemy import UniqueConstraint

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    posts = db.relationship("Post", backref="user", lazy=True)
    authorizations = db.relationship("Authorization", backref="user", lazy=True)

    def __repr__(self):
        return '<User {}>'.format(repr(self.id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.String(80), db.ForeignKey("user.id"), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    link_url = db.Column(db.Text)
    image_url = db.Column(db.Text)
    date_from = db.Column(db.DateTime)
    date_until = db.Column(db.DateTime)

    publishings = db.relationship("Publishing", backref="post", lazy=True)

    __table_args__ = ({"sqlite_autoincrement": True},)

    def __repr__(self):
        return '<Post {}>'.format(repr(self.id))

    def is_a_record(self):
        if (len(self.publishings) == 0):
            return False
        else:
            # check if all the publications from a post are archived
            for pub in self.publishings:
                if (pub.state != 2):
                    # state 2 is archived.
                    return False
            return True


class Publishing(db.Model):
    publishing_id = db.Column(db.Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    num_version = db.Column(db.Integer, nullable=False, default=1)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"), nullable=False)
    state = db.Column(db.Integer, nullable=False, default=-1)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    link_url = db.Column(db.Text)
    image_url = db.Column(db.Text)
    date_from = db.Column(db.DateTime)
    date_until = db.Column(db.DateTime)

    UniqueConstraint(num_version, post_id, channel_id, name='unicity_publishing_numvers')
    __table_args__ = ({"sqlite_autoincrement": True},)

    def __repr__(self):
        return '<Publishing {} ({} {})>'.format(repr(self.publishing_id), repr(self.post_id), repr(self.channel_id))

    def get_author(self):
        return db.session.query(Post).get(self.post_id).user_id


class PubGCal(Publishing):

    date_start = db.Column(db.DateTime, nullable=True)
    date_end = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.Text, nullable=True)
    color_id = db.Column(db.Text, nullable=True)
    hour_start = db.Column(db.Text, nullable=True)
    hour_end = db.Column(db.Text, nullable=True)
    guests = db.Column(db.Text, nullable=True)
    visibility = db.Column(db.Text, nullable=True)
    availability = db.Column(db.Text, nullable=True)


class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    module = db.Column(db.String(100), nullable=False)
    config = db.Column(db.Text, nullable=False)

    publishings = db.relationship("Publishing", backref="channel", lazy=True)
    authorizations = db.relationship("Authorization", cascade="all, delete", backref="channel", lazy=True)

    __table_args__ = ({"sqlite_autoincrement": True},)

    def __repr__(self):
        return '<Channel {}>'.format(repr(self.id))


class Authorization(db.Model):

    user_id = db.Column(db.String(80), db.ForeignKey("user.id"), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"), nullable=False)
    permission = db.Column(db.Integer, nullable=False)

    __table_args__ = (db.PrimaryKeyConstraint('user_id', 'channel_id'),)

    def __repr__(self):
        return '<Authorization {} {}>'.format(repr(self.user_id), repr(self.channel_id))


class Comment(db.Model):
    publishing_id = db.Column(db.Integer, db.ForeignKey("publishing.publishing_id"), primary_key=True, nullable=False)
    user_comment = db.Column(db.Text, nullable=True)
    moderator_comment = db.Column(db.Text, nullable= True)

    def __repr__(self):
        return '<Comment {}>'.format(repr(self.publishing_id))

    __table_args__ = (db.PrimaryKeyConstraint('publishing_id'),)


class Permission(Enum):
    AUTHOR = 1
    MODERATOR = 2


class State(Enum):
    INCOMPLETE = -1
    NOT_VALIDATED = 0
    PUBLISHED = 1
    ARCHIVED = 2
    REFUSED = 3
    OLD_VERSION=4