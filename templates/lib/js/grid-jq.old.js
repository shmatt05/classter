var classList = [
    {
        "classID": "6473",
        "classLength": "1.5",
        "dayOfWeek": "0",
        "timeOfDay": "0910",
        "colorCode": "#FFCC66",
        "shareWidth":2
    },
    {
        "classID": "4345",
        "classLength": "0.7",
        "dayOfWeek": "0",
        "timeOfDay": "0950",
        "colorCode": "#33FFAD",
        "shareWidth":2
    },
    {
        "classID": "1122",
        "classLength": "3",
        "dayOfWeek": "5",
        "timeOfDay": "1743",
        "colorCode": "#FF6699",
        "shareWidth":1
    }];

var depthArr;
var classArr;
var hourHeight = 75; // Macro for row height



$(document).ready(function() {

    $('.classBox').click(function() {
        var classKey = $(this).attr('id');
        $('#classkey').val(classKey);
//        $.magnificPopup.open({
//                type:'ajax',
//            items: {
//                src: 'html/user-popup.html'
//
//            },
//
//            closeOnContentClick: false,
//            ajax: {
//                data:({
//                    'classID':classKey
//                })
//            }
//
//        });
        $.magnificPopup.open({
            type:'inline',
            items: {
                src: '#test-popup'

            },

            closeOnContentClick: false

        });

    });

    $("#signup").submit(function(e)
    {
        var postData = $(this).serializeArray();
        var formURL = $(this).attr("action");
        $.ajax(
            {
                url : formURL,
                type: "POST",
                data : postData,
                success:function(data, textStatus, jqXHR)
                {
                   result = parseInt(data);
                   if (result === 100) { // Successful signup for course
                       alert('ההרשמה עברה בהצלחה, יום טוב!');
                       var classLabel = '#lbl' +  $('#classkey').val();
                       var newCount = parseInt($(classLabel).text()) - 1;

                       $(classLabel).text(newCount);
                       $.magnificPopup.close();

                   }
                   else if (result === 200) {
                       alert('השיעור מלא, אנא נסה להרשם לשיעור אחר');
                   }
                   else if (result === 300) {
                       alert('הינך רשום כבר לשיעור זה');
                       $.magnificPopup.close();
                   }
                   else {
                       alert('ארעה תקלה, נסה שנית');
                       $.magnificPopup.close();
                   }
                },
                error: function(jqXHR, textStatus, errorThrown)
                {
                    alert('ארעה תקלה, נסה שנית');
                }
            });
        e.preventDefault(); //STOP default action
    });
});





function setClassesOnGrid(oneClass) {
    console.log(oneClass);
    var selectorStr = "" ;
    selectorStr+=oneClass.dayOfWeek;
    selectorStr+=oneClass.timeOfDay.substr(0,2);
    var startMinutes = parseInt(oneClass.timeOfDay.substr(2));

    // Take care of potential clashing between classes visually (overlap fix)
    var startHour = parseInt(oneClass.timeOfDay.substr(0,2));

    var fixedHour = startHour-6; // Clash Array only holds 18 out of 24 hours

    var startDay = parseInt(oneClass.dayOfWeek);
    var clashLength = 60*parseFloat(oneClass.classLength) + startMinutes;
    clashLength = Math.ceil(clashLength/60);

    // Fill array with "clash map"
    for (var j=fixedHour; j<(fixedHour+parseInt(clashLength)); j++) {

        depthArr[startDay][j]++;
    }

    //classArrStr saves day of week, starting and end time for each course, for future reference of clashes
    var classArrStr = oneClass.dayOfWeek.toString() + "," + startHour.toString() + "," + (startHour + clashLength).toString();
    classArr.push(classArrStr);
    console.log(classArrStr);

    //Start positioning new class on grid
    selectorStr+="00";
    var $divToSet=$('#'+selectorStr);

    var classLength = hourHeight*parseFloat(oneClass.classLength);

    d=document.createElement('div');
    $(d).attr('id', oneClass.classID);
    document.body.appendChild(d);
    $(d).addClass('classBox');
    $(d).addClass('clearfix');
    $(d).addClass('open-popup-link');
    var $divOverlay= $(d);
    $divOverlay.css('position','absolute');
    $divOverlay.css('background-color',oneClass.colorCode);
    var rowPos = $divToSet.offset();
    var bottomTop = rowPos.top;
    bottomTop = bottomTop + (startMinutes/60)*hourHeight;
    var bottomLeft = rowPos.left;
    var bottomWidth =  $divToSet.css('width');

    $divOverlay.css('top', bottomTop);
    $divOverlay.css('left', bottomLeft);
    $divOverlay.css('width', bottomWidth);


    $divOverlay.css('height', classLength);

    var openSlots = parseInt(oneClass.maxSlots) - parseInt(oneClass.takenSlots);
    var labelName = 'lbl' + oneClass.classID;
    $divOverlay.append("<p>" + oneClass.className + "<br>" +  oneClass.instructor + "<br>Studio: " + oneClass.studioID + "<br><label id=" + labelName +" class='classLabels'>"+ openSlots +"</label> </p>");




}

function initDepthArr() {
    depthArr=new Array(7);
    classArr= new Array();
    for (var i=0; i<7; i++) {
        depthArr[i] = new Array(18)
    }


    for ( i=0; i<7; i++) {
        for (var j=0; j<18; j++) {
            depthArr[i][j] = 0;
        }
    }

}

function setClassClashes(){
    var classInfo; // string built while class was added to grid
    var tempMax; // keep max clash for one class
    $(".classBox").each(function( index ) {

        tempMax = 0;
        classInfo = classArr[index].split(","); // split into arr
        var classDay = parseInt(classInfo[0]);
        var classStartHour = parseInt(classInfo[1]) -6;
        var classEndHour = classStartHour + parseInt(classInfo[2]) -6;
        for (var i=classStartHour; i<classEndHour; i++) {
            if (tempMax < depthArr[classDay][i]) {
                tempMax = depthArr[classDay][i];
            }
        }
        $(this).css('width', function() {
            return parseFloat(parseFloat($(this).css('width')) / tempMax);
        });
    });
}