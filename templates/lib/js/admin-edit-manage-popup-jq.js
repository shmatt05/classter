/**
 * Created by Matan on 1/7/14.
 */
$(document).ready(function() {
    $('.chosen-select').chosen({
        no_results_text: 'לא נמצאו תוצאות',
        width: '85%%'
    });

    $( "#slider-range-min" ).slider({
        range: "min",
        value: classMinutes,
        min: 1,
        max: 180,
        slide: function( event, ui ) {
            $( "#amount" ).val(ui.value );
        }
    });
    $( "#amount" ).val($( "#slider-range-min" ).slider( "value" ) );

    $( "#slider-range-min2" ).slider({
        range: "min",
        value: classCapacity,
        min: 1,
        max: 50,
        slide: function( event, ui ) {
            $( "#participants" ).val(ui.value );
        }
    });
    $( "#participants" ).val($( "#slider-range-min2" ).slider( "value" ) );
    $('#date').data("date", classDate);
    $('#time').data('time', classTime);

     $('#deletecourse').on('click',  function(e) {
         var postData = {};
         postData['class_id'] = classID;
         postData['class_date'] = classDate;
         console.log(postData);
                $.ajax(
            {
                url : '/delete_course_instance',
                type: "POST",
                data : postData,
                async:'false',
                success:function(data, textStatus, jqXHR)
                {
                            $("#calendar").weekCalendar("removeEvent", classID);
                             var magnificPopup = $.magnificPopup.instance;
                              magnificPopup.close();

                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('בעיית תקשורת, אנא נסה שוב');
                }
            });
         e.preventDefault();
     });

});