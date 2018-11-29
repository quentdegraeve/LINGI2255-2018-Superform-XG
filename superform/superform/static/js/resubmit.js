$("#publish-button").click(function(event){
    var toReturn = true;
       var title_max_length = 200;
    var descr_max_length = 200;
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

