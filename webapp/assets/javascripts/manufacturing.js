$(document).ready(function () {
    //
    // Activate tooltips
    //
    $("[rel=tooltip]").tooltip();
    
    //
    // Blueprint Search
    //
    var opts, b;
    opts = {
        'minChars':3,
        'maxHeight':800,
        'width':300,
        'serviceUrl': '/manufacturing/blueprint_search/',
        'onSelect': function(value, data){ window.location.href = "/manufacturing/calculator/" + data + "/"; },
    };
    b = $('#id_blueprint').autocomplete(opts);
    
    //
    // Inline editing of material prices
    //
    $('.editable').blur(function(event) {
      // common vars
      var material_id = $(event.target).attr('id').replace("material_", "");
      
      // update bill of materials
      // step 1: update the material price in the corresponding row
      var price = $("#material_" + material_id + "").val();
      var quantity = $("#material_quantity_" + material_id + "").text().replace(/,/g, "");
      var total = parseInt(quantity) * parseFloat(price);
      //$("#material_price_" + material_id + "").text(addCommas(sprintf("%.2f", total)));
      $("#material_price_" + material_id + "").text(addCommas(total.toFixed(2)));
      
      // step 2: update the total material price per unit
      var materials_cost_unit = 0;
      
      $('#billofmaterials tbody span[id*="material_price_"]').each(function(index, element) {
          var p = $(this).text().replace(/,/g, '');
          materials_cost_unit += parseFloat(p);
      });
      
      $("#materials_cost_total_unit").text(addCommas(materials_cost_unit.toFixed(2)));
      
      // update the cost and profit overview
      var blueprint_runs = parseInt($('#blueprint_runs').text().replace(/,/g, ""));
      
      // step 1: material cost (unit + total)
      $("#materials_cost_unit").text(addCommas(materials_cost_unit.toFixed(2)));
      $("#materials_cost_total").text(addCommas((materials_cost_unit * blueprint_runs).toFixed(2)));
      
      // step 2: total cost (unit + total)
      var blueprint_cost_unit = parseFloat($('#blueprint_cost_unit').text().replace(/,/g,""));
      var total_cost_unit = blueprint_cost_unit + materials_cost_unit;
      $('#total_cost_unit').text(addCommas(total_cost_unit.toFixed(2)));
      $('#total_cost_total').text(addCommas((total_cost_unit * blueprint_runs).toFixed(2)));
      
      // step 3: profit  (unit + total)
      var revenue_unit = parseFloat($('#revenue_unit').text().replace(/,/g, ""));
      var profit_unit = revenue_unit - total_cost_unit;
      
      if (profit_unit > 0) {
        $('#profit_unit, #profit_total').removeClass().addClass("green");
      } else {
        $('#profit_unit, #profit_total').removeClass().addClass("red");  
      }
      
      $('#profit_unit').text(addCommas(profit_unit.toFixed(2)));
      $('#profit_total').text(addCommas((profit_unit * blueprint_runs).toFixed(2)));
    });
});