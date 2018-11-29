function update_img_link(){
    var module  = document.getElementsByClassName('row')[0].getAttribute("module-namechan");
    if(module  == "superform.plugins.linkedin" || module == "superform.plugins.slack") {
        document.getElementById('imagepost').type = "text";
        document.getElementById('imagepost_old').type = "text";
    }
}

update_img_link();

let height = $('#old_pub').height() - $('#mod_comment').height(); // - $('#pagination_old').height();
$('#chat_box').height(height);
$('#chat_box').show();
$('#chat_box .scroll').scrollTop($('#chat_box .scroll')[0].scrollHeight);

let current = 0;
if(pubs.length > 1){
    $('#prev_button').removeClass('disabled');
    current = pubs.length-1;
}

function updateFields(){
    $('#titlepost_old').val(pubs[current].title);
    $('#descrpost_old').val(pubs[current].description);
    $('#linkurlpost_old').val(pubs[current].link_url);
    $('#imagepost_old').val(pubs[current].image_url);
    $('#datefrompost_old').val(pubs[current].date_from);
    $('#dateuntilpost_old').val(pubs[current].date_until);

    if(current == 0){
        $('#prev_button').addClass('disabled');
    }
    else{
        $('#prev_button').removeClass('disabled');
    }
    if(current != pubs.length - 1){
        $('#next_button').removeClass('disabled');
    }
    else{
        $('#next_button').addClass('disabled');
    }
}

$('#next_button').on('click', function(){
    if(pubs.length > current+1){
        current++;
        updateFields();
    }
});

$('#prev_button').on('click', function(){
    if(current-1 >= 0){
        current--;
        updateFields();
    }
});

$('.talktext').on('click', function () {
    _this = $(this);
    number = _this.attr('id').split('_')[1] - 1;
    console.log(number)
    current = number;
    updateFields();
});

