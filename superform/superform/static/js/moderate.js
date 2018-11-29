function update_img_link(){
    var module  = document.getElementsByClassName('row')[0].getAttribute("module-namechan");
    if(module  == "superform.plugins.linkedin" || module == "superform.plugins.slack") {
        document.getElementById('imagepost').type = "text";
    }
}
update_img_link();

$("#publish, #unvalidate").click(function(event){
    var toReturn = true;
    var title_max_length = 200;
    var descr_max_length = 200;
     if((!prevalidate_post(title_max_length,descr_max_length))){
            toReturn = false;
     }
     return toReturn;
});

function prevalidate_post(title_max_length,descr_max_length){
     return prevalidate_post_or_publishing ("titlepost","descrpost",
    "linkurlpost","imagepost",
    "datefrompost","dateuntilpost",title_max_length,descr_max_length);
}




