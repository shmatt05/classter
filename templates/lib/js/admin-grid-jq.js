/**
 * Created by matan on 12/5/13.
 */
var classesTableArr = [];

var changeWeekVar = new Date().getTime();

$(document).ready(function () {

    changeWeek(new Date().getTime()); //initialize first date screen

    // Calendar Date Limitations (Back / Forward)
//    var past = new Date();
//    past.addDays(-7);
//    var future = new Date();
//    future.addDays(14);

// Start Weekly Customization for Calendar
    var startDate,
        endDate,
        selectCurrentWeek = function () {
            console.log('now in');
            window.setTimeout(function () {
                $('.week-picker').datepicker('widget').find('.ui-datepicker-current-day').find('a').addClass('white')
            }, 1);
        };
    $('.week-picker').datepicker({
        dateFormat: 'dd/mm/yy',
        "showButtonPanel":true,
        "showOtherMonths": false,
        "selectOtherMonths": false,
        "closeText":"סיים",
        currentText:"היום",
        "isRTL":true,
        dayNamesMin:["א","ב","ג","ד","ה","ו","ש"],
        monthNames:['ינואר','פברואר','מרץ','אפריל','מאי','יוני','יולי','אוגוסט','ספטמבר','אוקטובר','נובמבר','דצמבר'],
        "onSelect": function (dateText, inst) {
            var date = $(this).datepicker('getDate'),
                dateFormat = inst.settings.dateFormat || $.datepicker._defaults.dateFormat;
            startDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay());
            endDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay() + 6);
            //$('.week-picker').val($.datepicker.formatDate(dateFormat,date,inst.settings)); //$.datepicker.formatDate(dateFormat, startDate, inst.settings) + ' - ' + $.datepicker.formatDate(dateFormat, endDate, inst.settings)
            selectCurrentWeek();
            // highlight the TR
            $('.ui-datepicker-current-day').parent().addClass('highlight');

            // highlight the TD > A
            $('.ui-datepicker-current-day').siblings().find('a').addClass('white');
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
    }).click(function(event) {
            // highlight the TR
            $('.ui-datepicker-current-day').parent().addClass('highlight');

            // highlight the TD > A
            $('.ui-datepicker-current-day:eq(0)').siblings().find('a').addClass('white');
        });


    $('.week-picker').on('mousemove', 'tr', function () {
        $(this).find('td a').addClass('ui-state-hover');
    });
    $('.week-picker').on('mouseleave', 'tr', function () {
        $(this).find('td a').removeClass('ui-state-hover');
    });
    // End Customization for jQuery UI Weekly





    // Start Calendar Instance Customization
    $('#calendar').weekCalendar({
        data: function (start, end, callback) {
            //changeWeek(changeWeekVar);
            callback(classesTableArr);
            for (var i=0; i<classesTableArr.length; i++) {
                $('#'+classesTableArr[i].id + ' .lblInstructor').text(classesTableArr[i].instructor);

                $('#'+classesTableArr[i].id + ' .lblOpenSlots').text(classesTableArr[i].openSlots);
            }
        },
        buttonText: {
            today:'היום',
            lastWeek:'קודם',
            nextWeek:'הבא'

        },
        use24Hour:true,
        changedate: function($calendar, date) {
            //changeWeekVar = date.getTime();


            //console.log(classesTableArr);
            changeWeek(date.getTime());
            //$('#calendar').weekCalendar('refresh')


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
            newCoursePopup(calEvent.start, calEvent.end);

        },
        eventDrop: function(newCalEvent, calEvent, $event) { // Moved Existing Event
            editCourseNoPopup(calEvent.start,newCalEvent.start, newCalEvent.end, calEvent.id);




        },
        eventResize: function(calEvent, $event) { // Resized Existing Event
            editCourseNoPopup(calEvent.start,calEvent.start,calEvent.end, calEvent.id);
        },
        eventClick: function(calEvent, $event) { // Clicked classBox
          //  editCoursePopup( calEvent.start,calEvent.id);
            manageCoursePopup(calEvent.id, calEvent.start);
        },
        eventMouseover: function(calEvent, $event) {

        },
        eventMouseout: function(calEvent, $event) {

        }
    });

    $('#tabs').tab();

    $("#nav a").click(function(e){
        e.preventDefault();
        $('html,body').scrollTo(this.hash,this.hash);
    });

      $('.chosen-select').chosen({
        no_results_text: 'לא נמצאו תוצאות',
        width: '300px'
    });
    $("#newclasscolor").spectrum({
    color: "green"
    });
     $("#classcolor").spectrum({
    color:"#FFEBD8"
    });
});



function updateCalendarWeek(chosenDate) {
    $('#calendar').weekCalendar('gotoWeek', chosenDate);
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

                            oneClass.openSlots = newClass.max_capacity - Object.keys(newClass.users_table).length;
                            oneClass.instructor = newClass.instructor;
                            oneClass.studio = newClass.studio;
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
//Popup for creating new course
function newCoursePopup(startTime, endTime) {

    var newDate = returnDateStr(startTime);
    var newHour = returnTimeStr(startTime);
    var classMinutes = (endTime - startTime) / 60000;

    $.magnificPopup.open({
        type:'ajax',
        items: {
            src: '/newcoursepopup'

        },
        ajax: {
            settings: {
                cache:false,

                type:'POST',
                data: {
                    'course_date':newDate,
                    'course_hour':newHour,
                    'course_minutes':classMinutes

                }

            }
        },
        closeOnContentClick: false,
        callbacks: {
            close:function() {
                $("#calendar").weekCalendar("removeUnsavedEvents");
            }
        }
    });
}
//Popup that lets admin change actual course info (time,participants,intructor, etc)
function editCoursePopup(startTime, courseID) {
  var newDate = returnDateStr(startTime);
    var newHour = returnTimeStr(startTime);

    $.magnificPopup.open({
        type:'ajax',
        items: {
            src: '/edit_course_button_click'

        },
        ajax: {
            settings: {
                cache:false,

                type:'POST',
                data: {

                    'class_id':courseID,
                    'class_date':newDate,
                    'class_hour':newHour
                }

            }
        },
        closeOnContentClick: false,
        callbacks: {

        }
    });
}


//Popup that shows who is signed up to course, lets admin change list
function manageCoursePopup(courseID, startTime) {

    $.magnificPopup.open({
        type:'ajax',
        items: {
            src: '/managecoursepopup'

        },
        ajax: {
            settings: {
                cache:false,

                type:'POST',
                data: {
                    'class_id':courseID,
                    'class_date':returnDateStr(startTime)
                }

            }
        },
        closeOnContentClick: false,
        callbacks: {
            close:function() {
                //todo: maybe refresh grid after edit?
            }
        }
    });
}

function editCourseNoPopup(oldStartTime,startTime, endTime, courseID) {

    postData = {};
    postData['old_date'] = returnDateStr(oldStartTime);
    postData['new_date'] = returnDateStr(startTime);
    postData['new_hour'] = returnTimeStr(startTime);
    postData['new_minutes'] = (endTime - startTime) / 60000;
    postData['course_id']=courseID;
    $.ajax(
        {
            url : '/editcoursetime',
            type: "POST",
            data : postData,
            dataType:'text',
            async:'true',
            cache:'false',
            success:function(data, textStatus, jqXHR)
            {

                updateCalendarWeek(startTime);
//                var result = $.parseJSON(data)
//                $('#'+courseID + ' .lblInstructor').text(result['instructor']);
//
//                $('#'+courseID + ' .lblOpenSlots').text(result['open_slots']);
            },
            error: function(jqXHR, textStatus, errorThrown)
            {
                alert('בעיית תקשורת, אנא נסה שוב');
            }
        });




}


function returnDateStr (someDate) {
    return (someDate.getDate()<10?("0"+someDate.getDate()):someDate.getDate()) + "/" +
        ((someDate.getMonth()+1)<10?("0"+(someDate.getMonth()+1)):(someDate.getMonth()+1)) + "/" +
        someDate.getFullYear();
}
function returnTimeStr(someDate) {
    var someHour = (someDate.getHours() < 10? '0' : '') + someDate.getHours();
    var someMinutes = (someDate.getMinutes() < 10? '0' : '') + someDate.getMinutes();
    return (someHour + ":" + someMinutes);
}