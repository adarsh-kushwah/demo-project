$(document).ready(function () {
    $('.repeater').repeater({
      // (Optional)
      // start with an empty list of repeaters. Set your first (and only)
      // "data-repeater-item" with style="display:none;" and pass the
      // following configuration flag
      initEmpty: false,
  
      // (Optional)
      // Removes the delete button from the first list item, [defaults to false]
      isFirstItemUndeletable: true,
  
      // (Optional)
      // Call while add the element
      show: function () {
        $(this).slideDown();
        $(this).find('[data-repeater-create]').remove()
      },
  
      // (Optional)
      // Call while delete the element
      hide: function (deleteElement) {
        if (confirm('Are you sure you want to delete this element?')) {
          $(this).slideUp(deleteElement);
        }
      },
    })




    $("#rowAdder").click(function () {
        newRowAdd =
            ' <label for="id_form-0-name">Name:</label>' +
            '<input type="text" name="form-0-name" maxlength="20" id="id_form-0-name">' +
            '<label for="id_form-0-status">Status:</label>' +
            '<select name="form-0-status" id="id_form-0-status">' +
          '<option value="available" selected>Available</option>' +
          '<option value="unavailable">Unavailable</option>' +
          '<option value="maintenance">Under Maintenance</option>' +
            '</select>' ;

        $('#newinput').append(newRowAdd);
    });
    $("body").on("click", "#DeleteRow", function () {
        $(this).parents("#row").remove();
    })



  });

