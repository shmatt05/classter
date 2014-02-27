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
                $('#'+classesTableArr[i].id + ' .lblOpenSlots').text(classesTableArr[i].openSlots+ ' מקומות');
                 $('#'+classesTableArr[i].id).css('background-color',classesTableArr[i].color);
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
              //  $event.css('backgroundColor', '#aaa');
                $event.css('opacity', '0.5');

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
            editCoursePopup( calEvent.start,calEvent.id);
            // manageCoursePopup(calEvent.id, calEvent.start);
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

    $("#instructorselect").chosen().change(function() {
        var fullName = $(this).val().split(' ');

        $('#instructorid').val($('#instructorselect option:selected').data('tid'));
        $('#instructorfirstname').val(fullName[0]);
        $('#instructorlastname').val(fullName[1]);


    });
    $("#studioselect").chosen().change(function() {
        $('#studioname').val($(this).val());

    });
    $("#classselect").chosen().change(function() {
        $('#classname').val($(this).val());
        $("#classcolor").spectrum("set", $('#classselect option:selected').data('color'));
        $('#classdescription').val($('#classselect option:selected').data('description'))
    });



    $("#userselect").chosen().change(function() {
        var fullName = $(this).val().split(' ');
        $('#userid').val(fullName[0]);
        $('#userfirstname').val(fullName[1]);
        $('#userlastname').val(fullName[2]);
        $('#useremail').val($('#userselect option:selected').data('email'));
        $('#userphone').val($('#userselect option:selected').data('phone'));

    });


    // All Delete Buttons AJAX
    $('#deleteinstructor').on('click',  function(e) {
        var postData = {};
        postData['instructor_id'] = $('#instructorid').val();
        $.ajax(
            {
                url : '/delete_instructor',
                type: "POST",
                data : postData,
                async:'false',
                success:function(data, textStatus, jqXHR)
                {
                    $('#instructorselect').find('option:selected').remove();
                    $('#instructorselect').trigger('chosen:updated');
                    $('#instructorid').val('');
                    $('#instructorfirstname').val('');
                    $('#instructorlastname').val('');
                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('בעיית תקשורת, אנא נסה שוב');
                }
            });
        e.preventDefault();
    });
    $('#deletestudio').on('click',  function(e) {
        var postData = {};
        postData['studio_name'] = $('#studioname').val();
        $.ajax(
            {
                url : '/delete_studio',
                type: "POST",
                data : postData,
                async:'false',
                success:function(data, textStatus, jqXHR)
                {
                    $('#studioselect').find('option:selected').remove();
                    $('#studioselect').trigger('chosen:updated');
                    $('#studioname').val('');
                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('בעיית תקשורת, אנא נסה שוב');
                }
            });
        e.preventDefault();
    });
    $('#deleteclass').on('click',  function(e) {
        var postData = {};
        postData['name'] = $('#classname').val();
        $.ajax(
            {
                url : '/delete_course_template',
                type: "POST",
                data : postData,
                async:'false',
                success:function(data, textStatus, jqXHR)
                {
                    $('#classselect').find('option:selected').remove();
                    $('#classselect').trigger('chosen:updated');
                    $('#classname').val('');
                    $('#classdescription').val('');
                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('בעיית תקשורת, אנא נסה שוב');
                }
            });
        e.preventDefault();
    });

    $('#deleteuser').on('click',  function(e) {
        var postData = {};
        postData['user_id'] = $('#userid').val();
        $.ajax(
            {
                url : '/delete_user',
                type: "POST",
                data : postData,
                async:'false',
                success:function(data, textStatus, jqXHR)
                {

                    $('#userselect').find('option:selected').remove();
                    $('#userselect').trigger('chosen:updated');
                    $('#userid').val('');
                    $('#userfirstname').val('');
                    $('#userlastname').val('');
                    $('#useremail').val('');
                    $('#userphone').val('');


                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('בעיית תקשורת, אנא נסה שוב');
                }
            });
        e.preventDefault();
    });


        // All Update Buttons AJAX

    $('#editinstructor').on('click',  function(e) {
        var postData = {};
        postData['id'] = $('#instructorid').val();
        postData['first_name'] = $('#instructorfirstname').val();
        postData['last_name'] = $('#instructorlastname').val();

        $.ajax(
            {
                url : '/edit_instructor',
                type: "POST",
                data : postData,
                async:'false',
                success:function(data, textStatus, jqXHR)
                {
                    $('#instructorselect').find('option:selected').remove();
                    $("#instructorselect").append(new Option($('#instructorfirstname').val()+' '+$('#instructorlastname').val(),$('#instructorfirstname').val()+' '+$('#instructorlastname').val()));
                    $('#instructorselect option:last-child').data('tid',postData['id'] );
                    $('#instructorselect').trigger('chosen:updated');
                    $('#instructorid').val('');
                    $('#instructorfirstname').val('');
                    $('#instructorlastname').val('');
                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('בעיית תקשורת, אנא נסה שוב');
                }
            });
        e.preventDefault();
    });
    $('#editstudio').on('click',  function(e) {
        var postData = {};
        postData['old_name'] = $('#studioselect').val();
        postData['new_name'] = $('#studioname').val();
        $.ajax(
            {
                url : '/edit_studio',
                type: "POST",
                data : postData,
                async:'false',
                success:function(data, textStatus, jqXHR)
                {
                    $('#studioselect').find('option:selected').remove();
                    $("#studioselect").append(new Option($('#studioname').val(),$('#studioname').val()));
                    $('#studioselect').trigger('chosen:updated');
                    $('#studioname').val('');
                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('בעיית תקשורת, אנא נסה שוב');
                }
            });
        e.preventDefault();
    });
    $('#editclass').on('click',  function(e) {
        var postData = {};
        postData['new_name'] = $('#classname').val();
        postData['prev_name'] = $('#classselect').val();
        postData['new_description'] = $('#classdescription').val();
        postData['new_color'] = $("#classcolor").spectrum("get").toHexString();

        $.ajax(
            {
                url : '/edit_course_template',
                type: "POST",
                data : postData,
                async:'false',
                success:function(data, textStatus, jqXHR)
                {

                    $('#classselect').find('option:selected').remove();
                    $("#classselect").append(new Option($('#classname').val(),$('#classname').val()));
                    $('#classselect option:last-child').data('color',postData['new_color'] );
                    $('#classselect option:last-child').data('description',postData['new_description'] );
                    $('#classselect').trigger('chosen:updated');
                    $('#classname').val('');
                    $('#classdescription').val('');

                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('בעיית תקשורת, אנא נסה שוב');
                }
            });
        e.preventDefault();
    });

    $('#edituser').on('click',  function(e) {
        var postData = {};
        postData['user_id'] = $('#userid').val();
        postData['first_name'] = $('#userfirstname').val();
        postData['last_name'] = $('#userlastname').val();
        postData['email'] = $('#useremail').val();
        postData['phone'] = $('#userphone').val();

        $.ajax(
            {
                url : '/edit_user',
                type: "POST",
                data : postData,
                async:'false',
                success:function(data, textStatus, jqXHR)
                {

                    $('#userselect').find('option:selected').remove();
                    $("#userselect").append(new Option($('#userid').val()+' '+$('#userfirstname').val()+' ' +$('#userlastname').val(),$('#userid').val()+' '+$('#userfirstname').val()+' ' +$('#userlastname').val()));
                    $('#userselect option:last-child').data('email',postData['email'] );
                    $('#userselect option:last-child').data('phone',postData['phone'] );
                    $('#userselect').trigger('chosen:updated');
                    $('#userid').val('');
                    $('#userfirstname').val('');
                    $('#userlastname').val('');
                    $('#useremail').val('');
                    $('#userphone').val('');


                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('בעיית תקשורת, אנא נסה שוב');
                }
            });
        e.preventDefault();
    });
    // All Add Buttons AJAX

    $('#addinstructor').on('click',  function(e) {
        $('input').each(function() {
            if(!$(this).val()){
                alert('Some fields are empty');
                return false;
            }
        });
        var postData = {};
        postData['id'] = $('#newinstructorid').val();
        postData['first_name'] = $('#newinstructorfirstname').val();
        postData['last_name'] = $('#newinstructorlastname').val();

        $.ajax(
            {
                url : '/add_instructor',
                type: "POST",
                data : postData,
                async:'false',
                success:function(data, textStatus, jqXHR)
                {
                    $("#instructorselect").append(new Option($('#newinstructorfirstname').val()+' '+$('#newinstructorlastname').val(),$('#newinstructorfirstname').val()+' '+$('#newinstructorlastname').val()));
                    $('#instructorselect option:last-child').data('tid',postData['id'] );
                    $('#instructorselect').trigger('chosen:updated');
                    $('#newinstructorid').val('');
                    $('#newinstructorfirstname').val('');
                    $('#newinstructorlastname').val('');

                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('בעיית תקשורת, אנא נסה שוב');
                }
            });
        e.preventDefault();
    });
    $('#addstudio').on('click',  function(e) {
        var postData = {};

        postData['name'] = $('#newstudioname').val();
        $.ajax(
            {
                url : '/add_studio',
                type: "POST",
                data : postData,
                async:'false',
                success:function(data, textStatus, jqXHR)
                {
                    $("#studioselect").append(new Option($('#newstudioname').val(),$('#newstudioname').val()));
                    $('#studioselect').trigger('chosen:updated');
                    $('#newstudioname').val('');
                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('בעיית תקשורת, אנא נסה שוב');
                }
            });
        e.preventDefault();
    });

    $('#addclass').on('click',  function(e) {
        var postData = {};
        postData['name'] = $('#newclassname').val();
        postData['description'] = $('#newclassdescription').val();
        postData['color'] = $("#newclasscolor").spectrum("get").toHexString();

        $.ajax(
            {
                url : '/add_course_template',
                type: "POST",
                data : postData,
                async:'false',
                success:function(data, textStatus, jqXHR)
                {

                    $("#classselect").append(new Option($('#newclassname').val(),$('#newclassname').val()));
                   $('#classselect option:last-child').data('color',postData['color'] );
                    $('#classselect option:last-child').data('description',postData['description'] );
                    $('#classselect').trigger('chosen:updated');
                    $('#newclassname').val('');
                    $('#newclassdescription').val('');

                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('בעיית תקשורת, אנא נסה שוב');
                }
            });
        e.preventDefault();
    });

    $('#adduser').on('click',  function(e) {
        var postData = {};
        postData['user_id'] = $('#newuserid').val();
        postData['first_name'] = $('#newuserfirstname').val();
        postData['last_name'] = $('#newuserlastname').val();
        postData['email'] = $('#newuseremail').val();
        postData['phone'] = $('#newuserphone').val();

        $.ajax(
            {
                url : '/add_user_to_gym',
                type: "POST",
                data : postData,
                async:'false',
                success:function(data, textStatus, jqXHR)
                {


                    $("#userselect").append(new Option($('#newuserid').val()+' '+$('#newuserfirstname').val()+' ' +$('#newuserlastname').val(),$('#newuserid').val()+' '+$('#newuserfirstname').val()+' ' +$('#newuserlastname').val()));
                    $('#userselect option:last-child').data('email',postData['email'] );
                    $('#userselect option:last-child').data('phone',postData['phone'] );
                    $('#userselect').trigger('chosen:updated');
                    $('#newuserid').val('');
                    $('#newuserfirstname').val('');
                    $('#newuserlastname').val('');
                    $('#newuseremail').val('');
                    $('#newuserphone').val('');


                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('בעיית תקשורת, אנא נסה שוב');
                }
            });
        e.preventDefault();
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
                            oneClass.color = newClass.color;
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