$(document).ready(function() {
	//
	// Market Quicklook for element43
	//
	
	// Initialize slider
	$('#slider').slider({
				value: 0.0,
				min: 0.0,
				max: 1.0,
				step: 0.1,
				slide: function(event, ui) {
					
					$('#slider-label').html('Lowest security status: ' + ui.value);
					
					// Show notice if speed is (too) fast
					if (ui.value < 3) {
						$('#speed-notice').show();
					} 
					else {
						$('#speed-notice').hide();
					}
					
					interval = $("#slider").slider("value") * 1000;
				}
			});
	$('#speed-notice').hide();
	$('#slider-label').html('Lowest security status: ' + ui.value);
	
});