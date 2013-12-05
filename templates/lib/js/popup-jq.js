$(document).ready(function() {

    $('#signup').on('submit',  function(e) {

        var postData = $(this).serializeArray();
        var formURL = $(this).attr("action");
        $.ajax(
            {
                url : formURL,
                type: "POST",
                data : postData,
                dataType:'html',
                async:'false',
                success:function(data, textStatus, jqXHR)
                {

                    $("div.popup-div").html(data);
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


