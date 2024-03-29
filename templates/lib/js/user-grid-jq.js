﻿/**
 * Created by Matan on 11/26/13.
 */
var classesTableArr = [];
var changeWeekVar = new Date().getTime();

$(document).ready(function() {

    $('#about').on('click',  function(e) {
        $.magnificPopup.open({
            type:'inline',
            items: {
                src: '#aboutpopup'

            },

            closeOnContentClick: false

        });

    });

$('#welcomediv').find('img').each(function(){
    var imgClass = (this.width/this.height > 1) ? 'wide' : 'tall';
    $(this).addClass(imgClass);
})
changeWeek(new Date().getTime()); //initialize first date screen

// Calendar Date Limitations (Back / Forward)
var past = new Date();
past.addDays(-7);
var future = new Date();
future.addDays(14);

$('#calendar').weekCalendar({
    data: function (start, end, callback) {
        callback(classesTableArr);
        for (var i=0; i<classesTableArr.length; i++) {
            $('#'+classesTableArr[i].id + ' .lblInstructor').text(classesTableArr[i].instructor);
            $('#'+classesTableArr[i].id + ' .lblOpenSlots').text(classesTableArr[i].openSlots+ ' מקומות');
            // if ($('#'+classesTableArr[i].id).css('background-color') != 'rgb(170, 170, 170)') {
            $('#'+classesTableArr[i].id).css('background-color',classesTableArr[i].color);
            //  }
            if (classesTableArr[i].isReg) {
                $('#'+classesTableArr[i].id + ' .indicator').css('background-color','#33CC33');
            }
            else {
                $('#'+classesTableArr[i].id + ' .indicator').css('background-color','#990000');
            }

        }
    },
    buttonText: {
        today:'היום',
        lastWeek:'קודם',
        nextWeek:'הבא'

    },
    use24Hour:true,
    changedate: function($calendar, date) {
        changeWeek(date.getTime());

    },
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
            //$event.css('backgroundColor', '#aaa');
            $event.css('opacity', '0.3');

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
        console.log(calEvent.id);
        openPopup(calEvent.id, calEvent.start);
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

function openPopup(classID, classMilli) {

    $.magnificPopup.open({
        type:'ajax',
        items: {
            src: '/signupopup'

        },
        ajax: {
            settings: {
                cache:false,

                type:'POST',
                data: {
                    class_key:classID,
                    class_date:returnDateStr(new Date(classMilli))
                }

            }
        },
        closeOnContentClick: false,
        callbacks: {

        }
    });

}

// Render new chosen week via AJAX
//Server Side Function That Gets Date and returns whole week of date in schedules
function changeWeek(newDate) {
    classesTableArr = [];

    $.ajax(
        {
            url : '/changeweek',
            type: "POST",
            data : {'new_date':newDate},
            async:false,
            success:function(data, textStatus, jqXHR)
            {

                var result = $.parseJSON(data);

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
                            oneClass.isReg = newClass.is_registration_open;
                            oneClass.openSlots = Math.max(newClass.max_capacity - Object.keys(newClass.users_table).length,0);
                            oneClass.instructor = newClass.instructor;
                            oneClass.studio = newClass.studio;
                            oneClass.color = newClass.color;

                            //$('#calendar').weekCalendar('updateEvent', newClass);
                            classesTableArr.push(oneClass);

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


}
function returnDateStr (someDate) {
    return (someDate.getDate()<10?("0"+someDate.getDate()):someDate.getDate()) + "/" +
        ((someDate.getMonth()+1)<10?("0"+(someDate.getMonth()+1)):(someDate.getMonth()+1)) + "/" +
        someDate.getFullYear();
}

