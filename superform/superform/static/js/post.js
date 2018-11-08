$("input[type='checkbox']").each(function(){
     if($(this).attr("module-namechan") == "superform.plugins.linkedin" || $(this).attr("module-namechan") == "superform.plugins.slack" ){
         $(this).on("click",adapt_post_to_channel($(this).attr('data-namechan')));
     }
});

function adapt_post_to_channel(chan_name){
    document.getElementById(chan_name+"_imagepost").type = "text";
}

$("#publish-button").click(function(event){
    var toReturn = true;
     $("input[type='checkbox']:checked").each(function(){
        if($(this).attr("module-namechan") == "superform.plugins.linkedin"){
            if((!prevalidate_post($(this).attr("data-namechan"),200,256))){
                document.getElementById("li_"+$(this).attr("data-namechan")).children[0].style.color = "red";
                toReturn = false;
                return toReturn;
            }
        }else if($(this).attr("module-namechan") == "superform.plugins.slack"){
            if((!prevalidate_post($(this).attr("data-namechan"),40000,40000))){
                toReturn = false
                return toReturn;
            }
        }
      });
     return toReturn;
});


function createErrorMessage (element,error_message,id){
    var message = document.getElementById(id);
    if(message) {
        message.textContent =  error_message;
    }else{
        var new_elem = document.createElement('div');
        new_elem.setAttribute('id', id);
        new_elem.setAttribute('class',"error");
        var t = document.createTextNode(error_message);
        new_elem.appendChild(t);
         element.before(new_elem);
    }
}
function prevalidate_post (chan_name,title_length,descr_length){
     var toReturn = true;
     var elementToRemove;
     var input_title = document.getElementById(chan_name+"_titlepost");
    if (input_title.value == "") {
        createErrorMessage(input_title,"the title is empty","error_title");
        input_title.classList.add("invalid");
        toReturn = false;
    }else if(input_title.value.length > title_length){
         createErrorMessage(input_title,"the title is too long","error_title");
        input_title.classList.add("invalid");
        toReturn = false;
    }else{
        elementToRemove = document.getElementById("error_title");;
        if(elementToRemove){
            elementToRemove.remove();
        }
        input_title.classList.remove("invalid");
    }
    var input_descrip = document.getElementById(chan_name+"_descriptionpost");
    if (input_descrip.value == "") {
        createErrorMessage(input_descrip,"the description is empty","error_desc");
        input_descrip.classList.add("invalid");
        toReturn = false;
    }else if(input_descrip.value.length > descr_length){
        createErrorMessage(input_descrip,"the description is too long","error_desc");
        input_descrip.classList.add("invalid");
        toReturn = false;
    }else{
        elementToRemove = document.getElementById("error_desc");
        if(elementToRemove){
            elementToRemove.remove();
        }
        input_descrip.classList.remove("invalid");
    }

    var input_linkUrlPost = document.getElementById(chan_name+"_linkurlpost");
    var pattern = new RegExp('^(?:(?:https?|http?|wwww?):\\/\\/)?(?:(?!(?:10|127)(?:\\.\\d{1,3}){3})(?!(?:169\\.254|192\\.168)(?:\\.\\d{1,3}){2})(?!172\\.(?:1[6-9]|2\\d|3[0-1])(?:\\.\\d{1,3}){2})(?:[1-9]\\d?|1\\d\\d|2[01]\\d|22[0-3])(?:\\.(?:1?\\d{1,2}|2[0-4]\\d|25[0-5])){2}(?:\\.(?:[1-9]\\d?|1\\d\\d|2[0-4]\\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\\.(?:[a-z\u00a1-\uffff]{2,})))(?::\\d{2,5})?(?:\\/\\S*)?$');
    if( input_linkUrlPost.value != "" && !pattern.test(input_linkUrlPost.value)) {
        createErrorMessage(input_linkUrlPost,"insert a valid link","error_linkUrlPost");
        input_linkUrlPost.classList.add("invalid");
        toReturn = false;
    }else{
        elementToRemove = document.getElementById("error_linkUrlPost");
        if(elementToRemove){
            elementToRemove.remove();
        }
         input_linkUrlPost.classList.remove("invalid");
    }

    var input_linkImgUrlPost = document.getElementById(chan_name+"_imagepost");
    if( input_linkImgUrlPost.value != "" && !pattern.test(input_linkImgUrlPost.value)) {
        createErrorMessage(input_linkImgUrlPost,"insert a valid picture link ","error_linkImgUrlPost");
        input_linkImgUrlPost.classList.add("invalid");
        toReturn = false;
    }else{
        elementToRemove = document.getElementById("error_linkImgUrlPost");
        if(elementToRemove){
            elementToRemove.remove();
        }
         input_linkImgUrlPost.classList.remove("invalid");
    }

    var input_datefrompost = document.getElementById(chan_name+"_datefrompost");
    if(input_datefrompost.value == ""){
        createErrorMessage(input_datefrompost,"the date from post is empty","error_datefrompost");
        input_datefrompost.classList.add("invalid");
        toReturn = false;
    }else{
        elementToRemove = document.getElementById("error_datefrompost");
        if(elementToRemove){
            elementToRemove.remove();
        }
        input_datefrompost.classList.remove("invalid");
    }

    var input_dateuntilpost = document.getElementById(chan_name+"_dateuntilpost");
    if(input_dateuntilpost.value == ""){
        createErrorMessage(input_dateuntilpost,"the date until post is empty","error_dateuntilpost");
        input_dateuntilpost.classList.add("invalid");
        toReturn = false;
    }else{
        elementToRemove = document.getElementById("error_dateuntilpost");
        if(elementToRemove){
            elementToRemove.remove();
        }
        input_dateuntilpost.classList.remove("invalid");
    }

    var a = new Date(input_datefrompost.value);
    var b = new Date(input_dateuntilpost.value);
    if( b < a){
        createErrorMessage(input_dateuntilpost,"the date until post is more big that date from post","error_dateuntilpost");
        input_dateuntilpost.classList.add("invalid");
        toReturn = false;
    }

    if(a > new Date()){
        createErrorMessage(input_datefrompost,"the date is more old that now ", "error_datefrompost");
        input_dateuntilpost.classList.add("invalid");
        toReturn = false;
    }
    return toReturn;
}

