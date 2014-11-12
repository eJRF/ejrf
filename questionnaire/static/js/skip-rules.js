var SkipRules = (function () {
    var allRadios = $(":radio");
    var allOptions = $("select");

    var allHiddenQuestions = [];
    var allHiddenSubsections = [];

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

    var allHiddenQuestions = [];

    var hideSubsectionById = function (id) {
        $('#subsection-' + id + '-content').hide();
    };
    var showSubsectionById = function (id) {
        $('#subsection-' + id + '-content').show();
    };

    $(document).ready(function() {
        hideAllSubsections();
    });

    var getSubsectionIdsToSkip = function (selectedElements) {
        var elements = $.map(selectedElements, function (val) {
                            if (val.attributes['data-skip-subsection']) {
                                return val.attributes['data-skip-subsection'].value.split(",");
                            } else {
                                return '';
                            }
                        });
        return $.grep(elements, function (val, index) {
                return val !== '';
            });
    };

    var showSubsections = function(currentlyHiddenSubsections, SubsectionsToBeHidden) {
        $.map(currentlyHiddenSubsections, function (val, index) {
            if ($.inArray(val, SubsectionsToBeHidden) === -1) {
                showSubsectionById(val);
            }
        });
    };

    var hideAllSubsections = function() {
        var checkedRadios = $('[type="radio"]:checked');
        var selectedOptions = $('option:selected');
        var allSelectedResponses = [];
        $.merge(allSelectedResponses, checkedRadios);
        $.merge(allSelectedResponses, selectedOptions);
        SubsectionIdsToHide = getSubsectionIdsToSkip(allSelectedResponses);
        
        showSubsections(allHiddenSubsections, SubsectionIdsToHide);
        $.map(SubsectionIdsToHide, function(val) {hideSubsectionById(val);});
        allHiddenSubsections = SubsectionIdsToHide; 
    };


    $.map(allRadios, function (element) {
        $(element).on('change', function () {
            hideAllQuestions();
            hideAllSubsections();
        });
    });

    $.map(allOptions, function (element) {
        $(element).on('change', function () {
            hideAllQuestions();
            hideAllSubsections();
        });

    });
    return {getQuestionIdsToSkip: getQuestionIdsToSkip,
            showQuestions:        showQuestions,
            showQuestionById:     showQuestionById};
})();
