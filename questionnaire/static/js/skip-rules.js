var SkipRules = (function () {
    var allRadios = $(":radio");

    var allOptions = $("select");

    var allQuestionsToSkipFromSelects = [];
    var allQuestionsToSkipFromRadios = [];
    var allHiddenQuestions = [];

    var hideQuestionById = function (id) {
        $('.form-group-question-' + id).hide();
    };
    var showQuestionById = function (id) {
        $('.form-group-question-' + id).show();
    };

    $(document).ready(function() {
        hideAllQuestions();
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
    };

    var showQuestions = function(currentlyHiddenQuestions, questionsToBeHidden) {
        $.map(currentlyHiddenQuestions, function (val, index) {
            if ($.inArray(val, questionsToBeHidden) === -1) {
                showQuestionById(val);
            }
        });
    };

    var hideAllQuestions = function() {
        var checkedRadios = $('[type="radio"]:checked');
        var selectedOptions = $('option:selected');
        var allSelectedResponses = [];
        $.merge(allSelectedResponses, checkedRadios);
        $.merge(allSelectedResponses, selectedOptions);
        questionIdsToHide = getQuestionIdsToSkip(allSelectedResponses);
        
        showQuestions(allHiddenQuestions, questionIdsToHide);
        $.map(questionIdsToHide, function(val) {hideQuestionById(val);});
        allHiddenQuestions = questionIdsToHide; 
    };

    $.map(allRadios, function (element) {
        $(element).on('change', function () {
            hideAllQuestions();
        });
    });

    $.map(allOptions, function (element) {
        $(element).on('change', function () {
            hideAllQuestions();
        });

    });
    return {getQuestionIdsToSkip: getQuestionIdsToSkip,
            showQuestions:        showQuestions,
            showQuestionById:     showQuestionById};
})();
