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
                    var dt = new Date(postData['date'].replace(/(\d{2})\/(\d{2})\/(\d{4})/,'$3-$2-$1'));
                    $("#calendar").weekCalendar("gotoWeek", dt);


                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('בעיית תקשורת, אנא נסה שוב');
                }
            });
        e.preventDefault();
    });
    $('#editclass').on('submit',  function(e) {
        var postData = {};
        postData['class_id'] = classID;
        postData['date'] = $('#date').val();
        postData['time'] = $('#time').val();
        postData['length'] = $('#amount').val();
        postData['participants'] = $('#participants').val();
        postData['class'] = $('#classname').val();
        postData['studio'] = $('#studio').val();
        postData['instructor'] = $('#instructor').val();
        postData['open_date'] = $('#opendate').val();
        postData['open_time'] = $('#opentime').val();

        var formURL = $(this).attr("action");
        $.ajax(
            {
                url : formURL,
                type: "POST",
                data : postData,
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
    // END EDIT COURSE JAVASCRIPT
    // START MANAGE COURSE JAVASCRIPT
    var selectedUserID;
    $('#selectable_signedup').selectable({
        selected: function(event, ui) {
            selectedUserID = ui.selected.value;

            $(ui.selected).addClass("ui-selected").siblings().removeClass("ui-selected");
        }
    });
    $('#selectable_waiting').selectable({
        selected: function(event, ui) {
            selectedUserID = ui.selected.value;
            $(ui.selected).addClass("ui-selected").siblings().removeClass("ui-selected");
        }
    });
    $('.chosen-manage').chosen({
        no_results_text: 'לא נמצאו תוצאות',
        width: '70%'
    });

    $( '#adduserwait' ).click(function () {
        $('#waitingnamelist').empty();
        $.ajax(
            {
                url : '/get_all_users',
                type: "POST",
                data : {},
                async:true,
                success:function(data, textStatus, jqXHR)
                {
                    var result = $.parseJSON(data);
                    for (var user in result) {

                        userObj = result[user];
                        $("#waitingnamelist").append(new Option(userObj.id +' '+ userObj.first_name + ' '+ userObj.last_name, userObj.id));


                    }
                    $('#waitingnamelist').trigger("chosen:updated");
                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('ארעה תקלה, נסה שנית');
                }
            });
        if ( $('#addwaiting').is( ":hidden" ) ) {

            $( "#addwaiting" ).slideDown( "slow" );
        } else {

            $( "#addwaiting" ).hide();
        }

    });
    $( '#adduserlist' ).click(function () {
        $('#classnamelist').empty();
        $.ajax(
            {
                url : '/get_all_users',
                type: "POST",
                data : {},
                async:true,
                success:function(data, textStatus, jqXHR)
                {
                    var result = $.parseJSON(data);
                    for (var user in result) {

                        userObj = result[user];
                        $("#classnamelist").append(new Option(userObj.id +' '+ userObj.first_name + ' '+ userObj.last_name, userObj.id));


                    }
                    $('#classnamelist').trigger("chosen:updated");
                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('ארעה תקלה, נסה שנית');
                }
            });
        if ( $('#addlist').is( ":hidden" ) ) {

            $( "#addlist" ).slideDown( "slow" );
        } else {

            $( "#addlist" ).hide();
        }

    });

    $('#adduserbutton').on('click',  function(e) {
        postData = {};
        postData['user_id'] = $('#classnamelist').val();

        postData['class_id'] = courseID;
        postData['class_date'] = dateStr;

        $.ajax(
            {
                url : '/admin_register_to_course',
                type: "POST",
                data : postData,
                dataType:'html',
                async:'false',
                success:function(data, textStatus, jqXHR)
                {

                    decData = $.parseJSON(data);
                    $('#'+decData['class_key'] + ' .lblOpenSlots').text(decData['open_slots']);
                    var magnificPopup = $.magnificPopup.instance;
                    magnificPopup.close();
                    $('#'+courseID).click();

                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('בעיית תקשורת, אנא נסה שוב');
                }
            });
    });

    $('#addwaitbutton').on('click',  function(e) {
        //TODO: Add user to waiting list, just like #adduserbutton .click
    });

    $('#removeuserlist').on('click',  function(e) {
        postData = {};
        postData['user_id'] = selectedUserID;
        postData['class_id'] = courseID;
        postData['class_date'] = dateStr;

        $.ajax(
            {
                url : '/admin_delete_from_course',
                type: "POST",
                data : postData,
                dataType:'html',
                async:'false',
                success:function(data, textStatus, jqXHR)
                {
                    decData = $.parseJSON(data);
                    $('#'+decData['class_key'] + ' .lblOpenSlots').text(decData['open_slots']);

                    var magnificPopup = $.magnificPopup.instance;
                    magnificPopup.close();
                    $('#'+courseID).click();
                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('בעיית תקשורת, אנא נסה שוב');
                }
            });
    });

    $('#removeuserwait').on('click',  function(e) {
        //TODO: Remove user to waiting list, just like #removeuserwait .click
    });

$('#popbody a').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})

});
