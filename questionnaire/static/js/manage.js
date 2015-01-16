$(function () {
    $('#duplicate-questionnaire-form').validate({
        rules: {'questionnaire': 'required', 'year': 'required', 'name': 'required'}
    });

    var elementID = '#duplicate-questionnaire-form #id_questionnaire',
        selectQuestionnaireElement = $(elementID),
        questionnaireNameElement = $('#id_name');

    selectQuestionnaireElement.on('change', function () {
        questionnaireNameElement.val($(elementID + ' option:selected').text());
    });

    $('#id_year').on('change', function () {
        $.ajax({
            type: 'get',
            url: '/questionnaire/validate/',
            data: {year: $(this).val()},
            success: function (data) {
                var htmlContent = data.status && '<div class="alert ' + data.status + '">' + data.message + '</div>';
                $('#notification').html(htmlContent);
            }
        });
    })
});
