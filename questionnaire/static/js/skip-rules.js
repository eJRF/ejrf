var SkipRules = (function () {
    var allRadios = $(":radio");

    var allOptions = $("select");

    var allQuestionsToSkipFromSelects = [];
    var allQuestionsToSkipFromRadios = [];

    var hideQuestionById = function (id) {
        $('.form-group-question-' + id).hide();
    };
    var showQuestionById = function (id) {
        $('.form-group-question-' + id).show();
    }

    $(document).ready(function() {
        hideBasedOnRadios();
        hideBasedOnSelects();
    });

    var getQuestionIdsToSkip = function (selectedElements) {
        return selectedElements
            .map(function (index, val) {
                if (val.attributes['data-skip-rules']) {
                    return val.attributes['data-skip-rules'].value.split(",");
                } else {
                    return '';
                }
            })
            .filter(function (index, val) {
                return val !== '';
            });
    }

    var hideBasedOnRadios = function () {
        var checkedRadios = $('[type="radio"]:checked');
        var currentSkipQuestions = getQuestionIdsToSkip(checkedRadios);

        allQuestionsToSkipFromRadios.map(function (index, val) {
            if ($.inArray(val, currentSkipQuestions) == -1) {
                showQuestionById(val);
            }
        })
        allQuestionsToSkipFromRadios = currentSkipQuestions;

        $.merge([], currentSkipQuestions, allQuestionsToSkipFromSelects).map(function (val, index) {
            hideQuestionById(val);
        });
    }
    allRadios.map(function (_, element) {
        $(this).on('change', function () {
            hideBasedOnRadios();
        });
    });

    var hideBasedOnSelects = function() {
        var selectedOptions = $('option:selected');
        var currentQuestionsToSkip = getQuestionIdsToSkip(selectedOptions);

        allQuestionsToSkipFromSelects.map(function (index, val) {
            if ($.inArray(val, currentQuestionsToSkip) == -1) {
                showQuestionById(val);
            }
        })
        allQuestionsToSkipFromSelects = currentQuestionsToSkip;
        
        $.merge([], currentQuestionsToSkip, allQuestionsToSkipFromRadios).map(function (val, index) {
            hideQuestionById(val);
        });
    }

    allOptions.map(function (_, element) {
        $(this).on('change', function () {
            hideBasedOnSelects();
        });

    });
    return {getQuestionIdsToSkip: getQuestionIdsToSkip}
})();
