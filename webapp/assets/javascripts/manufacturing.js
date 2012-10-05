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
    
    $('.editable').blur(function(event) {
      // common vars
      var material_id = $(event.target).attr('id').replace("material_", "");
      
      // update bill of materials
      // step 1: update the material price in the corresponding row
      var price = $("#material_" + material_id + "").val();
      var quantity = $("#material_quantity_" + material_id + "").text().trim().replace(/,/g, "");
      var total = parseInt(quantity) * parseFloat(price);
      $("#material_price_" + material_id + "").text(addCommas(sprintf("%.2f", total)));
      
      // step 2: update the total material price per unit
      var materials_cost_unit = 0;
      
      $('#billofmaterials tbody span[id*="material_price_"]').each(function(index, element) {
          var p = $(this).text().trim().replace(/,/g, '');
          materials_cost_unit += parseFloat(p);
      });
      
      $("#materials_cost_total_unit").text(addCommas(sprintf("%.2f", materials_cost_unit)));
      
      // update the cost and profit overview
      var blueprint_runs = parseInt($('#blueprint_runs').text().trim().replace(/,/g, ""));
      
      // step 1: material cost (unit + total)
      $("#materials_cost_unit").text(addCommas(sprintf("%.2f", materials_cost_unit)));
      $("#materials_cost_total").text(addCommas(sprintf("%.2f", materials_cost_unit * blueprint_runs)));
      
      // step 2: total cost (unit + total)
      var blueprint_cost_unit = parseFloat($('#blueprint_cost_unit').text().trim().replace(/,/g,""));
      var total_cost_unit = blueprint_cost_unit + materials_cost_unit;
      $('#total_cost_unit').text(addCommas(sprintf("%.2f", total_cost_unit)));
      $('#total_cost_total').text(addCommas(sprintf("%.2f", total_cost_unit * blueprint_runs)));
      
      // step 3: profit  (unit + total)
      var revenue_unit = parseFloat($('#revenue_unit').text().trim().replace(/,/g, ""));
      var profit_unit = revenue_unit - total_cost_unit;
      
      if (profit_unit > 0) {
        $('#profit_unit, #profit_total').removeClass().addClass("green");
      } else {
        $('#profit_unit, #profit_total').removeClass().addClass("red");  
      }
      
      $('#profit_unit').text(addCommas(sprintf("%.2f", profit_unit)));
      $('#profit_total').text(addCommas(sprintf("%.2f", profit_unit * blueprint_runs)));
    });
});