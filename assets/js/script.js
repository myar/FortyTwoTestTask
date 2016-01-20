$(document).ready(function() {
    var options = {
            beforeSubmit:  removeErrors,
            success:       showResponse,
            dataType:      'json',
        };
    $('.editForm').ajaxForm(options);
});

// Clear all error messages in the form.
function removeErrors(formData, jqForm, options) {
    var queryString = $.param(formData);
    $('ul').remove();
    $('p').remove();
    $('.saveForm').attr("disabled", "true");
    $(".spinner").show();
    $(".editForm").find('input, textarea').attr("disabled", "true");
    return true;
}

// Process form submission. If the response contains a location field,
// then the submission was a success and we should return to the new location.
// Otherwise, specify the error messages in the form.
function showResponse(responseText, options, xhr, $form) {
    $(".spinner").hide();
    $('.saveForm').removeAttr("disabled");
    $(".editForm").find('input, textarea').removeAttr("disabled")
    if (responseText.success){
          $(".saveForm").before('<p>Changes have been saved.</p>');
        }
    if (responseText.errors){
        for ( i in responseText["errors"]) {
            output='<ul class="errorlist">';
            output += "<li>" + responseText["errors"][i] + "</li>";
            output += '</ul>'
            $('.error_'+i)[0].innerHTML=output;
        }
    }
    if (responseText.success){
          window.location.href = responseText.location;
    }
}
