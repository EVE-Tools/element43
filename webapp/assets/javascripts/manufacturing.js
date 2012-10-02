$(document).ready(function () {
    var boptions, b;
    boptions = {
        'minChars':3,
        'maxHeight':800,
        'width':300,
        'serviceUrl': '/manufacturing/blueprint_search/',
        'onSelect': function(value, data){ window.location.href = "/manufacturing/calculator/" + data + "/"; },
    };
    b = $('#id_blueprint').autocomplete(boptions)
});