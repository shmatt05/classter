var sampleClass= {
    "classID": "6473",
    "classLength": "1.5",
    "dayOfWeek": "0",
    "timeOfDay": "0910",
    "colorCode": "#FFCC66"
}
var hourHeight = 75;
$(document).ready(function() {

    setClassOnGrid(sampleClass);
    $('.classBox').click(function() {
        alert($(this).attr('id'));
    });
 });



function setClassOnGrid(oneClass) {
    var selectorStr = "" ;
    selectorStr+=oneClass.dayOfWeek;
    selectorStr+=oneClass.timeOfDay.substr(0,2);
    var startMinutes = parseInt(oneClass.timeOfDay.substr(2));
    selectorStr+="00";
    console.log(startMinutes);
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