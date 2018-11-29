
update_img_link(document.getElementsByClassName('row')[0].getAttribute("module-namechan").split('.')[2],"imagepost");

$("#publish-button").click(function(event){
    var toReturn = true;
    let mod = document.getElementsByClassName('row')[0].getAttribute("module-namechan").split('.')[2]
    let title_max_length=100000;
    let descr_max_length=100000;
    if(mod != undefined){
    console.log(post_form_validations[mod]);
         if(post_form_validations[mod]['title_max_length'] != undefined){
             title_max_length = post_form_validations[mod]['title_max_length'] ;
         }
         if(post_form_validations[mod]['description_max_length'] != undefined){
             descr_max_length = post_form_validations[mod]['description_max_length'] ;
         }
     }
    if((!prevalidate_post(title_max_length,descr_max_length))){
        toReturn = false;
    }
     return toReturn;
});

function prevalidate_post (title_max_length,descr_max_length){
return prevalidate_post_or_publishing ("titlepost","descrpost",
    "linkurlpost","imagepost",
    "datefrompost","dateuntilpost",title_max_length,descr_max_length);
}

