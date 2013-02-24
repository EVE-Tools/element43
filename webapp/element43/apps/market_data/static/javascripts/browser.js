$(document).ready(function() {
	$('#tree').dynatree({
		title: "market",
		// Tree's name
		autoCollapse: true,
		// Auto-collapse other branches
		imagePath: " ",
		// Path to a folder containing icons.
		initAjax: {
			url: "/market/browse/tree/"
		},
		// Initial AJAX location
		fx: {
			height: "toggle",
			duration: 200
		},
		// Animation
		onLazyRead: function(node) {
			node.appendAjax({
				url: "/market/browse/tree/" + node.data.key + "/"
			}); // AJAX URL
		},
		onActivate: function(node) {
			if(node.data.hasItems) {
				$('#group').load('/market/browse/panel/' + node.data.key + '/'); // Load right panel
			}
		},
		onPostInit: function(isReloading, isError) {
			// If load_path defined load path
			if(typeof load_path !== 'undefined') {
				this.loadKeyPath(load_path, function(node, status) {
					if(status == "loaded") {
						// 'node' is a parent that was just traversed.
						// If we call expand() here, then all nodes will be expanded
						// as we go
						node.expand();
					} else if(status == "ok") {
						// 'node' is the end node of our path.
						// If we call activate() or makeVisible() here, then the
						// whole branch will be exoanded now
						node.activate();
					} else if(status == "notfound") {
						var seg = arguments[2],
							isEndNode = arguments[3];
					}
				});

			}
		}
	});
});