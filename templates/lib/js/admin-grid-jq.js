/**
 * Created by matan on 12/5/13.
 */
var classesTableArr;
$(document).ready(function () {



    // Calendar Date Limitations (Back / Forward)
//    var past = new Date();
//    past.addDays(-7);
//    var future = new Date();
//    future.addDays(14);

// Start Weekly Customization for Calendar
    var startDate,
        endDate,
        selectCurrentWeek = function () {
            window.setTimeout(function () {
                $('#weekpicker').datepicker('widget').find('.ui-datepicker-current-day a').addClass('ui-state-active')
            }, 1);
        };
    $('#weekpicker').datepicker({
        dateFormat: 'dd/mm/yy',
        "showButtonPanel":true,
        "showOtherMonths": false,
        "selectOtherMonths": false,
        "closeText":"סיים",
        currentText:"היום",
        "isRTL":true,
        dayNamesMin:["ר","ש","ש","ר","ח","ש","ש"],
        monthNames:['ינואר','פברואר','מרץ','אפריל','מאי','יוני','יולי','אוגוסט','ספטמבר','אוקטובר','נובמבר','דצמבר'],
        "onSelect": function (dateText, inst) {
            var date = $(this).datepicker('getDate'),
                dateFormat = inst.settings.dateFormat || $.datepicker._defaults.dateFormat;
            startDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay());
            endDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay() + 6);
            $('#weekpicker').val($.datepicker.formatDate(dateFormat,date,inst.settings)); //$.datepicker.formatDate(dateFormat, startDate, inst.settings) + ' - ' + $.datepicker.formatDate(dateFormat, endDate, inst.settings)
            selectCurrentWeek();
            updateCalendarWeek(date);
        },
        "beforeShow": function () {
            selectCurrentWeek();
        },
        "beforeShowDay": function (date) {
            var cssClass = '';
            if (date >= startDate && date <= endDate) {
                cssClass = 'ui-datepicker-current-day';
            }
            return [true, cssClass];
        },
        "onChangeMonthYear": function (year, month, inst) {
            selectCurrentWeek();
        }
    }).datepicker('widget').addClass('ui-weekpicker');
    $('.ui-weekpicker').on('mousemove', 'tr', function () {
        $(this).find('td a').addClass('ui-state-hover');
    });
    $('.ui-weekpicker').on('mouseleave', 'tr', function () {
        $(this).find('td a').removeClass('ui-state-hover');
    });
    // End Customization for jQuery UI Weekly

    // Start Calendar Instance Customization
    $('#calendar').weekCalendar({
        data: changeWeek(new Date()),
        buttonText: {
            today:'היום',
            lastWeek:'קודם',
            nextWeek:'הבא'

        },
        use24Hour:true,
        changedate: function($calendar, date) {
            //TODO: Add and Parse AJAX Request for more courses when browsing through calendar
        },
        timeslotsPerHour: 4,
        defaultEventLength:4,
        timeSeparator: ' - ',
        buttons:true,
//        minDate:past,
//        maxDate:future,
        longDays:['ראשון','שני','שלישי','רביעי','חמישי','שישי','שבת'],
        longMonths:['ינואר','פברואר','מרץ','אפריל','מאי','יוני','יולי','אוגוסט','ספטמבר','אוקטובר','נובמבר','דצמבר'],
        shortMonths:['ינואר','פברואר','מרץ','אפריל','מאי','יוני','יולי','אוגוסט','ספטמבר','אוקטובר','נובמבר','דצמבר'],
        startOnFirstDayOfWeek:true,
        businessHours:{start:6, end:23, limitDisplay: true},
        dateFormat:"d/m/Y",
        allowCalEventOverlap: true,
        overlapEventsSeparate: true,
        totalEventsWidthPercentInOneColumn : 95,


        height: function($calendar) {
            return $(window).height() - $('h1').outerHeight(true);
        },
        eventRender: function(calEvent, $event) {
            if (calEvent.end.getTime() < new Date().getTime()) {
                $event.css('backgroundColor', '#aaa');
                $event.find('.time').css({
                    backgroundColor: '#999',
                    border:'1px solid #888'
                });
            }
        },
        eventNew: function(calEvent, $event) { // Added New Event
            //TODO: Open Editor?
            //TODO: Create New Class On Serverside - Send Back New UUID and Save it Client Side
        },
        eventDrop: function(calEvent, $event) { // Moved Existing Event
            //TODO: Send server edit_event parameters with class UUID -> Get Confirmation?
        },
        eventResize: function(calEvent, $event) { // Resized Existing Event
            //TODO: Send server edit_event parameters with class UUID -> Get Confirmation?
        },
        eventClick: function(calEvent, $event) { // Clicked classBox
            //TODO: Open Class Viewer / Editor
        },
        eventMouseover: function(calEvent, $event) {
            //TODO: Slightly Zoom / Add Tooltip?
        },
        eventMouseout: function(calEvent, $event) {

        }
    });

    $('#tabs').tab();
    //changeWeek(0);


});



function updateCalendarWeek(chosenDate) {
            $('#calendar').weekCalendar('gotoWeek', chosenDate);
}

// Render new chosen week via AJAX
function changeWeek(newDate) {
    classesTableArr = new Array();
    $.ajax(
            {
                url : '/changeweek',
                type: "POST",
                data : newDate,
                success:function(data, textStatus, jqXHR)
                {
                    var result = $.parseJSON(data);
                    result.shift(); // Remove 1st element of array (month/day/etc)

                    for (var day in result) {
                        dayObj = result[day].courses_list;

                        if (dayObj.length >0) {
                            for (var course in dayObj){
                                var newClass = dayObj[course];
                                var oneClass = {};
                                oneClass.id=newClass.id;
                                oneClass.start=newClass.milli;
                                oneClass.end = oneClass.start + +(parseInt(newClass.duration)*60000);
                                oneClass.title = newClass.name;
                                //$('#calendar').weekCalendar('updateEvent', newClass);
                                classesTableArr.push(oneClass);
                                console.log(classesTableArr);
                                //$('#calendar').weekCalendar('clear');
                                //$('#calendar').weekCalendar('refresh');
                            }
                        }


                    }


                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('ארעה תקלה, נסה שנית');
                }
            });
    return classesTableArr;

}
