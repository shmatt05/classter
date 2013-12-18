/**
 * Created by matan on 12/18/13.
 */
$(document).ready(function() {
    //first update new open slots counter for course
    $('#'+($('#classkey').val()) + ' .lblOpenSlots').text($('#openslots').val());

});