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
        var elements = $.map(selectedElements, function (val) {
                            if (val.attributes['data-skip-rules']) {
                                return val.attributes['data-skip-rules'].value.split(",");
                            } else {
                                return '';
                            }
                        });
        return $.grep(elements, function (val, index) {
                return val !== '';
            });
    }

    var showQuestions = function(currentlyHiddenQuestions, questionsToBeHidden) {
        $.map(currentlyHiddenQuestions, function (val, index) {
            if ($.inArray(val, questionsToBeHidden) === -1) {
                showQuestionById(val);
            }
        })
    }

    var hideQuestions = function(radioQuestionsToSkip, selectQuestionsToSkip) {
        $.map($.merge($.merge([], radioQuestionsToSkip), selectQuestionsToSkip), function (val) {
            hideQuestionById(val);
        });
    }

    var hideBasedOnRadios = function () {
        var checkedRadios = $('[type="radio"]:checked');
        var currentSkipQuestions = getQuestionIdsToSkip(checkedRadios);

        showQuestions(allQuestionsToSkipFromRadios, currentSkipQuestions);        
        allQuestionsToSkipFromRadios = currentSkipQuestions;

        hideQuestions(currentSkipQuestions, allQuestionsToSkipFromSelects);
    }

    allRadios.map(function (_, element) {
        $(this).on('change', function () {
            hideBasedOnRadios();
        });
    });

    var hideBasedOnSelects = function() {
        var selectedOptions = $('option:selected');
        var currentQuestionsToSkip = getQuestionIdsToSkip(selectedOptions);

        showQuestions(allQuestionsToSkipFromSelects, currentQuestionsToSkip);
        allQuestionsToSkipFromSelects = currentQuestionsToSkip;
        
        hideQuestions(currentQuestionsToSkip, allQuestionsToSkipFromRadios);
    }

    allOptions.map(function (_, element) {
        $(this).on('change', function () {
            hideBasedOnSelects();
        });

    });
    return {getQuestionIdsToSkip: getQuestionIdsToSkip,
            showQuestions:        showQuestions,
            showQuestionById:     showQuestionById,
            hideQuestions:        hideQuestions}
})();
