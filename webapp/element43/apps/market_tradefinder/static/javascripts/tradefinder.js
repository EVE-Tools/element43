$(document).ready(function() {
	$.getJSON('/market/tradefinder/regions/', function(regions) {

		var typeaheadOptions = {
			source: regions,
			items: 8
		};

		$('#start-typeahead').typeahead(typeaheadOptions);
		$('#destination-typeahead').typeahead(typeaheadOptions);
	});
});
