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

   initDepthArr();
    setClassesOnGrid(classList);
    setClassClashes();
    $('.classBox').click(function() {
        $.magnificPopup.open({
  items: {
    src: '#test-popup',
    type: 'inline'
  }
});
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

        var fixedHour = startHour-6; // Clash Array only holds 18 out of 24 hours

        var startDay = parseInt(oneClass.dayOfWeek);
        var clashLength = 60*parseFloat(oneClass.classLength) + startMinutes;
        clashLength = Math.ceil(clashLength/60);
        // Fill array with "clash map"
        // tempMax saves the number of maximum clashes for this clash

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
        console.log (bottomWidth + " " + (bottomWidth / 2))

       $divOverlay.css('top', bottomTop);
       $divOverlay.css('left', bottomLeft);
       $divOverlay.css('width', function() {
           return (parseFloat(bottomWidth) / oneClass.shareWidth);
       });
        $divOverlay.css('height', classLength);
        $divOverlay.append("<p>Testing 1 2 3 "+ oneClass.classID +"</p>");
    }

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
    console.log('now starting..');
    $(".classBox").each(function( index ) {
        console.log( index + ": " + $( this ).attr('id') );
    });
}