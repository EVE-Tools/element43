$(document).ready(function() {
    $.getJSON('/market/history/' + mapRegionID + '/' + invTypeID + '/', function(data) {
        // Parse data
        var data_ohlc = [],
            data_high = [],
            data_low = [],
            data_volume = [],
            length = data.length;

        // Only proceed if there is any data
        if(length !== 0) {
            for(i = 0; i < length; i++) {
                data_ohlc.push([
                data[i][0], // Timestamp
                data[i][1], // Open
                data[i][2], // High
                data[i][3], // Low
                data[i][4] // Close
                ]);

                data_high.push([
                data[i][0], // Timestamp
                data[i][2]  // High
                ]);

                data_low.push([
                data[i][0], // Timestamp
                data[i][3]  // Low
                ]);

                data_volume.push([
                data[i][0], // Timestamp
                data[i][5]  // Volume
                ]);
            }

            var groupingUnits = [
                ['day', [1, 2, 3, 4, 5, 6]],
                ['week', [1, 2, 3, 4]],
            ];

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
                    selected: 4,
                    inputEnabled: false
                },

                title: {
                    text: mapRegionName,
                    floating: true
                },

                yAxis: [{
                    title: {
                        text: 'Price'
                    },
                    height: 200,
                    lineWidth: 2
                }, {
                    title: {
                        text: 'Volume'
                    },
                    top: 200,
                    height: 100,
                    gridLineWidth: 0,
                    offset: 0,
                    lineWidth: 2,
                    labels: {
                        enabled: false
                    }
                }],

                series: [{
                    type: 'candlestick',
                    name: invTypeName,
                    data: data_ohlc,
                    dataGrouping: {
                        units: groupingUnits
                    },
                    tooltip: {
                        valueDecimals: 2
                    }
                }, {
                    type: 'column',
                    name: 'Volume',
                    data: data_volume,
                    dataGrouping: {
                        units: groupingUnits
                    },
                    yAxis: 1
                }]
            });
        }
    });
});