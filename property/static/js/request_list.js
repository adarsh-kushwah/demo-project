function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;   
}


$(".reject_request").click(function(){
    let request_id = $(this).data('request_id');
    let reject_request = $(this).data('reject_request');
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/property/request-response/'+request_id+'/?reject_request='+reject_request,
        type: "DELETE",
        headers: {'X-CSRFToken': csrftoken},
        success: function (data) {
            location.reload();
        },
        error: function (error) {
            console.log('erroe');
        }
    })


})