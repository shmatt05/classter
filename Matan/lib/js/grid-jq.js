 $(document).ready(function() {
    var $divToSet = $('#41800');
    var $divOverlay=$('#class1');
    var rowPos = $divToSet.position();
    var bottomTop = rowPos.top;
    var bottomLeft = rowPos.left;
    var bottomWidth = $divToSet.css('width');
    var bottomHeight = $divToSet.css('height');
    $divOverlay.css('top', bottomTop);
    $divOverlay.css('left', bottomLeft);
    $divOverlay.css('width', bottomWidth);
    $divOverlay.css('height', bottomHeight);

 });