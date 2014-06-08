$(document).ready(function() {
    // Destroy modal when hidden to allow loading of new data
    $('body').on('hidden.bs.modal', '.modal', function () {
        $(this).removeData('bs.modal');
    });
});