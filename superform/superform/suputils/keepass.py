import os
import sys
import platform
from flask import has_request_context
from pykeepass import PyKeePass

dir_path = os.path.dirname(os.path.realpath(__file__))

try:
    if platform.system() == 'Windows':
        kp = PyKeePass(dir_path + '\Superform.kdbx', keyfile=dir_path + '\\NewKey.key')
    else:
        kp = PyKeePass(dir_path + '/Superform.kdbx', keyfile=dir_path + '/NewKey.key')

except ImportError or FileNotFoundError:
    sys.exit('Please create a Keepass database named Superform with a key file named NewKey.key in the subutils folder')


def set_entry_from_data(title, username=None, password=None, url=None, notes=None):
    KeepassEntry.title = title
    KeepassEntry.username = username
    KeepassEntry.password = password
    KeepassEntry.url = url
    KeepassEntry.notes = notes


def add_entry_in_group(group):
    group_kp = kp.find_groups(name=group, first=True)
    if group_kp is None:
        group_kp = kp.add_group(kp.root_group, group)
    kp.add_entry(group_kp, KeepassEntry.title, KeepassEntry.username, KeepassEntry.password, KeepassEntry.url, KeepassEntry.notes)
    kp.save()


def delete_entry(title):
    entry_kp = kp.find_entries(title=title, first=True)
    if entry_kp is not None:
        kp.delete_entry(entry_kp)
        kp.save()


def modify_entry_in_group(group, title):
    entry_kp = kp.find_entries(title=title, first=True)
    if KeepassEntry.password == '':
        KeepassEntry.password = entry_kp.password
    if KeepassEntry.username == '':
        KeepassEntry.username = entry_kp.username
    delete_entry(title)
    add_entry_in_group(group)


def get_password_from_keepass(title):
    entry = kp.find_entries(title=title, first=True)
    if entry.password is None:
        if has_request_context():
            return 0
        else:
            sys.exit('Keepass password is not set for ' + title)
    return entry.password


def set_entry_from_keepass(title):
    entry = kp.find_entries(title=title, first=True)
    if entry.username is None or entry.password is None:
        if has_request_context():
            return 0
        else:
            if entry.username is None and entry.password is None:
                sys.exit('Keepass username and password are not set for ' + title)
            elif entry.password is None:
                sys.exit('Keepass password is not set for ' + title)
            else:
                sys.exit('Keepass username is not set for ' + title)
    KeepassEntry.title = entry.title
    KeepassEntry.username = entry.username
    KeepassEntry.password = entry.password
    KeepassEntry.url = entry.url
    KeepassEntry.notes = entry.notes


class KeepassEntry:
    title = ''
    username = ''
    password = ''
    url = ''
    notes = ''
