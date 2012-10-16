$(document).ready(function() {
    // Destroy modal when hidden to allow loading of new data
    $('body').on('hidden', '.modal', function () {
        $(this).removeData('modal');
    });
});