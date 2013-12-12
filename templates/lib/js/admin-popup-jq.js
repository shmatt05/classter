/**
 * Created by matan on 12/11/13.
 */
$(document).ready(function() {
    $('#addclass').on('submit',  function(e) {

    });

    $('.chosen-select').chosen({
        no_results_text: 'לא נמצאו תוצאות',
        width: '95%'
    });

    $( "#slider-range-min" ).slider({
      range: "min",
      value: 60,
      min: 1,
      max: 180,
      slide: function( event, ui ) {
        $( "#amount" ).val(ui.value );
      }
    });
    $( "#amount" ).val($( "#slider-range-min" ).slider( "value" ) );
});

