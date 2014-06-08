$(document).ready(function() {
  $("#pp-amount").keyup(function(){
    var amount = Number($(this).val());
    if (amount < 3.0 && amount !== 0) {
      $('#pp-note').fadeIn();
    } else {
      $('#pp-note').fadeOut();
    }
  });

  $("#pp-amount-one").keyup(function(){
    var amount = Number($(this).val());
    if (amount < 3.0 && amount !== 0) {
      $('#pp-note-one').fadeIn();
    } else {
      $('#pp-note-one').fadeOut();
    }
  });
});