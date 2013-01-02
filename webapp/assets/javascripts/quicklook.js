$(document).ready(function() {
    //
    // Market Quicklook for element43
    //
    // Show / Hide filters section

    $('#overview_link').click(function(e) {
        if($('#filters').is(':visible')) {
            $('#filters').slideUp();
        }
    });

    $('#ask_link').click(function(e) {
        if(!($('#filters').is(':visible'))) {
            $('#filters').slideDown();
        }
    });

    $('#bid_link').click(function(e) {
        if(!($('#filters').is(':visible'))) {
            $('#filters').slideDown();
        }
    });

    $('#region_link').click(function(e) {
        if($('#filters').is(':visible')) {
            $('#filters').slideUp();
        }
    });

    $('#mats_link').click(function(e) {
        if($('#filters').is(':visible')) {
            $('#filters').slideUp();
        }
    });

    // Sliders
    $("#security-slider").slider({
        value: 0.4,
        min: 0.0,
        max: 1.0,
        step: 0.1,
        slide: function(event, ui) {
            $("#system-security").html(ui.value);
            $("#system-security").switchClass($("#system-security").attr('class'), "sec" + (ui.value * 10), 200);
        }
    });

    $("#system-security").val($("#security-slider").slider("value"));

    $("#age-slider").slider({
        value: 8,
        min: 1,
        max: 8,
        step: 1,
        slide: function(event, ui) {
            $("#data-age").html(ui.value);
        }
    });

    $("#data-age").html($("#age-slider").slider("value"));

    // Handle Filtering
    $('#filter-button').click(
    function() {
        if (!$('#filter-button').hasClass('disabled')) {
            $('#filter-button').addClass('disabled');
            $('#filter-button').text('Loading...');

            $('#ask').load('/market/tab/ask/' + invTypeID + '/' + ($("#security-slider").slider('value') * 10) + '/' + $("#age-slider").slider('value') + '/',
                function() {
                    $('#filter-button').removeClass('disabled');
                    $('#filter-button').text('Filter Orders');
                });
            $('#bid').load('/market/tab/bid/' + invTypeID + '/' + ($("#security-slider").slider('value') * 10) + '/' + $("#age-slider").slider('value') + '/',
                function() {
                    $('#filter-button').removeClass('disabled');
                    $('#filter-button').text('Filter Orders');
                });
        }
    });
});