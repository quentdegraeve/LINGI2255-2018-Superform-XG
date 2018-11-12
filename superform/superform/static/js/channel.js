$("#inlineFormCustomSelectModule").on("click",function(){
    var e = document.getElementById("inlineFormCustomSelectModule");
    var module = e.options[e.selectedIndex].value;
    add_inputs_for_channel(module);
});

function add_inputs_for_channel(module){
    var input_username = document.getElementById("inlineFormInputTextUserName");
    var input_password = document.getElementById("inlineFormInputTextPassword");
    if(module == "linkedin" || module == "slack") {
        if (!input_password) {
            $("<input name=\"password\" type=\"password\" class=\"form-control\" id=\"inlineFormInputTextPassword\" placeholder=\"New channel password\">").insertAfter("#inlineFormInputText");
        }else{
            input_password.hidden = false;
        }
        if (!input_username) {
            $("<input name=\"username\" type=\"text\" class=\"form-control\" id=\"inlineFormInputTextUserName\" placeholder=\"New channel username\">").insertAfter("#inlineFormInputText");
        }else{
            input_username.hidden = false;
        }
    }else{
        if(input_username){
            input_username.hidden = true;
        }
        if(input_password){
            input_password.hidden = true;
        }
    }
}
