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
	
	// Fancy clock
	// http://www.alessioatzeni.com/blog/css3-digital-clock-with-jquery/

  // Create a newDate() UTC object
	var now = new Date();
	var min = 60*1000;
	
  // Output the day, date, month and year   
  $('#date').html("EVE Time ");

  setInterval(function () {
			now = new Date();
      // Create a newDate() object and extract the seconds of the current time on the visitor's
      var seconds = new Date(now.getTime() + (now.getTimezoneOffset() * min)).getSeconds();
      // Add a leading zero to seconds value
      $("#sec").html((seconds < 10 ? "0" : "") + seconds);
  }, 1000);

  setInterval(function () {
			now = new Date();
      // Create a newDate() object and extract the minutes of the current time on the visitor's
      var minutes = new Date(now.getTime() + (now.getTimezoneOffset() * min)).getMinutes();
      // Add a leading zero to the minutes value
      $("#min").html((minutes < 10 ? "0" : "") + minutes);
  }, 1000);

  setInterval(function () {
			now = new Date();
      // Create a newDate() object and extract the hours of the current time on the visitor's
      var hours = new Date(now.getTime() + (now.getTimezoneOffset() * min)).getHours();
      // Add a leading zero to the hours value
      $("#hours").html((hours < 10 ? "0" : "") + hours);
  }, 1000);
});