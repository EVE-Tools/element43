$(document).ready(function() {
    //
    // Station view for element43
    //

    // Slide controls

    $('#spread_link').click(function() {
        $('#tabs').toggle("slide", 200, function(){
            $('#spread-controls').toggle("slide", 200);

            $('#menu-left').toggleClass("span3", 200);
            $('#menu-left').toggleClass("span2", 200);

            $('#panel-right').toggleClass("span9", 200);
            $('#panel-right').toggleClass("span10", 200);
        });
    });

    $('#button-back').click(function() {

        $('#menu-left').toggleClass("span3");
        $('#menu-left').toggleClass("span2");

        $('#panel-right').toggleClass("span9");
        $('#panel-right').toggleClass("span10");

        $('#spread-controls').toggle("slide", 200, function(){
            $('#tabs').toggle("slide", 200);

            $('#overview_link').trigger('click');
        });
    });

    // Get market groups and initialize tree
    $.getJSON('/static/javascripts/groups.json', function(groups) {
        $('#tree').dynatree({
            title: "market",
            // Tree's name
            autoCollapse: true,
            // Auto-collapse other branches
            imagePath: "/static/images/icons/eve/",
            // Initial AJAX location
            fx: {
                height: "toggle",
                duration: 200
            },
            // Animation
            children: groups,
            onActivate: function(node) {
                if(!node.data.isFolder) {
                    $('#group').html('<img src="/static/images/loading.gif"><i> Loading data...</i>');
                    $('#group').load('/market/trading/station/' + staStationID + '/import/browse/panel/' + node.data.key + '/', function(){$("[rel=tooltip]").tooltip();}); // Load right panel
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

    // AJAX autocomplete setup
    var options, a;
    options = {
        'minChars': 3,
        'maxHeight': 800,
        'width': 300,
        'serviceUrl': '/market/trading/live_search/',
        'onSelect': function(value, data) {
            // Forward depending on whether it's a system or region
            var id = data;
            if(id.indexOf('system_') != -1) {
                $('#import').load('/market/trading/station/' + staStationID + '/import/system/' + id.replace('system_', '') + '/', function() {
                    $("[rel=tooltip]").tooltip();
                });
            } else if(id.indexOf('region_') != -1) {
                $('#import').load('/market/trading/station/' + staStationID + '/import/region/' + id.replace('region_', '') + '/', function() {
                    $("[rel=tooltip]").tooltip();
                });
            }
        }
    };
    a = $('#import-search').autocomplete(options);

    $('#import-search').keypress(function(e) {
        if(e.which == 13) {
            $('#import').load('/market/trading/search/?query=' + encodeURIComponent($('#import-search').val()));
        }
    });
});

function loadSystem(id) {
    $('#import').load('/market/trading/station/' + staStationID + '/import/system/' + id + '/', function() {
        $("[rel=tooltip]").tooltip();
    });
}

function loadRegion(id) {
    $('#import').load('/market/trading/station/' + staStationID + '/import/region/' + id + '/', function() {
        $("[rel=tooltip]").tooltip();
    });
}