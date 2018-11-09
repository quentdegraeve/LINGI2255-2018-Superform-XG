function update_img_link(){
    var module  = document.getElementsByClassName('row')[0].getAttribute("module-namechan");
    if(module  == "superform.plugins.linkedin" || module == "superform.plugins.slack") {
        document.getElementById('imagepost').type = "text";
    }
}
update_img_link();



