$(document).ready(function () {
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


$(document).ready(function () {

    $('#image_input').attr('multiple',true);

    $(".delete_image").click(function(){
        image_id = $(this).data('image_id');
        
        $.ajax({
            url: '/property/update/'+image_id+'/',
            headers: {'X-CSRFToken': csrftoken},
            type: "DELETE",
            data : {'request_type':'delete_property_image'},
            success: function (data) {
                location.reload();
            },
            error: function (error) {
                console.log('erroe');
            }
        });
        
    });


});


});