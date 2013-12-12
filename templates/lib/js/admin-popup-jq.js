/**
 * Created by matan on 12/11/13.
 */
$(document).ready(function() {
    $('#addclass').on('submit',  function(e) {

    });

    $('.chosen-select').chosen({
        no_results_text: 'לא נמצאו תוצאות',
        width: '95%'
    });

    $( "#slider-range-min" ).slider({
      range: "min",
      value: 60,
      min: 1,
      max: 180,
      slide: function( event, ui ) {
        $( "#amount" ).val(ui.value );
      }
    });
    $( "#amount" ).val($( "#slider-range-min" ).slider( "value" ) );

        $('#addclass').on('submit',  function(e) {

//        var postData = $(this).serializeArray();
//        var formURL = $(this).attr("action");
//            console.log(postData);
//        $.ajax(
//            {
//                url : formURL,
//                type: "POST",
//                data : postData,
//                dataType:'html',
//                async:'false',
//                success:function(data, textStatus, jqXHR)
//                {
//
//
//                },
//                error: function(jqXHR, textStatus, errorThrown)
//                {
//                    alert('בעיית תקשורת, אנא נסה שוב');
//                }
//            });
//        e.preventDefault(); //STOP default action

    });
});

