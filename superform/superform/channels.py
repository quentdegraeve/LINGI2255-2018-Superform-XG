import json
import ast

from flask import Blueprint, current_app, url_for, request, redirect, render_template

from superform.plugins.linkedin import authenticate
from superform.utils import login_required, get_instance_from_module_path, get_modules_names, get_module_full_name
from superform.models import db, Channel
import ast

from superform.suputils import keepass

channels_page = Blueprint('channels', __name__)


@channels_page.route("/channels", methods=['GET', 'POST'])
@login_required(admin_required=True)
def channel_list():
    if request.method == "POST":
        action = request.form.get('@action', '')
        if action == "new":
            name = request.form.get('name')
            username = request.form.get('username')
            password = request.form.get('password')
            module = request.form.get('module')
            if module in get_modules_names(current_app.config["PLUGINS"].keys()):
                channel = Channel(name=name, module=get_module_full_name(module), config="{}")
                db.session.add(channel)
                db.session.flush()
                keepass.set_entry_from_data(str(channel.id), username, password)
                keepass.add_entry_in_group(module)
                db.session.commit()

        elif action == "delete":
            channel_id = request.form.get("id")
            channel = Channel.query.get(channel_id)
            if channel:
                db.session.delete(channel)
                db.session.commit()
                keepass.delete_entry(channel_id)
        elif action == "edit":
            channel_id = request.form.get("id")
            channel = Channel.query.get(channel_id)
            name = request.form.get('name')
            username = request.form.get('username')
            password = request.form.get('password')
            if name is not '':
                channel.name = name
                conf = json.loads(channel.config)
                conf["channel_name"] = name
                channel.config = json.dumps(conf)
                db.session.commit()
            if username is not '' or password is not '':
                keepass.set_entry_from_data(str(channel.id), username, password)
                keepass.modify_entry_in_group(get_modules_names([channel.module])[0], channel.id)

    channels = Channel.query.all()
    mods = get_modules_names(current_app.config["PLUGINS"].keys())

    auth_fields = dict()

    for m in mods:
        full_name = get_module_full_name(m)
        clas = get_instance_from_module_path(full_name)
        fields = clas.AUTH_FIELDS
        auth_fields[m] = fields

    return render_template("channels.html", channels=channels, modules=get_modules_names(current_app.config["PLUGINS"].keys()), auth_fields=auth_fields)


@channels_page.route("/configure/<int:id>", methods=['GET', 'POST'])
@login_required(admin_required=True)
def configure_channel(id):
    c = Channel.query.get(id)
    m = c.module
    clas = get_instance_from_module_path(m)
    config_fields = clas.CONFIG_FIELDS

    if request.method == 'GET':
        if (c.config is not ""):
            d = ast.literal_eval(c.config)
            setattr(c, "config_dict", d)
        return render_template("channel_configure.html", channel=c, config_fields=config_fields)
    str_conf = "{"
    cfield = 0
    for field in config_fields:
        if cfield > 0:
            str_conf += ","
        str_conf += "\"" + field + "\" : \"" + request.form.get(field) + "\""
        cfield += 1
    str_conf += "}"
    c.config = str_conf
    db.session.commit()
    return redirect(url_for('channels.channel_list'))
