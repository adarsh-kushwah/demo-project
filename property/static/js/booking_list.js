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
    let csrftoken = $('.review_rating_div').data('csrf_token');
    $.ajax({
        url: '/rating/property/'+booking_id+'/',
        headers: {'X-CSRFToken': csrftoken},
        type: "POST",
        data: {'star':star},
        
        success: function (data) {
            $('.property-rating-'+booking_id).removeClass('checked');
            for(var i = 1; i <= star; i++)
            {   
                $('.star-'+booking_id+'-'+i).addClass('checked');
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
    let csrftoken = $('.review_rating_div').data('csrf_token');
    $.ajax({
        url: '/rating/renter/'+booking_id+'/',
        headers: {'X-CSRFToken': csrftoken},
        type: "POST",
        data: {'star':star},
        
        success: function (data) {
            $('.renter-rating-'+booking_id).removeClass('checked');
            for(var i = 1; i <= star; i++)
            {   
                $('.star-'+booking_id+'-'+i).addClass('checked');
            }
        },
        error: function (error) {
            console.log('erroe');
        }
    });
})


$('.submit_property_review').click(function(){
    let csrftoken = $('.review_rating_div').data('csrf_token');
    let booking_id = $(this).data('booking_id');
    let form_data = $(".review_form-"+booking_id).serialize();
    let reportValidity = $(".review_form-"+booking_id)[0].reportValidity();
    if(reportValidity){
        $.ajax({
            url: '/rating/property-review/'+booking_id+'/',
            headers: {'X-CSRFToken': csrftoken},
            type: "POST",
            data: form_data,
            dataType: 'json',
            success: function (data) {
                console.log('sucess');
                $('#property_review_'+booking_id).text('Your review : '+data['description']);
            },
            error: function (error) {
                console.log('erroe');
            }
        })
    }
    else{
        console.log('error')
    }
})


$('.submit_renter_review').click(function(){
    let csrftoken = $('.review_rating_div').data('csrf_token');
    let booking_id = $(this).data('booking_id');
    let form_data = $(".review_form-"+booking_id).serialize();
    let reportValidity = $(".review_form-"+booking_id)[0].reportValidity();
    if(reportValidity){
        $.ajax({
            url: '/rating/renter-review/'+booking_id+'/',
            headers: {'X-CSRFToken': csrftoken},
            type: "POST",
            data: form_data,
            dataType: 'json',
            success: function (data) {
                $('#renter_review_'+booking_id).text('Your review : '+data['description']);
            },
            error: function (error) {
                console.log('erroe');
            }
        })
    }
    else{
        console.log('erroe')
    }
})