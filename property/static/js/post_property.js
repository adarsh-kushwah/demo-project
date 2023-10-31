$(document).ready(function () {
    var count = parseInt($("#id_form-TOTAL_FORMS").val())-1;

    $("#id_form-0-name").attr('required', 'required');

    $("#rowAdder").click(function () {
        console.log('test')
        count ++;
        newRowAdd =
                '<div class="added_row" ><br><label for="id_form-'+count+'-name">Name:</label>' +
                '<input type="text" name="form-'+count+'-name" required="True" maxlength="20" id="id_form-'+count+'-name">' +
                
                '<label for="id_form-'+count+'-status">Status:</label>' +    
                '<select name="form-'+count+'-status" id="id_form-'+count+'-status">' +
                    '<option value="available" selected>Available</option>' +
                    '<option value="unavailable">Unavailable</option>' +
                    '<option value="maintenance">Under Maintenance</option>' +
                '</select></div>' ;
        
        $('#newinput').append(newRowAdd);
        $('#id_form-TOTAL_FORMS').val(count+1);
        //$('#id_form-INITIAL_FORMS').val(count);
    });


    $(".DeleteRow").click(function () {
        $('div.added_row:last').remove();
        count --;
        $('#id_form-TOTAL_FORMS').val(count+1);
        //$('#id_form-INITIAL_FORMS').val(count);
    });

  });

