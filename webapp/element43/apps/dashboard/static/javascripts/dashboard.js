$(document).ready(function() {
    // Destroy modal when hidden to allow loading of new data
    $('body').on('hidden.bs.modal', '.modal', function () {
        $(this).removeData('bs.modal');
    });

    $.getJSON('/secure/dashboard/journal/', function(data) {
        // Parse data
        var length = data.length;
        var balance = [];

        // Only proceed if there is any data
        if(length !== 0) {

            var groupingUnits = [
                ['week', [1]],
                ['month', [1, 2, 3, 4, 6]]
            ];

            var counter = 0;

            $.each(data, function(key, val) {
                balance[counter] = {
                    type: 'line',
                    name: key,
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
                rangeSelector: {
                    enabled: false
                },
                title: {
                    enabled: false
                },
                yAxis: {
                    title: {
                        text: 'Balance'
                    },
                    lineWidth: 2
                },
                tooltip: {
                    valueDecimals: 2
                },
                navigator: {
                    height: 20
                },
                series: balance
            });
        }
    });
});