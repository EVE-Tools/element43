$(document).ready(function () {
    //
    // Market Quicklook for element43
    //

    // Show / Hide filters section


    $('#ask_link').click(function (e) {
        if (!($('#filters').is(':visible'))) {
            $('#filters').slideDown();
        }
    });

    $('#bid_link').click(function (e) {
        if (!($('#filters').is(':visible'))) {
            $('#filters').slideDown();
        }
    })

    $('#region_link').click(function (e) {
        if ($('#filters').is(':visible')) {
            $('#filters').slideUp();
        }
    })

    $('#mats_link').click(function (e) {
        if ($('#filters').is(':visible')) {
            $('#filters').slideUp();
        }
    })

    // Sliders

    $("#security-slider").slider({
        value: 0.4,
        min: 0.0,
        max: 1.0,
        step: 0.1,
        slide: function (event, ui) {
            $("#system-security").html(ui.value);
            $("#system-security").switchClass($("#system-security").attr('class'), "sec" + (ui.value * 10), 200);
        }
    });

    $("#system-security").val($("#security-slider").slider("value"));

    $("#age-slider").slider({
        value: 8,
        min: 1,
        max: 8,
        step: 1,
        slide: function (event, ui) {
            $("#data-age").html(ui.value);
        }
    });

    $("#data-age").html($("#age-slider").slider("value"));

    // Handle filtering

    $('#filter-button').click(

    function () {
        $('#ask').load('/market/tab/ask/' + invTypeID + '/' + ($("#security-slider").slider('value') * 10) + '/' + $("#age-slider").slider('value') + '/');
        $('#bid').load('/market/tab/bid/' + invTypeID + '/' + ($("#security-slider").slider('value') * 10) + '/' + $("#age-slider").slider('value') + '/');
    });

    /**
     * Gray theme for Highcharts JS
     * @author Torstein HÃ¸nsi modified by zweizeichen for Element43
     */

    Highcharts.theme = {
        colors: ["#33b5e5", "#50C878", "#FF0000", "#E68A17", "#333333"],
        chart: {
            backgroundColor: "#121417",
            borderWidth: 0,
            borderRadius: 15,
            plotBackgroundColor: null,
            plotShadow: false,
            plotBorderWidth: 0
        },
        title: {
            style: {
                color: '#FFFFFF',
                font: '16px Helvetica, sans-serif'
            }
        },
        subtitle: {
            style: {
                color: '#FFFFFF',
                font: '12px Helvetica, sans-serif'
            }
        },
        xAxis: {
            gridLineWidth: 0,
            lineColor: '#FFFFFF',
            tickColor: '#FFFFFF',
            labels: {
                style: {
                    color: '#FFFFFF',
                    fontWeight: 'bold'
                }
            },
            title: {
                style: {
                    color: '#AAA',
                    font: 'bold 12px Helvetica, sans-serif'
                }
            }
        },
        yAxis: {
            alternateGridColor: null,
            minorTickInterval: null,
            gridLineColor: 'rgba(255, 255, 255, .2)',
            lineWidth: 0,
            tickWidth: 0,
            labels: {
                style: {
                    color: '#FFF',
                    fontWeight: 'bold'
                }
            },
            title: {
                style: {
                    color: '#AAA',
                    font: 'bold 12px Helvetica, sans-serif'
                }
            }
        },
        legend: {
            itemStyle: {
                color: '#CCC'
            },
            itemHoverStyle: {
                color: '#FFF'
            },
            itemHiddenStyle: {
                color: '#333'
            }
        },
        labels: {
            style: {
                color: '#CCC'
            }
        },
        tooltip: {
            backgroundColor: {
                linearGradient: [0, 0, 0, 50],
                stops: [
                    [0, 'rgba(96, 96, 96, .8)'],
                    [1, 'rgba(16, 16, 16, .8)']
                ]
            },
            borderWidth: 0,
            style: {
                color: '#FFF'
            }
        },


        plotOptions: {
            line: {
                dataLabels: {
                    color: '#CCC'
                },
                marker: {
                    lineColor: '#333'
                }
            },
            spline: {
                marker: {
                    lineColor: '#333'
                }
            },
            scatter: {
                marker: {
                    lineColor: '#333'
                }
            },
            candlestick: {
                lineColor: 'white'
            }
        },

        toolbar: {
            itemStyle: {
                color: '#CCC'
            }
        },

        navigation: {
            buttonOptions: {
                backgroundColor: {
                    linearGradient: [0, 0, 0, 20],
                    stops: [
                        [0.4, '#606060'],
                        [0.6, '#333333']
                    ]
                },
                borderColor: '#000000',
                symbolStroke: '#C0C0C0',
                hoverSymbolStroke: '#FFFFFF'
            }
        },

        exporting: {
            buttons: {
                exportButton: {
                    symbolFill: '#55BE3B'
                },
                printButton: {
                    symbolFill: '#7797BE'
                }
            }
        },

        // scroll charts
        rangeSelector: {
            buttonTheme: {
                fill: {
                    linearGradient: [0, 0, 0, 20],
                    stops: [
                        [0.4, '#888'],
                        [0.6, '#555']
                    ]
                },
                stroke: '#000000',
                style: {
                    color: '#CCC',
                    fontWeight: 'bold'
                },
                states: {
                    hover: {
                        fill: {
                            linearGradient: [0, 0, 0, 20],
                            stops: [
                                [0.4, '#BBB'],
                                [0.6, '#888']
                            ]
                        },
                        stroke: '#000000',
                        style: {
                            color: 'white'
                        }
                    },
                    select: {
                        fill: {
                            linearGradient: [0, 0, 0, 20],
                            stops: [
                                [0.1, '#000'],
                                [0.3, '#333']
                            ]
                        },
                        stroke: '#000000',
                        style: {
                            color: "#6EA8E5"
                        }
                    }
                }
            },
            inputStyle: {
                backgroundColor: '#333',
                color: 'silver'
            },
            labelStyle: {
                color: 'silver'
            }
        },

        navigator: {
            handles: {
                backgroundColor: '#666',
                borderColor: '#AAA'
            },
            outlineColor: '#CCC',
            maskFill: 'rgba(16, 16, 16, 0.5)',
            series: {
                color: '#7798BF',
                lineColor: '#A6C7ED'
            }
        },

        scrollbar: {
            barBackgroundColor: {
                linearGradient: [0, 0, 0, 20],
                stops: [
                    [0.4, '#888'],
                    [0.6, '#555']
                ]
            },
            barBorderColor: '#CCC',
            buttonArrowColor: '#CCC',
            buttonBackgroundColor: {
                linearGradient: [0, 0, 0, 20],
                stops: [
                    [0.4, '#888'],
                    [0.6, '#555']
                ]
            },
            buttonBorderColor: '#CCC',
            rifleColor: '#FFF',
            trackBackgroundColor: {
                linearGradient: [0, 0, 0, 10],
                stops: [
                    [0, '#000'],
                    [1, '#333']
                ]
            },
            trackBorderColor: '#666'
        },

        // special colors for some of the demo examples
        legendBackgroundColor: 'rgba(48, 48, 48, 0.8)',
        legendBackgroundColorSolid: 'rgb(70, 70, 70)',
        dataLabelsColor: '#444',
        textColor: '#E0E0E0',
        maskColor: 'rgba(255,255,255,0.3)'
    };

    // Apply the theme
    var highchartsOptions = Highcharts.setOptions(Highcharts.theme);
});