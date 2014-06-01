var pow = Math.pow,
  floor = Math.floor,
  abs = Math.abs,
  log = Math.log;

function round(n, precision) {
  var prec = Math.pow(10, precision);
  return Math.round(n * prec) / prec;
}

function abbreviateNumber(n) {
  var base = floor(log(abs(n)) / log(1000));
  var suffix = 'kMB' [base - 1];
  return suffix ? round(n / pow(1000, base), 2) + suffix : '' + n;
}

$(document).ready(function() {

  $(function() {
    $('.carousel').carousel({
      interval: 8000
    });
  });

  $('#ticker span.value').each(function() {
    var span = $(this);

    var newNum = abbreviateNumber(span.attr('data-isk'));

    if (span.hasClass('green') && newNum > 0) newNum = '+' + newNum;

    span.text(newNum);
  });


  // Generate params string for value list
  var params = "";
  $.each(types, function(index, value) {
    if (index === 0) {
      params += "?type=" + value;
    } else {
      params += "&type=" + value;
    }
  });

  var url = '/stats/' + region + '/' + params;

  // Define stat loader
  var stat_loader = function load_stats(data) {

    // Iterate over types
    $.each(data.typestats, function(type_key, type_val) {
      // Iterate over type values
      $.each(type_val, function(type_val_key, type_val_val) {
        // Set values
        var element = $('.' + type_val_key + '_' + type_key);
        var old_val = parseFloat(element.attr('data-isk'));
        var new_val = type_val_val.toFixed(2);

        // Pulse values on change
        if (old_val > new_val) {
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
        }
        if (old_val < new_val) {
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
        if (/move/i.test(type_val_key)) {
          if (new_val > 0) {
            // >0 => green and +
            element.removeClass('red');
            element.addClass('green');

            if (element.text().indexOf("+") < 0) {
              element.text('+' + element.text());
            }
          } else if (new_val < 0) {
            // <0 => red
            element.removeClass('green');
            element.addClass('red');
          } else {
            // = 0 => white
            element.removeClass('red');
            element.removeClass('green');
            element.text(' ');
          }
        }
      });
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

  $('#ticker').ticker();
});