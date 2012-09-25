$(document).ready(function () {

	var options, a;
	options = {
		'minChars':3,
		'maxHeight':800,
		'width':300,
		'serviceUrl': '/live_search/',
		'onSelect': function(value, data){ window.location.href = "/market/" + data; },
	};
	a = $('#main-search').autocomplete(options);

	// Fancy clock
	// http://www.alessioatzeni.com/blog/css3-digital-clock-with-jquery/

	// Create a newDate() UTC object
	var now = new Date();
	var min = 60 * 1000;

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

	// Tabs for quicklook

	$('#tabs a').click(function (e) {
		e.preventDefault();
		$(this).tab('show');
	})

});