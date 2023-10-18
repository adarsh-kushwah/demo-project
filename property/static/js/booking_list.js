$('#history_button').click(function() {
    $("#booking_history").css("display","block");
    $("#current_booking").css("display","none");
    $('#history_button').css("color","blue");
    $('#current_button').css("color","black");
});

$('#current_button').click(function() {
    $("#booking_history").css("display","none");
    $("#current_booking").css("display","block");
    $('#history_button').css("color","black");
    $('#current_button').css("color","blue");
});



$('.property-rating').click(function(){
    
    let star = $(this).data('star');
    let booking_id = $(this).data('booking_id');
    let csrftoken = $('#rating-div').data('csrf_token');
    $.ajax({
        url: '/rating/property/'+booking_id+'/',
        headers: {'X-CSRFToken': csrftoken},
        type: "POST",
        data: {'star':star},
        
        success: function (data) {
            $('.fa-star').removeClass('checked');
            for(var i = 1; i <= star; i++)
            {   
                $('.star'+i).addClass('checked');
            }
        },
        error: function (error) {
            console.log('erroe');
        }
    });
})


$('.renter-rating').click(function(){
    
    let star = $(this).data('star');
    let booking_id = $(this).data('booking_id');
    let csrftoken = $('#rating-div').data('csrf_token');
    $.ajax({
        url: '/rating/renter/'+booking_id+'/',
        headers: {'X-CSRFToken': csrftoken},
        type: "POST",
        data: {'star':star},
        
        success: function (data) {
            $('.fa-star').removeClass('checked');
            for(var i = 1; i <= star; i++)
            {   
                $('.star'+i).addClass('checked');
            }
        },
        error: function (error) {
            console.log('erroe');
        }
    });
})