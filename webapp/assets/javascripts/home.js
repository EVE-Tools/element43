var pow=Math.pow, floor=Math.floor, abs=Math.abs, log=Math.log;

function round(n, precision) {
    var prec = Math.pow(10, precision);
    return Math.round(n*prec)/prec;
}

function abbreviateNumber(n) {
    var base = floor(log(abs(n))/log(1000));
    var suffix = 'kMB'[base-1];
    return suffix ? round(n/pow(1000,base),2)+suffix : ''+n;
}

$(document).ready(function() {

    // More JSON
    $.getJSON('/market/history/34/', function(data) {

        // Default data
        var invTypeID = 34;
        var invTypeName = "Tritanium";
        var mapRegionIDs = [10000002, 10000043, 10000032, 10000030];
        var mapRegions = {"10000032": "Sinq Laison", "10000002": "The Forge", "10000043": "Domain", "10000030": "Heimatar"};


        // Parse data
        var length = data.length;
        var prices = [];
        var namesParsed = $.parseJSON(mapRegions);

        // Only proceed if there is any data
        if(length !== 0) {

            var groupingUnits = [
                ['week', [1]],
                ['month', [1, 2, 3, 4, 6]]
            ];

            var counter = 0;

            $.each(data, function(key, val) {
                prices[counter] = {
                    type: 'line',
                    name: mapRegions[key],
                    data: val,
                    dataGrouping: {
                        units: groupingUnits
                    },
                    tooltip: {
                        valueDecimals: 2
                    }
                };
                counter++;
            });

            // Create the chart
            window.chart = new Highcharts.StockChart({
                chart: {
                    renderTo: 'history',
                    height: 300,
                    buttonOptions: {
                        enabled: false
                    }
                },
                scrollbar: {
                    enabled: false
                },
                rangeSelector: {
                    enabled: false
                },
                navigator: {
                    enabled : false
                },
                title: {
                    text: "Tritanium"
                },
                yAxis: {
                    title: {
                        text: 'Price'
                    },
                    lineWidth: 2
                },
                tooltip: {
                    valueDecimals: 2
                },
                series: prices
            });
        }
    });

    // Generate params string for value list
    var params = "";
    $.each(types, function(index, value) {
        if(index === 0) {
            params += "?type=" + value;
        } else {
            params += "&type=" + value;
        }
    });

    var url = '/stats/' + region + '/' + params;

    // Define stat loader
    var stat_loader = function load_stats(data) {
            $.each(data, function(key, val) {

                // Iterate over typestats or insert EMDR stats
                if(key == "typestats") {
                    // Iterate over types
                    $.each(val, function(type_key, type_val) {
                        // Iterate over type values
                        $.each(type_val, function(type_val_key, type_val_val) {
                            // Set values
                            var element = $('#' + type_val_key + '_' + type_key);
                            var old_val = parseFloat(element.attr('data-isk'));
                            var new_val = type_val_val.toFixed(2);

                            // Pulse values on change
                            if(old_val > new_val) {
                                // If new value is smaller, pulse red, remove style left over from the pulse afterwards
                                element.text(abbreviateNumber(new_val));
                                element.attr('data-isk', new_val);
                                element.pulse({
                                    color: '#FF0000'
                                }, {
                                    duration: 400
                                }, function() {
                                    element.removeAttr("style");
                                });
                            } else if(old_val < new_val) {
                                // If new value is higher, pulse green, remove style left over from the pulse afterwards
                                element.text(abbreviateNumber(new_val));
                                element.attr('data-isk', new_val);
                                element.pulse({
                                    color: '#50C878'
                                }, {
                                    duration: 400
                                }, function() {
                                    element.removeAttr("style");
                                });
                            } else {
                                // If it's just the same number don't do anything
                            }

                            // Set font color depending on value on bid fields
                            if(/move/i.test(type_val_key)) {
                                if(new_val > 0) {
                                    // >0 => green and +
                                    element.removeClass();
                                    element.addClass('green');

                                    if(element.text().indexOf("+") < 0) {
                                        element.text('+' + element.text());
                                    }
                                } else if(new_val < 0) {
                                    // <0 => red
                                    element.removeClass();
                                    element.addClass('red');
                                } else {
                                    // = 0 => white
                                    element.removeClass();
                                }
                            }
                        });
                    });

                } else {
                    $('#' + key).text(String(val).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,"));
                }

            });

            // Schdeule next reload
            reload();
        };

        // Load initial dataset
        $.getJSON(url, stat_loader);

    function reload() {
        setTimeout(function() {
            $.getJSON(url, stat_loader);
        }, 5000);
    }
});