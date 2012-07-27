$(document).ready(function() {
	$('.typeahead').typeahead();
	
	// Measure time when we last ran the live search script
	var last_run = new Date().getTime();
	
	$('#main-search').on('keyup', function(e) {
		
		// Only send request if there are more than 2 characters in the text field and if we have at least 500ms between the requests
		var now = new Date().getTime();
		
		if ($('#main-search').val().length > 2 && (now - last_run) > 500) {
			
			last_run = now;
			
			// Build URL
			var url = '/live_search/' + encodeURIComponent($('#main-search').val());
			
			// Get JSON from view
			$.getJSON(url, function(data) {
				$('#main-search').data('typeahead').source = data;
			});
		}
	});
});