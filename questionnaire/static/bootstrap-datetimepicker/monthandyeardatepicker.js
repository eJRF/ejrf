$(function () {
    var $date_option = $('.date-time-picker').data('date-option');
    if ($date_option == "mm") {
        $('.date-time-picker').datepicker({
            format: "mm/yyyy",
            startView: 1,
            minViewMode: 1
        });
    } else {
        $('.date-time-picker').datepicker({
            format: "dd/mm/yyyy",
            todayHighlight: true
        });

    }

});