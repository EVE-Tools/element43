$(document).ready(function() {
  //
  // Activate tooltips
  //
  $('[rel=tooltip]').tooltip();

  //
  // Blueprint Search
  //
  var opts, b;
  opts = {
    'minChars': 3,
    'maxHeight': 800,
    'width': 300,
    'serviceUrl': '/manufacturing/blueprint_search/',
    'onSelect': function(value, data) {
      window.location.href = '/manufacturing/calculator/' + data + '/';
    }
  };
  b = $('#id_blueprint').autocomplete(opts);

  //
  // Inline editing of material prices
  //
  $('#billofmaterials').find('.editable').blur(function(event) {
    // First step is to get all values and calculate the new values
    var material_id = $(event.target).attr('id').replace('material_', '');
    var blueprint_runs = parseInt($('#blueprint_runs').text().replace(/,/g, ''), 10);
    var blueprint_cost_unit = parseFloat($('#blueprint_cost_unit').text().replace(/,/g, ''));
    var brokers_fee = parseFloat($('#brokers_fee_unit').text().replace(/,/g, ''));
    var sales_tax = parseFloat($('#sales_tax_unit').text().replace(/,/g, ''));
    var produced_units = parseInt($('#produced_units').text().replace(/,/g, ''), 10);
    var price = $('#material_' + material_id + '').val().replace(/,/g, '');
    var quantity = $('#material_quantity_' + material_id + '').text().replace(/,/g, '');
    var total = parseInt(quantity, 10) * parseFloat(price);
    var materials_cost_total = 0;

    $('#material_price_' + material_id + '').text(addCommas(total.toFixed(2)));

    $('#billofmaterials tbody span[id*=material_price_]').each(function(index, element) {
      var p = $(this).text().replace(/,/g, '');
      materials_cost_total += parseFloat(p);
    });

    var total_cost_unit = blueprint_cost_unit + (materials_cost_total / produced_units);
    var revenue_unit = parseFloat($('#revenue_unit').text().replace(/,/g, ''));
    var profit_unit = revenue_unit - total_cost_unit - sales_tax - brokers_fee;

    // Next step is to update all fields
    $('#materials_cost_unit').text(addCommas((materials_cost_total / produced_units).toFixed(2)));
    $('#materials_cost_total, #materials_cost_total_bom').text(addCommas((materials_cost_total).toFixed(2)));
    $('#materials_cost_total').text(addCommas((materials_cost_total).toFixed(2)));
    $('#total_cost_unit').text(addCommas(total_cost_unit.toFixed(2)));
    $('#total_cost_total').text(addCommas((total_cost_unit * produced_units).toFixed(2)));
    $('#profit_unit').text(addCommas(profit_unit.toFixed(2)));
    $('#profit_total').text(addCommas((profit_unit * produced_units).toFixed(2)));

    // Last thing to do is to update css classes
    if(profit_unit > 0)  {
      $('#profit_unit, #profit_total').removeClass().addClass('green');
    } else {
      $('#profit_unit, #profit_total').removeClass().addClass('red');
    }
  });
});