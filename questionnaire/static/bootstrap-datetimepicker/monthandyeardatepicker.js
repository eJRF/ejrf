$(function () {
    var dateFields = $('.date-time-picker');

    var initializeDatePicker = function (elem) {
        var fieldData = $(elem).data('date-option');
        if (fieldData == 'mm') {
            $(elem).datepicker({
                format: "mm/yyyy",
                startView: 1,
                minViewMode: 1
            });
        } else {
            $(elem).datepicker({
                format: "dd/mm/yyyy",
                todayHighlight: true
            });
        }
    };

    dateFields.map(function (_, dtField) {
        initializeDatePicker(dtField);
    });
});