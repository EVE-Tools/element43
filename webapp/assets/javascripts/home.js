$(document).ready(function () {
	// Home stat loader script
	$('#stats').load('/stats/ #stats', reload())
	
	function reload(){
		setTimeout(function() { $('#stats').load('/stats/ #stats', reload()); }, 5000);
	}
});