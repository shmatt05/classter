var classList = [
    {
    "classID": "6473",
    "classLength": "1.5",
    "dayOfWeek": "0",
    "timeOfDay": "0910",
    "colorCode": "#FFCC66"
},
    {
    "classID": "4345",
    "classLength": "0.7",
    "dayOfWeek": "0",
    "timeOfDay": "0950",
    "colorCode": "#33FFAD"
},
    {
    "classID": "1122",
    "classLength": "3",
    "dayOfWeek": "5",
    "timeOfDay": "1743",
    "colorCode": "#FF6699"
}];

var depthArr;

var hourHeight = 75; // Macro for row height

$(document).ready(function() {
   initDepthArr();
    setClassesOnGrid(classList);
    $('.classBox').click(function() {
        alert($(this).attr('id'));
    });

 });



function setClassesOnGrid(classList) {
    for (var i=0; i<classList.length; i++) {
        oneClass=classList[i];
        var selectorStr = "" ;
        selectorStr+=oneClass.dayOfWeek;
        selectorStr+=oneClass.timeOfDay.substr(0,2);
        var startMinutes = parseInt(oneClass.timeOfDay.substr(2));

        // Take care of potential clashing between classes visually (overlap fix)
        var startHour = parseInt(oneClass.timeOfDay.substr(0,2));
        var startDay = parseInt(oneClass.dayOfWeek);
        var clashLength = 60*parseFloat(oneClass.classLength) + startMinutes;
        clashLength = Math.ceil(clashLength/60);
        var fixedHour = startHour-6;

        for (var j=fixedHour; j<(fixedHour+parseInt(clashLength)); j++) {
            //console.log(fixedHour+" "+(fixedHour+parseInt(clashLength))+ " "+ depthArr[startDay][j]);
            depthArr[startDay][j]++;
        }

        selectorStr+="00";
        var $divToSet=$('#'+selectorStr);

        var classLength = hourHeight*parseFloat(oneClass.classLength);

        d=document.createElement('div');
        $(d).attr('id', oneClass.classID);
        document.body.appendChild(d);
        $(d).addClass('classBox');
        var $divOverlay= $(d);
        $divOverlay.css('position','absolute');
        $divOverlay.css('background-color',oneClass.colorCode);
        var rowPos = $divToSet.position();
        var bottomTop = rowPos.top;
        bottomTop = bottomTop + (startMinutes/60)*hourHeight;
        var bottomLeft = rowPos.left;
        var bottomWidth = $divToSet.css('width')

        $divOverlay.css('top', bottomTop);
        $divOverlay.css('left', bottomLeft);
        $divOverlay.css('width', bottomWidth);
        $divOverlay.css('height', classLength);
        $divOverlay.append("<p>Testing 1 2 3 "+ oneClass.classID +"</p>");
    }

}

function initDepthArr() {
    depthArr=new Array(7);
    for (var i=0; i<7; i++) {
        depthArr[i] = new Array(18)
    }


    for ( i=0; i<7; i++) {
        for (var j=0; j<18; j++) {
            depthArr[i][j] = 0;
        }
    }

}

