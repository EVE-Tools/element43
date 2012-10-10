$(document).ready(function () {
    $.getJSON('/market/history/' + invTypeID + '/', function (data) {
        // Parse data
        var length = data.length;
        var prices = [];

        // Only proceed if there is any data

        if (length != 0) {
            
            var groupingUnits = [
                ['week', [1]],
                ['month', [1, 2, 3, 4, 6]]
            ];
            
            var counter = 0;
            
            $.each(data, function(key, val){
                prices[counter] = {
                                    type: 'line',
                                    name: mapRegionNames[counter],
                                    data: val,
                                    dataGrouping: {
                                        units: groupingUnits
                                    },
                                    tooltip: {
                                        valueDecimals: 2
                                    }
                                }
                counter++;
            });
            
            

            // Create the chart
            window.chart = new Highcharts.StockChart({
                chart: {
                    renderTo: 'history',
                    height: 400,
                    style: {
                        fontFamily: 'Helvetica, sans-serif',
                        fontSize: '12px'
                    }
                },

                rangeSelector: {
                    selected: 1
                },

                title: {
                    text: "Average Prices in " + mapRegionNames,
                    floating: true
                },

                yAxis: [{
                    title: {
                        text: 'Price'
                    },
                    lineWidth: 2
                }],

                series: prices
            });
        }
    });
});