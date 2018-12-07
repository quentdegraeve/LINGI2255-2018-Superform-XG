from superform.models import Channel, Post, Publishing
from superform.delete import delete
from superform import db

def create_channel(module):
    chan = Channel(name="test_delete_" + module[18:], module=module, config="{}")
    db.session.add(chan)
    db.session.commit()


def create_post():
    post = Post(user_id="superego", title="test_delete", description="test_delete", link_url="", image_url="",
                date_from="", date_until="")
    db.session.add(post)
    db.session.commit()


def create_publishing(id, idc):
    pub = Publishing(post_id=id, channel_id=idc, state=0, title="test_delete", description="test_delete",
                     link_url="", image_url="",
                     date_from="", date_until="", misc="")
    db.session.add(pub)
    db.session.commit()


def test_pub_deleted_single():
    c = db.session.query(Channel).filter(Channel.name == "test_delete_rss", Channel.module == "superform.plugins.rss").first()
    if c is None:
        create_channel("superform.plugins.rss")
        c = db.session.query(Channel).filter(Channel.name == "test_delete_rss", Channel.module == "superform.plugins.rss").first()
    create_post()
    p = db.session.query(Post).filter(Post.title == "test_delete", Post.description == "test_delete").first()
    create_publishing(p.id, c.name)
    pu = db.session.query(Publishing).filter(Publishing.post_id == p.id, Publishing.channel_id == c.name).first()
    delete(p.id)
    assert db.session.query(Publishing).filter(Publishing.post_id == p.id, Publishing.channel_id == c.name).first() is None


def test_post_deleted_single():
    c = db.session.query(Channel).filter(Channel.name == "test_delete_rss",
                                         Channel.module == "superform.plugins.rss").first()
    if c is None:
        create_channel("superform.plugins.rss")
        c = db.session.query(Channel).filter(Channel.name == "test_delete_rss",
                                             Channel.module == "superform.plugins.rss").first()
    create_post()
    p = db.session.query(Post).filter(Post.title == "test_delete", Post.description == "test_delete").first()
    create_publishing(p.id, c.name)
    pu = db.session.query(Publishing).filter(Publishing.post_id == p.id, Publishing.channel_id == c.name).first()
    delete(p.id)
    assert db.session.query(Post).filter(Post.title == "test_delete", Post.description == "test_delete").first() is None


def test_post_deleted_no_pub():
    create_post()
    p = db.session.query(Post).filter(Post.title == "test_delete", Post.description == "test_delete").first()
    delete(p.id)
    assert db.session.query(Post).filter(Post.title == "test_delete", Post.description == "test_delete").first() is None


def test_post_deleted_multiple():
    c1 = db.session.query(Channel).filter(Channel.name == "test_delete_rss",
                                         Channel.module == "superform.plugins.rss").first()
    if c1 is None:
        create_channel("superform.plugins.rss")
        c1 = db.session.query(Channel).filter(Channel.name == "test_delete_rss",
                                             Channel.module == "superform.plugins.rss").first()
    c2 = db.session.query(Channel).filter(Channel.name == "test_delete_gcal",
                                          Channel.module == "superform.plugins.gcal").first()
    if c1 is None:
        create_channel("superform.plugins.gcal")
        c1 = db.session.query(Channel).filter(Channel.name == "test_delete_gcal",
                                              Channel.module == "superform.plugins.gcal").first()
    create_post()
    p = db.session.query(Post).filter(Post.title == "test_delete", Post.description == "test_delete").first()
    create_publishing(p.id, c1.name)
    p1 = db.session.query(Publishing).filter(Publishing.post_id == p.id, Publishing.channel_id == c1.name).first()
    create_publishing(p.id, c2.name)
    p2 = db.session.query(Publishing).filter(Publishing.post_id == p.id, Publishing.channel_id == c1.name).first()
    delete(p.id)
    assert db.session.query(Post).filter(Post.title == "test_delete", Post.description == "test_delete").first() is None


def test_pubs_deleted_mutliple():
    c1 = db.session.query(Channel).filter(Channel.name == "test_delete_rss",
                                          Channel.module == "superform.plugins.rss").first()
    if c1 is None:
        create_channel("superform.plugins.rss")
        c1 = db.session.query(Channel).filter(Channel.name == "test_delete_rss",
                                              Channel.module == "superform.plugins.rss").first()
    c2 = db.session.query(Channel).filter(Channel.name == "test_delete_gcal",
                                          Channel.module == "superform.plugins.gcal").first()
    if c1 is None:
        create_channel("superform.plugins.gcal")
        c1 = db.session.query(Channel).filter(Channel.name == "test_delete_gcal",
                                              Channel.module == "superform.plugins.gcal").first()
    create_post()
    p = db.session.query(Post).filter(Post.title == "test_delete", Post.description == "test_delete").first()
    create_publishing(p.id, c1.name)
    p1 = db.session.query(Publishing).filter(Publishing.post_id == p.id, Publishing.channel_id == c1.name).first()
    create_publishing(p.id, c2.name)
    p2 = db.session.query(Publishing).filter(Publishing.post_id == p.id, Publishing.channel_id == c1.name).first()
    delete(p.id)
    assert (db.session.query(Publishing).filter(Publishing.post_id == p.id, Publishing.channel_id == c1.name).first() is None
            and db.session.query(Publishing).filter(Publishing.post_id == p.id, Publishing.channel_id == c2.name).first() is None)