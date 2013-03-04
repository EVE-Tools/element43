$(document).ready(function() {
	// Get market groups and initialize tree
	$.getJSON('/static/javascripts/groups.json', function(groups) {
		$('#tree').dynatree({
			title: "market",
			// Tree's name
			autoCollapse: true,
			// Auto-collapse other branches
			imagePath: "//image.eveonline.com/Type/",
			// Initial AJAX location
			fx: {
				height: "toggle",
				duration: 200
			},
			// Animation
			children: groups,
			onActivate: function(node) {
				if(!node.data.isFolder) {
					$('#group').append('<img src="/static/images/loading.gif"><i> Loading data...</i>');
					$('#panel').fadeOut(250);
					$('#group').load('/market/browse/panel/' + node.data.key + '/'); // Load right panel
				}
			},
			onPostInit: function(isReloading, isError) {
				// If marketGroup defined load path
				if (typeof marketGroup !== 'undefined') {
					this.activateKey(marketGroup);
				}
			}
		});
	});
});