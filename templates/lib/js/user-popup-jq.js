$(document).ready(function() {
    $('#classdate').val(returnDateStr(new Date(parseInt(milli))));
    $('#signupbutton').on('click',  function(e) {

        var postData = {};
        postData['class_key'] = $('#classkey').val();
        postData['class_date']
        var formURL = $(this).attr("action");
        $.ajax(
            {
                url : '/register_to_class',
                type: "POST",
                data : postData,
                dataType:'html',
                async:'false',
                success:function(data, textStatus, jqXHR)
                {

                    $("div.popup-div").html(data); // Fits Any Message - Failed And Successful!
                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('בעיית תקשורת, אנא נסה שוב');
                }
            });
        e.preventDefault(); //STOP default action

    });
    $('#back').click(function() {

       //TODO: send ajax with user id and class key, then re-render html with $("div.popup-div").html(data);
        // TODO: that way data is always up to date!
    });
});
function returnDateStr (someDate) {
    return (someDate.getDate()<10?("0"+someDate.getDate()):someDate.getDate()) + "/" +
      ((someDate.getMonth()+1)<10?("0"+(someDate.getMonth()+1)):(someDate.getMonth()+1)) + "/" +
      someDate.getFullYear();
}


