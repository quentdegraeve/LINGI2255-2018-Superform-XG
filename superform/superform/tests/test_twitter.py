import datetime
import os
import tempfile
import sys
import contextlib

import pytest

from superform import app, db, Publishing
from superform.models import Channel
from superform.plugins import twitter
from io import StringIO


@pytest.fixture
def client():
    app.app_context().push()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_send_tweet_bad_config(client):
    name = "unittest_twitter"
    module = "superform.plugins.twitter"
    P = Publishing(post_id=0,channel_id=name,state=0,title='test',description='unit test')
    C = Channel(name=name, module=module, config="{}")
    db.session.add(C)
    db.session.add(P)
    db.session.commit()
    pub = db.session.query(Publishing).filter(Publishing.post_id == 0, Publishing.channel_id == name).first()
    c = db.session.query(Channel).filter(Channel.name == pub.channel_id).first()
    temp_stdout = StringIO()
    with contextlib.redirect_stdout(temp_stdout):
        twitter.run(pub,c.config)
    output = temp_stdout.getvalue().strip()
    db.session.query(Publishing).filter(Publishing.post_id == 0).delete()
    db.session.query(Channel).filter(Channel.name == name).delete()
    db.session.commit()
    assert 'Missing' in output


def test_tweet_split_no_split():
    string_input = 'hello \t world! \n have a nice day.'
    string_output = twitter.tweet_split(string_input,(',', '!', '?', ':', ';'))
    assert string_input == string_output[0]


def test_tweet_split_3_split():
    string_input = 'Repudiandae quam vel voluptatum voluptates. Rerum quas ut vel ipsum assumenda aut ab. Nam incidunt similique iure fugit animi quia eum sint. Eos voluptatem assumenda nemo repellendus non et nemo. Aliquam ut amet maiores repudiandae vel rerum distinctio. Quasi totam consequatur unde impedit quia dolor. Quia itaque aut aut. Eligendi qui praesentium error. Quis qui corrupti corporis ullam ad pariatur autem magni. Vitae accusantium maiores blanditiis quaerat eum qui. Reiciendis et quis molestias et. Aut dolorem esse praesentium sunt. Quo molestiae est deserunt et sint voluptas. Ullam et pariatur voluptatem sint consequatur sapiente maiores voluptatem. Porro optio rerum natus sed voluptas.'
    string_output = twitter.tweet_split(string_input,(',', '!', '?', ':', ';'))
    assert string_output[0] == '1/3 Repudiandae quam vel voluptatum voluptates. Rerum quas ut vel ipsum assumenda aut ab. Nam incidunt similique iure fugit animi quia eum sint. Eos voluptatem assumenda nemo repellendus non et nemo. Aliquam ut amet maiores repudiandae vel rerum distinctio.'
    assert string_output[1] == '2/3 Quasi totam consequatur unde impedit quia dolor. Quia itaque aut aut. Eligendi qui praesentium error. Quis qui corrupti corporis ullam ad pariatur autem magni. Vitae accusantium maiores blanditiis quaerat eum qui. Reiciendis et quis molestias et.'
    assert string_output[2] == '3/3 Aut dolorem esse praesentium sunt. Quo molestiae est deserunt et sint voluptas. Ullam et pariatur voluptatem sint consequatur sapiente maiores voluptatem. Porro optio rerum natus sed voluptas.'


def test_tweet_split_http_url_split():
    string_input = 'Repudiandae quam vel voluptatum voluptates. Rerum quas ut vel ipsum assumenda aut ab. Nam incidunt similique iure fugit animi quia eum sint. Eos voluptatem assumenda nemo repellendus non et nemo. Aliquam ut amet maiores repudiandae vel rerum distinctio. https://moodleucl.uclouvain.be/course/view.php?id=7599 Aut dolorem esse praesentium sunt. Quo molestiae est deserunt et sint voluptas. Ullam et pariatur voluptatem sint consequatur sapiente maiores voluptatem. Porro optio rerum natus sed voluptas.'
    string_output = twitter.tweet_split(string_input, (',', '!', '?', ':', ';'))
    assert string_output[0] == '1/2 Repudiandae quam vel voluptatum voluptates. Rerum quas ut vel ipsum assumenda aut ab. Nam incidunt similique iure fugit animi quia eum sint. Eos voluptatem assumenda nemo repellendus non et nemo. Aliquam ut amet maiores repudiandae vel rerum distinctio. '
    assert string_output[1] == '2/2 https://moodleucl.uclouvain.be/course/view.php?id=7599 Aut dolorem esse praesentium sunt. Quo molestiae est deserunt et sint voluptas. Ullam et pariatur voluptatem sint consequatur sapiente maiores voluptatem. Porro optio rerum natus sed voluptas.'


def test_tweet_split_www_url_split():
    string_input = 'Repudiandae quam vel voluptatum voluptates. Rerum quas ut vel ipsum assumenda aut ab. Nam incidunt similique iure fugit animi quia eum sint. Eos voluptatem assumenda nemo repellendus non et nemo. Aliquam ut amet maiores repudiandae vel rerum distinctio. www.xkcd.com Aut dolorem esse praesentium sunt. Quo molestiae est deserunt et sint voluptas. Ullam et pariatur voluptatem sint consequatur sapiente maiores voluptatem. Porro optio rerum natus sed voluptas.'
    string_output = twitter.tweet_split(string_input, (',', '!', '?', ':', ';'))
    assert string_output[0] == '1/2 Repudiandae quam vel voluptatum voluptates. Rerum quas ut vel ipsum assumenda aut ab. Nam incidunt similique iure fugit animi quia eum sint. Eos voluptatem assumenda nemo repellendus non et nemo. Aliquam ut amet maiores repudiandae vel rerum distinctio. '
    assert string_output[1] == '2/2 www.xkcd.com Aut dolorem esse praesentium sunt. Quo molestiae est deserunt et sint voluptas. Ullam et pariatur voluptatem sint consequatur sapiente maiores voluptatem. Porro optio rerum natus sed voluptas.'

