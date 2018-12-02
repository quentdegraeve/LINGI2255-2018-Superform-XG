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
            "name": "My Twitter",
            "fields": [
                {
                    "name": "description",
                    "value": "Description 2"
                }
            ]
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
            component.prop("required", true);
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

function addLinkToDropDownButton(button, link) {
    var menu = button.find(".dropdown-menu");
    link.addClass("dropdown-item");
    menu.append(link);
}

function createHeader(label, button) {

    var title = $("<div>");
    title.append(label);

    var tools = $("<div>");
    tools.append(button);

    var container = $("<div>");
    container.addClass("d-flex");
    container.addClass("justify-content-between");
    container.append(title);
    container.append(tools);

    return container;
}

function createDisclaimer(content) {

    var container = $("<div>");
    container.addClass("alert");
    container.addClass("alert-danger");

    var button = $("<button>");
    button.addClass("close");
    button.prop("type", "button");
    button.attr("data-dismiss", "alert");
    button.attr("aria-label", "Close");

    var icon = $("<i>");
    icon.addClass("fas");
    icon.addClass("fa-times");

    button.append(icon);
    container.append(button);
    container.append(content);

    return container;
}

function createComponent(field) {

    var button = createDropDownButton();
    var restore = $("<a>");
    restore.text("Restore");

    addLinkToDropDownButton(button, restore);

    var label = $("<label>");
    label.text(field.label);

    var header = createHeader(label, button);
    var input = createInput(field);
    var container = $("<div>");

    container.addClass("form-group");
    container.append(header);
    container.append(input);

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

function createChannelFieldset(fields, channel, name) {

    if (typeof channel === 'undefined') {
        return;
    }

    var fieldset = createFieldSet(name);

    for (var k = 0; k < fields.length; k++) {
        if ($.inArray(fields[k].name, channel.disabled_fields) < 0) {
            fieldset.append(createComponent(fields[k]));
        }
    }

    for (var k = 0; k < channel.fields.length; k++) {
        fieldset.append(createComponent(channel.fields[k]));
    }

    return fieldset;
}

function fillGeneralFieldset() {
    var fieldset = $("fieldset[name=\"General\"]");
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

    tabs.append(tab);
    selector.append(a);
}

$(document).ready(function () {

    var tabs = $("#tabs");
    var selector = $("#selector");

    tabs.empty();
    selector.empty();

    var fields = layout.default.fields;
    var fieldset = createGeneralFieldset(fields);

    addTab(tabs, selector, fieldset, "General");

    for (var k = 0; k < data.channels.length; k++) {
        var channel = layout.channels.find(function(channel) {
            return channel.module == data.channels[k].module;
        });
        var fieldset = createChannelFieldset(fields, channel, data.channels[k].name);
        if (typeof fieldset !== 'undefined') {
            addTab(tabs, selector, fieldset, data.channels[k].name);
        }
    }

    fillGeneralFieldset();
    fillChannelFieldset();

    selector.children().first().addClass("active");
    tabs.children().first().addClass("active show");

    $("#validate").on("click", function() {
        var button = $(this);
        button.prop("disabled", true);
        var filled = true;
        $(":required").each(function() {
            if ($(this).val().length === 0) {
                var disclaimer = createDisclaimer("This field is required");
                $(this).parent().append(disclaimer);
                if (filled) {
                    filled = false;
                }
            }
        });
        if (filled) {
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
            button.prop("disabled", false);
        }
    });

    $("#add").on("click", function() {
        var container = $("#add_channel");
        container.modal();
    });
});