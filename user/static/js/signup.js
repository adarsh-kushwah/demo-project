
$('#user_signup_form').submit(function(e){
    confirm('Are you sure you want to sign up')
});

$('#SelectStateDropDown').click(function(e) {
    // Your event handler code here
    $.ajax({
        url: '/user/signup/',
        type: "GET",
        data: {'state':e.target.value},
        success: function (data) {
            $("#SelectCityDropDown").empty();
            $('#SelectCityDropDown').append(`<option value="">Select city</option>`);
            data.choice_list.forEach(function (item, index) {
                const opt = document.createElement("option");
                $('#SelectCityDropDown').append(`<option value="${item[1]}">${item[0]}</option>`);
            });
        },
        error: function (error) {
            console.log('erroe');
        }
    });
  });

  $('#SelectCityDropDown').click(function(e) {
    // Your event handler code here

    $.ajax({
        url: '/user/signup/',
        type: "GET",
        data: {'city':e.target.value},
        success: function (data) {
            $("#SelectPostalCodeDropDown").empty();
            $('#SelectPostalCodeDropDown').append(`<option value="">Select pincode</option>`);
            data.postal_code_list.forEach(function (item, index) {
                const opt = document.createElement("option");
                $('#SelectPostalCodeDropDown').append(`<option value="${item[1]}">${item[0]}</option>`);
            });
        },
        error: function (error) {
            console.log('erroe');
        }
    });
  });