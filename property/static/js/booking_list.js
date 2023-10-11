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
