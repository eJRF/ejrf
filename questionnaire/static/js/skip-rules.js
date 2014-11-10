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

    var hideBasedOnRadios = function () {
        var checkedRadios = $('[type="radio"]:checked');
        var currentSkipQuestions = getQuestionIdsToSkip(checkedRadios);

        showQuestions(allQuestionsToSkipFromRadios, currentSkipQuestions);
        
        allQuestionsToSkipFromRadios = currentSkipQuestions;

        $.map($.merge([], currentSkipQuestions, allQuestionsToSkipFromSelects), function (val, index) {
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

        showQuestions(allQuestionsToSkipFromSelects, currentQuestionsToSkip);
        allQuestionsToSkipFromSelects = currentQuestionsToSkip;
        
        $.map($.merge([], currentQuestionsToSkip, allQuestionsToSkipFromRadios), function (val, index) {
            hideQuestionById(val);
        });
    }

    allOptions.map(function (_, element) {
        $(this).on('change', function () {
            hideBasedOnSelects();
        });

    });
    return {getQuestionIdsToSkip: getQuestionIdsToSkip,
            showQuestions:        showQuestions,
            showQuestionById:     showQuestionById}
})();
