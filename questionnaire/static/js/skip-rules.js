var SkipRules = (function () {
    var allRadios = $(":radio");
    var allOptions = $("select");

    var allHiddenQuestions = [];
    var allHiddenSubsections = [];

    $(document).ready(function() {
        hideAllQuestions();
        hideAllSubsections();
    });

    var hideQuestionById = function (id) {
        $('.form-group-question-' + id).hide();
    };
    var showQuestionById = function (id) {
        $('.form-group-question-' + id).show();
    };

    var hideSubsectionById = function (id) {
        $('#subsection-' + id + '-content').hide();
    };
    var showSubsectionById = function (id) {
        $('#subsection-' + id + '-content').show();
    };

    var getElementsToSkip = function (selectedElements, dataAttribute) {
        var elements = $.map(selectedElements, function (val) {
                            if (val.attributes[dataAttribute]) {
                                return val.attributes[dataAttribute].value.split(",");
                            } else {
                                return '';
                            }
                        });
        return $.grep(elements, function (val, index) {
                return val !== '';
            });
    }

    var showElements = function(currentlyHiddenElements, elementsToBeHidden, fnHide) {

        $.map(currentlyHiddenElements, function (val, index) {
            if ($.inArray(val, elementsToBeHidden) === -1) {
                fnHide(val);
            }
        });
    };

    var hideAllQuestions = function() {
        var checkedRadios = $('[type="radio"]:checked');
        var selectedOptions = $('option:selected');
        var allSelectedResponses = [];
        $.merge(allSelectedResponses, checkedRadios);
        $.merge(allSelectedResponses, selectedOptions);
        questionIdsToHide = getElementsToSkip(allSelectedResponses, 'data-skip-rules');
        
        showElements(allHiddenQuestions, questionIdsToHide, showQuestionById);
        $.map(questionIdsToHide, function(val) {hideQuestionById(val);});
        allHiddenQuestions = questionIdsToHide; 
    };


    var hideAllSubsections = function() {
        var checkedRadios = $('[type="radio"]:checked');
        var selectedOptions = $('option:selected');
        var allSelectedResponses = [];
        $.merge(allSelectedResponses, checkedRadios);
        $.merge(allSelectedResponses, selectedOptions);
        SubsectionIdsToHide = getElementsToSkip(allSelectedResponses, 'data-skip-subsection');
        
        showElements(allHiddenSubsections, SubsectionIdsToHide, showSubsectionById);
        $.map(SubsectionIdsToHide, function(val) {hideSubsectionById(val);});
        allHiddenSubsections = SubsectionIdsToHide; 
    };

    var allHiddenQuestions = [];

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
    return {getElementsToSkip: getElementsToSkip,
            showElements:      showElements};
})();
