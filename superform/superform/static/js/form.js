var layout = {
    "default": {
        "fields": [
            {
                "name": "title",
                "label": "Title",
                "required": true,
                "type": "input[\"text\"]"
            },
            {
                "name": "description",
                "label": "Description",
                "required": true,
                "type": "textarea"
            },
            {
                "name": "link",
                "label": "Link",
                "required": true,
                "type": "input[\"text\"]"
            },
            {
                "name": "image",
                "label": "Image",
                "required": true,
                "type": "input[\"text\"]"
            },
            {
                "name": "publication_date",
                "label": "Publication Date",
                "required": true,
                "type": "input[\"date\"]"
            },
            {
                "name": "publication_until",
                "label": "Publication Until",
                "required": true,
                "type": "input[\"date\"]"
            }
        ]
    },
    "channels": [
        {
            "module": "Twitter",
            "icon": "fab fa-twitter",
            "disabled_fields": ["title"],
            "fields": []
        }
    ]
};

var data = {
    "default": {
        "fields": [
            {
                "name": "title",
                "value": "Ceci est mon titre"
            },
            {
                "name": "description",
                "value": "Ceci est ma description"
            },
            {
                "name": "link",
                "value": "http://www.google.com"
            },
            {
                "name": "image",
                "value": "http://www.google.com"
            },
            {
                "name": "publication_date",
                "value": "2018-12-12"
            },
            {
                "name": "publication_until",
                "value": "2018-12-12"
            }
        ]
    },
    "channels": [
        {
            "module": "Twitter",
            "name": "My first Twitter account",
            "state": 0,
            "fields": [
                {
                    "name": "description",
                    "value": "Description 2"
                }
            ]
        },
        {
            "module": "Twitter",
            "state": -1,
            "name": "My second Twitter account",
            "fields": []
        },
        {
            "module": "Twitter",
            "state": -1,
            "name": "My third Twitter account",
            "fields": []
        }
    ]
};

function createInput(field) {

    var component = 'undefined';

    switch (field.type) {
        case "input[\"text\"]":
            component = $("<input>");
            component.prop("type", "text");
            break;
        case "input[\"date\"]":
            component = $("<input>");
            component.prop("type", "date");
            break;
        case "textarea":
            component = $("<textarea>");
            component.prop("rows", 5);
            break;
        case "select":
            component = $("<select>");
            for (var k = 0; k < field.options.length; k++) {
                var option = $("<option>");
                option.text(field.options[k]);
                component.append(option);
            }
            break;
    }

    if (typeof component !== 'undefined') {
        component.addClass("form-control");
        component.prop("name", field.name);
        if (field.required) {
            component.prop("required", "required");
        }
    }

    return component;
}

function createDropDownButton() {

    var button = $("<button>");

    button.addClass("btn");
    button.addClass("btn-light");
    button.addClass("dropdown-toggle");
    button.prop("type", "button");
    button.attr("data-toggle", "dropdown");
    button.attr("aria-haspopup", true);
    button.attr("aria-expanded", false);
    button.text("options");

    var menu = $("<div>");
    menu.addClass("dropdown-menu");

    var container = $("<div>");
    container.addClass("btn-group");
    container.append(button);
    container.append(menu);

    return container;
}

function addLinkToDropDownButton(button, a) {
    var container = button.find(".dropdown-menu");
    a.addClass("dropdown-item");
    container.append(a);
}

function createComponent(field) {

    // Header :

    var label = $("<span>");
    label.addClass("font-weight-bold");
    label.text(field.label);

    var title = $("<div>");
    title.append(label);

    if (field.required) {
        var icon = $("<span>");
        icon.addClass("text-danger");
        icon.text("*");
        title.append(icon);
    }

    var header = $("<div>");
    header.addClass("field-header");
    header.append(title);

    // Body :

    var input = createInput(field);
    var feedback = $("<div>");
    feedback.addClass("invalid-feedback");
    feedback.append("This field seems to be empty or incorrect");

    var body = $("<div>");
    body.addClass("field-body");
    body.append(input);
    body.append(feedback);

    // Footer :

    var button = createDropDownButton();
    var restore = $("<a>");
    restore.text("Restore");
    addLinkToDropDownButton(button, restore);

    var footer = $("<div>");
    footer.addClass("field-body");
    footer.append(button);

    // Container :

    var container = $("<div>");
    container.addClass("field");
    container.append(header);
    container.append(body);
    container.append(footer);
    return container;
}

function createFieldSet(name) {
    var fieldset = $("<fieldset>");
    fieldset.prop("name", name);
    return fieldset;
}

function createGeneralFieldset(fields) {

    var fieldset = createFieldSet("General");

    for (var i = 0; i < fields.length; i++) {
        var component = createComponent(fields[i]);
        fieldset.append(component);
    }

    return fieldset;
}

function createChannelFieldset(channel) {
    var fieldset = createFieldSet(channel.name);
    for (var i = 0; i < layout.channels.length; i++) {
        if (layout.channels[i].module === channel.module) {
            for (var j = 0; j < layout.default.fields.length; j++) {
                var field = layout.default.fields[j];
                if ($.inArray(field.name, layout.channels[i].disabled_fields) < 0) {
                    fieldset.append(createComponent(field));
                }
            }
            var fields = layout.channels[i].fields;
            for (var j = 0; j < fields.length; j++) {
                fieldset.append(createComponent(fields[j]));
            }
            return fieldset;
        }
    }
}

function fillGeneralFieldset() {
    var name = "General";
    var fieldset = $("fieldset[name=\"" + name + "\"]");
    for (var k = 0; k < data.default.fields.length; k++) {
        var field = data.default.fields[k];
        var input = fieldset.find("[name=\"" + field.name + "\"]");
        input.val(field.value);
    }
}

function fillChannelFieldset() {
    for (var i = 0; i < data.channels.length; i++) {
        var channel = data.channels[i];
        var fieldset = $("fieldset[name=\"" + channel.name + "\"]");
        for (var j = 0; j < channel.fields.length; j++) {
            var field = channel.fields[j];
            var input = fieldset.find("[name=\"" + field.name + "\"]");
            input.val(field.value);
        }
    }
}

function addTab(tabs, selector, fieldset, name) {

    var id = name.replace(/\s/g, "_");

    var tab = $("<div>");
    tab.addClass("tab-pane");
    tab.addClass("fade");
    tab.attr("id", id);
    tab.attr("role", "tabpanel");
    tab.attr("aria-labelledby", id + "_tab");
    tab.append(fieldset);

    var a = $("<a>");
    a.addClass("nav-link");
    a.attr("id", id + "_tab");
    a.attr("data-toggle", "pill");
    a.attr("href", "#" + id);
    a.attr("role", "tab");
    a.attr("aria-controls", id);
    a.attr("aria-selected", "false");
    a.text(name);
    a.on("click", function() {
        update_header($(this).attr("href"));
    });

    tabs.append(tab);
    selector.append(a);
}

function createList() {
    var container = $("<div>");
    container.addClass("list-group");
    return container;
}

function addToList(list, name, onclick) {
    var a = $("<a>");
    a.addClass("list-group-item");
    a.addClass("list-group-item-action");
    a.text(name);
    a.on("click", onclick);
    list.append(a);
}

function update_header(href) {
    var id = href.substring(1, href.length);
    if (id === "General") {

        var header = $("#header");
        var title = $("<h1>");
        title.text("General");

        header.empty();
        header.append(title);

        return;
    }
    for (var i = 0; i < data.channels.length; i++) {
        if (data.channels[i].name.replace(/\s/g, "_") === id) {
            for (var j = 0; j < layout.channels.length; j++) {
                if (data.channels[i].module === layout.channels[j].module) {

                    var header = $("#header");
                    var title = $("<h1>");
                    title.append(data.channels[i].name);

                    var p = $("<p>");
                    var ul = $("<ul>");
                    p.addClass("lead");
                    p.append(ul);

                    var li;
                    li = $("<li>");
                    li.append("Module : " + data.channels[i].module);
                    ul.append(li);

                    li = $("<li>");
                    var span = $("<span>");
                    span.addClass("badge");
                    span.addClass("badge-secondary");

                    switch (data.channels[i].state) {
                        case -1:
                            span.text("Incomplete");
                            break;
                        case 0:
                            span.text("Not validated");
                            break;
                        case 1:
                            span.text("Validated");
                            break;
                        case 2:
                            span.text("Archived");
                            break;
                    }

                    li.append("Status : ");
                    li.append(span);
                    ul.append(li);

                    header.empty();
                    header.append(title);
                    header.append(p);
                }
            }
        }
    }
}

$("#validate").click(function() {

    var button = $(this);
    button.prop("disabled", true);

    var form = $(this).parents("form");
    if (form.get(0).checkValidity()) {
        var data = [];
        $("fieldset").each(function() {
            data.push({
                "name": $(this).prop("name"),
                "fields": $(this).serializeArray()
            });
        });
        $.post(url, JSON.stringify(data))
            .done(function() {
                button.prop("disabled", false);
            });
    } else {
        var input = $(".form-control:invalid").first();
        var tab = input.parents(".tab-pane");
        var id = tab.prop("id");
        var link = $("#selector").find("[aria-controls=\"" + id + "\"]");
        link.click();
        button.prop("disabled", false);
    }
    form.addClass("was-validated");
});

$("#add").on("click", function() {

    var container = $("#channel_manager");
    var list = createList();
    var content = container.find(".modal-body");

    content.empty();
    content.append(list);

    for (var i = 0; i < data.channels.length; i++) {
        var channel = data.channels[i];
        if (channel.state < 0) {
            var fieldset = $("fieldset[name=\"" + channel.name + "\"]");
            if (fieldset.length === 0) {
                addToList(list, channel.name, function() {
                    var name = $(this).text();
                    for (var i = 0; i < data.channels.length; i++) {
                        if (data.channels[i].name === name) {
                            var tabs = $("#tabs");
                            var selector = $("#selector");
                            var fieldset = createChannelFieldset(data.channels[i]);
                            addTab(tabs, selector, fieldset, name);
                        }
                    }
                    $(this).remove();
                });
            }
        }
    }

    container.modal();
});

$("#delete").on("click", function() {

    var container = $("#channel_manager");
    var list = createList();
    var content = container.find(".modal-body");

    content.empty();
    content.append(list);

    for (var i = 0; i < data.channels.length; i++) {
        var channel = data.channels[i];
        if (channel.state < 0) {
            var fieldset = $("fieldset[name=\"" + channel.name + "\"]");
            if (fieldset.length > 0) {
                addToList(list, channel.name, function() {
                    var name = $(this).text();
                    var id = name.replace(/\s/g, "_");
                    var link = $("#" + id);
                    if (link.hasClass("active")) {
                        $("#General_tab").addClass("active show");
                        $("#General").addClass("active show");
                    }
                    link.remove();
                    $("#" + id + "_tab").remove();
                    $(this).remove();
                });
            }
        }
    }

    container.modal();
});

$(document).ready(function() {

    var loader = $("#loader");
    var content = $("#content");
    loader.hide();
    content.show();

    var tabs = $("#tabs");
    var selector = $("#selector");

    tabs.empty();
    selector.empty();

    var fields = layout.default.fields;
    var fieldset = createGeneralFieldset(fields);

    addTab(tabs, selector, fieldset, "General");
    var list = createList();
    $("#add_channel .modal-body").append(list);

    for (var k = 0; k < data.channels.length; k++) {
        if (data.channels[k].state >= 0) {
            var name = data.channels[k].name;
            var fieldset = createChannelFieldset(data.channels[k]);
            if (typeof fieldset !== 'undefined') {
                addTab(tabs, selector, fieldset, name);
            }
        }
    }

    fillGeneralFieldset();
    fillChannelFieldset();

    selector.children().first().addClass("active");
    tabs.children().first().addClass("active show");
});