/**
 * Created by matan on 12/11/13.
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
      value: 20,
      min: 1,
      max: 50,
      slide: function( event, ui ) {
        $( "#participants" ).val(ui.value );
      }
        });
    $( "#participants" ).val($( "#slider-range-min2" ).slider( "value" ) );

    $('#addclass').on('submit',  function(e) {

        if ($('#classname').val() === "") {
            alert('הזן את שם השיעור');
            return false;
        }
        var postData = {};
        postData['date'] = $('#date').val();
        postData['time'] = $('#time').val();
        postData['length'] = $('#amount').val();
        postData['participants'] = $('#participants').val();
        postData['class'] = $('#classname').val();
        postData['studio'] = $('#studio').val();
        postData['instructor'] = $('#instructor').val();
        postData['open_date'] = $('#opendate').val();
        postData['open_time'] = $('#opentime').val();
        postData['all_month'] = $('#allmonth').prop('checked');

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
                    var magnificPopup = $.magnificPopup.instance;
                    magnificPopup.close();
                    var dt = new Date(postData['date'].replace(/(\d{2})\/(\d{2})\/(\d{4})/,'$3-$2-$1'));
                    $("#calendar").weekCalendar("removeUnsavedEvents");
                    $("#calendar").weekCalendar("gotoWeek", dt);

                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('בעיית תקשורת, אנא נסה שוב');
                }
            });
        e.preventDefault(); //STOP default action

    });
});

