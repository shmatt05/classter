/**
 * Created by matan on 12/18/13.
 */
$(document).ready(function() {
    //first update new open slots counter for course (in classBox)
    $('#'+($('#classkey').val()) + ' .lblOpenSlots').text($('#openslots').val());
    $('#addtocalendar').on('click', function(e) {
        var getData = {};

        getData['course_name'] = className;
        getData['course_date'] = classDate;
        getData['start_hour'] = startHour;
        getData['end_hour'] = endHour;
        $.ajax(
            {
                url : '/create_event',
                type: "GET",
                data : getData,

                async:'false',
                success:function(data, textStatus, jqXHR)
                {

                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('בעיית תקשורת, אנא נסה שוב');
                }
            });
        e.preventDefault(); //STOP default action
    });
});