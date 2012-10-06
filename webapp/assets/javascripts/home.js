$(document).ready(function () {
    
	// Generate params string for value list
    var params = ""
    $.each(types, function(index, value) {
        if (index == 0){
            params += "?type=" + value
        } else {
            params += "&type=" + value
        }
    });
    
    var url = '/stats/' + region + '/' + params
	
    // Define stat loader
    var stat_loader = function load_stats(data){
        $.each(data, function(key, val) {
            
            // Iterate over typestats or insert EMDR stats
            if (key == "typestats") {
                // Iterate over types
                $.each(val, function(type_key, type_val) {
                    // Iterate over type values
                    $.each(type_val, function(type_val_key, type_val_val){
                        // Set values
                        var element = $('#' + type_val_key + '_' + type_key)
                        var old_val = parseFloat(element.text().replace(/,/g, ""));
                        var new_val = type_val_val.toFixed(2);
                        
                        // Pulse values on change
                        if (old_val > new_val) {
                            // If new value is smaller, pulse red, remove style left over from the pulse afterwards
                            element.text(new_val.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,"));
            				 element.pulse({color: '#FF0000'}, {duration: 400}, function(){element.removeAttr("style")});
                        }
                        
                        else if (old_val < new_val) {
                            // If new value is higher, pulse green, remove style left over from the pulse afterwards
                             element.text(new_val.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,"));
                             element.pulse({color: '#50C878'}, {duration: 400}, function(){element.removeAttr("style")});
                        }
                        else {
                            // If it's just the same number don't do anything
                        }
                        
                        // Set font color depending on value on bid fields
                        if (/move/i.test(type_val_key)){
                            if (new_val > 0) {
                                // >0 => green and +
                                element.removeClass();
                                element.addClass('green')
                                
                                if(!(element.text().indexOf("+") >= 0)){
                                    element.text('+' + element.text());
                                }
                            }
                            else if (new_val < 0){
                                // <0 => red
                                element.removeClass();
                                element.addClass('red')
                            }
                            else {
                                // = 0 => white
                                element.removeClass();
                            }
                        }
                    });
                });
                
            } else {
                $('#' + key).text(val);
            }
            
          });
          
          // Schdeule next reload
          reload();
    }
    
    // Load initial dataset
    $.getJSON(url, stat_loader);
	
	function reload(){
	    setTimeout(function() {  $.getJSON(url, stat_loader); }, 5000);
	}
});