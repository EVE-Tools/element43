$(document).ready(function() {
  $('tr.top-tr').bind('click', function() {
    var targetOffset = $('#' + $(this).attr('data-station')).offset().top;
    $('html,body').animate({scrollTop: targetOffset},'fast');
  });
});