var applySkipRules = (function () {
    var self = this;
    var allRadios = $(":radio"),
        allOptions = $("select"),
        allHiddenQuestions = [],
        allHiddenSubsections = [];

    $(document).ready(function () {
        hideAllQuestions();
        hideAllSubsections();
        hideElementsInScopeBy('.hybrid-group-row')
    });

    var hideElementsInScopeBy = function (scopeClass) {
        var elementsToBeHidden = $(scopeClass);
        $.map(elementsToBeHidden, function (element) {
            self.applySkipRules.bindOnChangeEventListener(element);
        });
        $.map(elementsToBeHidden, function (elementToHide) {
            self.applySkipRules.hideAllGridQuestions(elementToHide);
        })
    };

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
                var data = val.attributes[dataAttribute];
                return data && data.value.split(",");
            } else {
                return '';
            }
        });
        return $.grep(elements, function (val, _) {
            return val !== '';
        });
    };

    var showElements = function (currentlyHiddenElements, elementsToBeHidden, fnShow) {

        $.map(currentlyHiddenElements, function (val, _) {
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

    var hideAllQuestions = function () {
        hideQuestions('data-skip-rules');
    };

    var hideAllSubsections = function () {
        var checkedRadios = $('[type="radio"]:checked'),
            selectedOptions = $('option:selected'),
            allSelectedResponses = [];
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
        showGridQuestion: function (val, gridInstance) {
            $(gridInstance).find('.form-group-question-' + val).show();
        },
        showGridElements: function (elementsToBeHidden, gridInstance) {
            var self = this;
            $.map(self.hiddenGridQuestions, function (val, _) {
                if ($.inArray(val, elementsToBeHidden) === -1) {
                    self.showGridQuestion(val, gridInstance);
                }
            });
        },
        getAllSelectedResponses: function (gridInstance) {
            var checkedRadios = $(gridInstance).find('[type=radio]:checked'),
                selectedOptions = $(gridInstance).find('option:checked'),
                allSelectedResponses = [];

            $.merge(allSelectedResponses, checkedRadios);
            $.merge(allSelectedResponses, selectedOptions);
            return allSelectedResponses;
        },

        hideAllGridQuestions: function (gridInstance) {
            var allSelectedResponses = this.getAllSelectedResponses(gridInstance),
                questionIdsToHide = getElementsToSkip(allSelectedResponses, 'data-skip-hybrid-grid-rules');
            this.showGridElements(questionIdsToHide, gridInstance);
            $.map(questionIdsToHide, function (val) {
                $(gridInstance).find('.form-group-question-' + val).hide();
            });
            this.hiddenGridQuestions = questionIdsToHide;
        },
        bindOnChangeEventListener: function (gridInstance) {
            var self = this;
            var allOptions = $(gridInstance).find('[type="radio"], select');
            $.map(allOptions, function (element) {
                $(element).on('change', function () {
                    self.hideAllGridQuestions(gridInstance)
                })
            })
        },
        bindSkipRulesOn: function (gridInstance) {
            $(gridInstance).find('div[class^="form-group form-group-question-"]').show();
            $(gridInstance).find('li[class^="form-group-question-"]').show();
            this.bindOnChangeEventListener(gridInstance);
        }
    };
})();
