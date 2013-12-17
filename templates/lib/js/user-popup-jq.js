$(document).ready(function() {

    $('#signupbutton').on('click',  function(e) {

        var postData = {};
        postData['class_key'] = $('#classkey').val();

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


