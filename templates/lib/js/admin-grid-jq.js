/**
 * Created by matan on 12/5/13.
 */
$(document).ready(function () {



    // Calendar Date Limitations (Back / Forward)
    var past = new Date();
    past.addDays(-7);
    var future = new Date();
    future.addDays(14);

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
        "showOtherMonths": false,
        "selectOtherMonths": false,
        "onSelect": function (dateText, inst) {
            var date = $(this).datepicker('getDate'),
                dateFormat = inst.settings.dateFormat || $.datepicker._defaults.dateFormat;
            startDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay());
            endDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay() + 6);
            $('#weekpicker').val($.datepicker.formatDate(dateFormat,date,inst.settings)); //$.datepicker.formatDate(dateFormat, startDate, inst.settings) + ' - ' + $.datepicker.formatDate(dateFormat, endDate, inst.settings)
            selectCurrentWeek();
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

    $('#calendar').weekCalendar({
        data: null,
        buttonText: {
            today:'היום',
            lastWeek:'קודם',
            nextWeek:'הבא'

        },
        use24Hour:true,
        timeslotsPerHour: 4,
        defaultEventLength:4,
        timeSeparator: ' - ',
        buttons:true,
        minDate:past,
        maxDate:future,
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



});



