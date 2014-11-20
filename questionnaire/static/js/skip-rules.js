var applySkipRules = (function () {
    var self = this;
    var allRadios = $(":radio");
    var allOptions = $("select");
    var originalGridInstance = $('.grid-group')

    var allHiddenQuestions = [];
    var allHiddenSubsections = [];

    $(document).ready(function () {
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
                var data = val.attributes[dataAttribute]
                return data && data.value.split(",");
            } else {
                return '';
            }
        });
        return $.grep(elements, function (val, index) {
            return val !== '';
        });
    };

    var showElements = function (currentlyHiddenElements, elementsToBeHidden, fnShow) {

        $.map(currentlyHiddenElements, function (val, index) {
            if ($.inArray(val, elementsToBeHidden) === -1) {
                fnShow(val);
            }
        });
    };

    var hideQuestions = function (dataAttr) {
        var checkedRadios = $('[type="radio"]:checked');
        var selectedOptions = $('option:selected');
        var allSelectedResponses = [];
        $.merge(allSelectedResponses, checkedRadios);
        $.merge(allSelectedResponses, selectedOptions);
        var questionIdsToHide = getElementsToSkip(allSelectedResponses, dataAttr);

        showElements(allHiddenQuestions, questionIdsToHide, showQuestionById);
        $.map(questionIdsToHide, function (val) {
            hideQuestionById(val);
        });
        allHiddenQuestions = questionIdsToHide;
    };

    var hideQuestionsWithinHybridGroup = function () {
        hideQuestions('data-skip-hybrid-grid-rules')
    };

    var hideAllQuestions = function () {
        hideQuestions('data-skip-rules');
    };


    var hideAllSubsections = function () {
        var checkedRadios = $('[type="radio"]:checked');
        var selectedOptions = $('option:selected');
        var allSelectedResponses = [];
        $.merge(allSelectedResponses, checkedRadios);
        $.merge(allSelectedResponses, selectedOptions);
        var subsectionIdsToHide = getElementsToSkip(allSelectedResponses, 'data-skip-subsection');

        showElements(allHiddenSubsections, subsectionIdsToHide, showSubsectionById);
        $.map(subsectionIdsToHide, function (val) {
            hideSubsectionById(val);
        });
        allHiddenSubsections = subsectionIdsToHide;
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
    return {
        getElementsToSkip: getElementsToSkip,
        showElements: showElements,
        hiddenGridQuestions: [],
        showGridQuestion: function(val, gridInstance){
            $(gridInstance).find('.form-group-question-' + val).show();
        },
        showGridElements: function (elementsToBeHidden, gridInstance) {
        var self = this;
        $.map(self.hiddenGridQuestions, function (val, index) {
                if ($.inArray(val, elementsToBeHidden) === -1) {
                    self.showGridQuestion(val, gridInstance);
                }
            });
        },
        bindSkipRulesOn: function (gridInstance) {
            var self = this;
            $(gridInstance).find('div[class^="form-group form-group-question-"]').show()
            var getallSelectedResponses =  function(){
                var checkedRadios = $(gridInstance).find('[type=radio]:checked');
                var selectedOptions = $(gridInstance).find('option:checked');
                var allSelectedResponses = [];
                $.merge(allSelectedResponses, checkedRadios);
                $.merge(allSelectedResponses, selectedOptions);
                return allSelectedResponses;
            };
            var allOptions = $(gridInstance).find('[type="radio"], select');

            $.map(allOptions, function (element) {
                $(element).off('change');
                $(element).on('change', function () {
                    var questionIdsToHide = getElementsToSkip(getallSelectedResponses(), 'data-skip-hybrid-grid-rules');
                    self.showGridElements(questionIdsToHide, gridInstance)

                    $.map(questionIdsToHide, function (val) {
                        $(gridInstance).find('.form-group-question-' + val).hide();
                    });
                    self.hiddenGridQuestions = questionIdsToHide;
                })
            })
        }
    };
})();
