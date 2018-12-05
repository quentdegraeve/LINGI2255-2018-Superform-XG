// @authors: Group 4
// @date: December 2018

function createInput(field) {

    var container = $("<div>");
    var component = 'undefined';

    switch (field.type) {
        case "input[\"text\"]":
            component = $("<input>");
            component.attr("type", "text");
            container.append(component);
            break;
        case "input[\"date\"]":
            component = $("<input>");
            component.attr("type", "date");
            container.append(component);
            break;
        case "input[\"url\"]":
            component = $("<input>");
            component.attr("type", "url");
            container.append(component);
            break;
        case "textarea":
            component = $("<textarea>");
            component.attr("rows", 5);
            container.append(component);
            break;
        case "select":
            component = $("<select>");
            var option = 'undefined';
            for (var k = 0; k < field.options.length; k++) {
                option = $("<option>");
                option.text(field.options[k]);
                component.append(option);
            }
            container.append(component);
            break;
        case "radio":
            var option = 'undefined';
            var label = 'undefined';
            for (var k = 0; k < field.options.length; k++) {
                option = $("<input>");
                option.attr("type", "radio");
                option.attr("name", field.name);
                option.attr("value", field.options[k]);
                label = $("<label>");
                label.append(option);
                label.append(field.options[k]);
                component = $("<div>");
                component.addClass("form-check");
                component.append(label);
                container.append(component);
            }
            break;
    }

    if (typeof component !== 'undefined') {
        container.children().each(function() {
            if (!$(this).hasClass("form-check")) {
                $(this).addClass("form-control");
            }
            $(this).attr("name", field.name);
            if (field.required) {
                $(this).attr("required", "required");
            }
        });
    }

    return container;
}

function createComponent(field) {

    // Header :

    var label = $("<span>");
    label.addClass("font-weight-bold");
    label.text(field.label);

    var header = $("<div>");
    header.addClass("field-header");
    header.append(label);

    if (field.required) {
        var icon = $("<span>");
        icon.addClass("text-danger");
        icon.text("*");
        header.append(icon);
    }

    // Body :

    var feedback = $("<div>");
    feedback.addClass("invalid-feedback");
    feedback.append("This field seems to be empty or incorrect");

    var body = createInput(field);
    body.addClass("field-body");
    body.append(feedback);

    // Footer :

    var footer = $("<div>");
    footer.addClass("field-footer");

    // Container :

    var container = $("<div>");
    container.addClass("field");
    container.append(header);
    container.append(body);
    container.append(footer);
    return container;
}

function createDropDownButton() {

    var button = $("<button>");

    button.addClass("btn");
    button.addClass("btn-light");
    button.addClass("dropdown-toggle");
    button.attr("type", "button");
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

function addOptionToComponent(component, name, onclick) {

    var footer = component.find(".field-footer");
    var container = footer.find(".btn-group");

    if (container.length === 0) {
        footer.append(createDropDownButton());
    }

    var option = $("<a>");
    option.addClass("dropdown-item");
    option.on("click", onclick);
    option.text(name);

    var menu = footer.find(".dropdown-menu");
    menu.append(option);
}

function createIcon(name) {
    var icon = $("<i>");
    icon.addClass(name);
    return icon;
}

function createBadge(state) {

    var span = $("<span>");
    span.addClass("badge");
    span.addClass("badge-secondary");

    switch (state) {
        case -1:
            span.text("Incomplete");
            return span;
        case 0:
            span.text("Not validated");
            return span;
        case 1:
            span.text("Validated");
            return span;
        case 2:
            span.text("Archived");
            return span;
    }
    return span;
}

function createAlert() {

    var button = $("<button>");
    button.addClass("close");
    button.attr("type", "button");
    button.attr("data-dismiss", "alert");
    button.attr("aria-label", "Close");
    button.attr("type", "button");

    var icon = createIcon("fas fa-times");
    icon.attr("aria-hidden", "true");
    button.append(icon);

    var container = $("<div>");
    container.addClass("alert");
    container.addClass("alert-dismissible");
    container.addClass("fade");
    container.addClass("show");
    container.attr("role", "alert");
    container.append(button);

    return container;
}

function createSuccessMessage(content) {
    var container = createAlert();
    container.addClass("alert-success");
    container.prepend(content);
    return container;
}

function createErrorMessage(content) {
    var container = createAlert();
    container.addClass("alert-danger");
    container.prepend(content);
    return container;
}

function createWarningMessage(content) {
    var container = createAlert();
    container.addClass("alert-warning");
    container.prepend(content);
    return container;
}

function createFieldset(name) {
    var fieldset = $("<fieldset>");
    fieldset.attr("name", name);
    return fieldset;
}

function createGeneralFieldset(fields) {

    var fieldset = createFieldset("General");

    for (var k = 0; k < fields.length; k++) {
        var component = createComponent(fields[k]);
        fieldset.append(component);
    }

    return fieldset;
}

function createChannelFieldset(channel) {

    var fieldset = createFieldset(channel.name);

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
    var fields = data.default.fields;

    for (var key in fields) {
        var input = fieldset.find("[name=\"" + key + "\"]");
        input.val(fields[key]);
    }
}

function fillChannelFieldset() {
    for (var k = 0; k < data.channels.length; k++) {

        var channel = data.channels[k];
        var fieldset = $("fieldset[name=\"" + channel.name + "\"]");
        var fields = channel.fields;

        for (var key in fields) {
            var input = fieldset.find("[name=\"" + key + "\"]");
            input.val(fields[key]);
        }
    }
}

function addTab(tabs, selector, fieldset) {

    var name = fieldset.attr("name");
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

// Features :

function addRestoreFeature(component) {
    addOptionToComponent(component, "Reset", function() {
        var container = $(this).parents(".field");
        var input = container.find(".form-control");
        for (var i = 0; i < data.default.fields.length; i++) {
            if (data.default.fields[i].name === input.attr("name")) {
                input.val(data.default.fields[i].value);
            }
        }
    });
}

function retrieveFormData() {
    var data = [];
    $("fieldset").each(function() {
        var array = $(this).serializeArray();
        var fields = {};
        for (var i = 0; i < array.length; i++) {
            fields[array[i].name] = array[i].value;
        }
        data.push({
            "name": $(this).attr("name"),
            "fields": fields
        });
    });
    return JSON.stringify(data);
}

$("#validate").click(function() {

    var button = $(this);
    button.attr("disabled", true);

    var content = $("<div>");
    content.append(createIcon("fas fa-spinner spin"));
    content.append("Loading...");

    var logs = $("#logs");
    logs.empty();
    logs.append(createWarningMessage(content));

    var form = $(this).parents("form");
    if (form.get(0).checkValidity()) {
        $.post(server_url, retrieveFormData())
            .done(function() {
                var content = $("<div>");
                content.append("The fields has been saved !");
                var message = createSuccessMessage(content);
                logs.empty();
                logs.append(message);
                button.attr("disabled", false);
            }).fail(function(error) {
                var content = $("<div>");
                content.append("An error has occurred !");
                var message = createErrorMessage(content);
                logs.empty();
                logs.append(message);
                button.attr("disabled", false);
            });
    } else {

        var content = $("<div>");
        content.append("Some field are incomplete !");

        var message = createErrorMessage(content);
        message.find("button.close").on("click", function() {
            form.removeClass("was-validated");
        });

        logs.empty();
        logs.append(message);

        form.addClass("was-validated");
        button.attr("disabled", false);
    }
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

var layout;
var data;

$(document).ready(function() {

    var logs = $("#logs");
    logs.empty();
    logs.append(createIcon("fas fa-spinner spin"));
    logs.append("Loading...");

    $.get(layout_url, function(json) {
        layout = json;
    }).done(function() {
        $.get(data_url, function(json) {
            data = json;
        }).done(function() {

            logs.empty();

            var content = $("#content");
            content.show();

            var tabs = $("#tabs");
            var selector = $("#selector");

            tabs.empty();
            selector.empty();

            var fields = layout.default.fields;
            var fieldset = createGeneralFieldset(fields);

            addTab(tabs, selector, fieldset);

            for (var k = 0; k < data.channels.length; k++) {
                if (data.channels[k].state >= 0) {
                    var name = data.channels[k].name;
                    var fieldset = createChannelFieldset(data.channels[k]);
                    if (typeof fieldset !== 'undefined') {
                        addTab(tabs, selector, fieldset);
                    }
                }
            }

            fillGeneralFieldset();
            fillChannelFieldset();

            selector.children().first().addClass("active");
            tabs.children().first().addClass("active show");

        }).fail(function() {
            logs.empty();
            logs.append(createErrorMessage("Error while loading the data"));
        });
    }).fail(function() {
        logs.empty();
        logs.append(createErrorMessage("Error while loading the layout"));
    });
});