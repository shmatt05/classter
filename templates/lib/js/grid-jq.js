/**
 * Created by Matan on 11/26/13.
 */


$(document).ready(function() {


    // Calendar Date Limitations (Back / Forward)
    var past = new Date();
    past.addDays(-7);
    var future = new Date();
    future.addDays(14);

    $('#calendar').weekCalendar({
        data: classesTableArr,
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
        totalEventsWidthPercentInOneColumn : 100,
        readonly:true,

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
        eventNew: function(calEvent, $event) {
            displayMessage('<strong>Added event</strong><br/>Start: ' + calEvent.start + '<br/>End: ' + calEvent.end);
            alert('You\'ve added a new event. You would capture this event, add the logic for creating a new event with your own fields, data and whatever backend persistence you require.');
        },
        eventDrop: function(calEvent, $event) {
            displayMessage('<strong>Moved Event</strong><br/>Start: ' + calEvent.start + '<br/>End: ' + calEvent.end);
        },
        eventResize: function(calEvent, $event) {
            displayMessage('<strong>Resized Event</strong><br/>Start: ' + calEvent.start + '<br/>End: ' + calEvent.end);
        },
        eventClick: function(calEvent, $event) {
            openPopup(calEvent.id);
        },
        eventMouseover: function(calEvent, $event) {
            displayMessage('<strong>Mouseover Event</strong><br/>Start: ' + calEvent.start + '<br/>End: ' + calEvent.end);
        },
        eventMouseout: function(calEvent, $event) {
            displayMessage('<strong>Mouseout Event</strong><br/>Start: ' + calEvent.start + '<br/>End: ' + calEvent.end);
        },
        noEvents: function() {
            displayMessage('There are no events for this week');
        }
    });

    function displayMessage(message) {
        $('#message').html(message).fadeIn();
    }

    //$('<div id="message" class="ui-corner-all"></div>').prependTo($('body'));

});

function openPopup(classID) {
//    $.magnificPopup.open({
//        type:'inline',
//        items: {
//            src: '#test-popup'
//
//        },
//
//        closeOnContentClick: false
//
//    });
    $.magnificPopup.open({
        type:'ajax',
        items: {
            src: 'html/popup.html'

        },

        closeOnContentClick: false,
        callbacks: {
            open:function(){
                var class_id = classID;

        }
    }
});

}