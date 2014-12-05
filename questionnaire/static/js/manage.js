$(function () {
    $('#duplicate-questionnaire-form').validate({
        rules: { 'questionnaire': 'required', 'year': 'required', 'name': 'required'}
    });

    var elementID = '#duplicate-questionnaire-form #id_questionnaire',
        selectQuestionnaireElement = $(elementID),
        questionnaireNameElement = $('#id_name');

    selectQuestionnaireElement.on('change', function () {
        questionnaireNameElement.val($(elementID + ' option:selected').text());
    });

});
