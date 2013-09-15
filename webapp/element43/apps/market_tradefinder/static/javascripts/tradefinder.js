$(document).ready(function() {
	var typeaheadOptions = {
		name: 'regionnames',
		prefetch: "/market/tradefinder/regions/"
	};

	$('#start-typeahead').typeahead(typeaheadOptions);
	$('#destination-typeahead').typeahead(typeaheadOptions);

});
