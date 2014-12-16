var getElementsToSkip = function(selectedElements, dataAttribute) {
    var elements = $.map(selectedElements, function(val) {
        if (val.attributes[dataAttribute]) {
            var data = val.attributes[dataAttribute];
            return data && data.value.split(",");
        } else {
            return '';
        }
    });
    return $.grep(elements, function(val, _) {
        return val !== '';
    });
};

var scopedSkipRules = (function(scope, dataAttribute, hideFn, showFn) {
    var scope = scope;

    return {
        hiddenQuestionIds: [],
        showGridElements: function(elementsToBeHidden) {
            var self = this;
            $.map(self.hiddenQuestionIds, function(val, _) {
                if ($.inArray(val, elementsToBeHidden) === -1) {
                    showFn(val);
                }
            });
        },
        getAllSelectedResponses: function() {
            var checkedRadios = scope.find('[type=radio]:checked'),
                selectedOptions = scope.find('option:checked'),
                allSelectedResponses = [];

            $.merge(allSelectedResponses, checkedRadios);
            $.merge(allSelectedResponses, selectedOptions);
            return allSelectedResponses;
        },
        hideQuestions: function() {
            var allSelectedResponses = this.getAllSelectedResponses(scope),
                questionIdsToHide = getElementsToSkip(allSelectedResponses, dataAttribute);
            this.showGridElements(questionIdsToHide);
            $.map(questionIdsToHide, hideFn);
            this.hiddenQuestionIds = questionIdsToHide;
        },
        bindOnChangeEventListener: function() {
            var self = this;
            var allOptions = scope.find('[type="radio"], select');
            $.map(allOptions, function(element) {
                $(element).on('change', function() {
                    self.hideQuestions()
                })
            })
        },
        bindAddMoreListener: function() {
            scope.find('div[class^="form-group form-group-question-"]').show();
            scope.find('li[class^="form-group-question-"]').show();
            this.bindOnChangeEventListener();
        }
    }
});

var createScopedHybridRules = function(scope) {
    var questionSelector = '.form-group-question-';
    var dataAttribute = 'data-skip-hybrid-grid-rules';
    var hideFn = function(val) {
        $(scope).find(questionSelector + val).hide();
    };
    var showFn = function(val) {
        $(scope).find(questionSelector + val).show();
    };

    var gridInstanceRule = new scopedSkipRules($(scope), dataAttribute, hideFn, showFn);
    gridInstanceRule.bindAddMoreListener();
    gridInstanceRule.hideQuestions();
    return gridInstanceRule;
};

var createScopedDisplayAllRules = function(scope) {
    var questionSelector = '.input-question-id-';
    var dataAttribute = 'data-skip-rules';

    var hideFn = function(val) {
        var element = $(scope).find(questionSelector + val);
        element.prop('disabled', true);
    };
    var showFn = function(val) {
        var element = $(scope).find(questionSelector + val);
        element.prop('disabled', false);
    };

    var gridInstanceRule = new scopedSkipRules($(scope), dataAttribute, hideFn, showFn);
    gridInstanceRule.bindAddMoreListener();
    gridInstanceRule.hideQuestions();
    return gridInstanceRule;
};

var applySkipRules = (function() {
    var self = this;
    var allRadios = $(":radio"),
        allOptions = $("select"),
        allHiddenQuestions = [],
        allHiddenSubsections = [];

    $(document).ready(function() {
        hideAllQuestions();
        hideAllSubsections();

        var allgrids = $('.hybrid-group-row');

        for (grid in allgrids.toArray()) {
            createScopedHybridRules(allgrids[grid]);
        }
        var tableRows = $('.grid tr');
        $.map(tableRows, function(tableRow) {
            createScopedDisplayAllRules(tableRow);
        });
    });

    var hideQuestionById = function(id) {
        $('.form-group-question-' + id).hide();
    };
    var showQuestionById = function(id) {
        $('.form-group-question-' + id).show();
    };

    var hideSubsectionById = function(id) {
        $('#subsection-' + id + '-content').hide();
    };
    var showSubsectionById = function(id) {
        $('#subsection-' + id + '-content').show();
    };

    var getElementsToSkip = function(selectedElements, dataAttribute) {
        var elements = $.map(selectedElements, function(val) {
            if (val.attributes[dataAttribute]) {
                var data = val.attributes[dataAttribute];
                return data && data.value.split(",");
            } else {
                return '';
            }
        });
        return $.grep(elements, function(val, _) {
            return val !== '';
        });
    };

    var showElements = function(currentlyHiddenElements, elementsToBeHidden, fnShow) {

        $.map(currentlyHiddenElements, function(val, _) {
            if ($.inArray(val, elementsToBeHidden) === -1) {
                fnShow(val);
            }
        });
    };

    var hideQuestions = function(dataAttr) {
        var checkedRadios = $('[type="radio"]:checked');
        var selectedOptions = $('option:selected');
        var allSelectedResponses = [];
        $.merge(allSelectedResponses, checkedRadios);
        $.merge(allSelectedResponses, selectedOptions);
        var questionIdsToHide = getElementsToSkip(allSelectedResponses, dataAttr);

        showElements(allHiddenQuestions, questionIdsToHide, showQuestionById);
        $.map(questionIdsToHide, function(val) {
            hideQuestionById(val);
        });
        allHiddenQuestions = questionIdsToHide;
    };

    var hideAllQuestions = function() {
        hideQuestions('data-skip-rules');
    };

    var hideAllSubsections = function() {
        var checkedRadios = $('[type="radio"]:checked'),
            selectedOptions = $('option:selected'),
            allSelectedResponses = [];
        $.merge(allSelectedResponses, checkedRadios);
        $.merge(allSelectedResponses, selectedOptions);
        var subsectionIdsToHide = getElementsToSkip(allSelectedResponses, 'data-skip-subsection');

        showElements(allHiddenSubsections, subsectionIdsToHide, showSubsectionById);
        $.map(subsectionIdsToHide, function(val) {
            hideSubsectionById(val);
        });
        allHiddenSubsections = subsectionIdsToHide;
    };


    $.map(allRadios, function(element) {
        $(element).on('change', function() {
            hideAllQuestions();
            hideAllSubsections();
        });
    });

    $.map(allOptions, function(element) {
        $(element).on('change', function() {
            hideAllQuestions();
            hideAllSubsections();
        });
    });
    return {
        getElementsToSkip: getElementsToSkip,
        showElements: showElements,
        hiddenGridQuestions: [],
        getAllSelectedResponses: function(gridInstance) {
            var checkedRadios = $(gridInstance).find('[type=radio]:checked'),
                selectedOptions = $(gridInstance).find('option:checked'),
                allSelectedResponses = [];

            $.merge(allSelectedResponses, checkedRadios);
            $.merge(allSelectedResponses, selectedOptions);
            return allSelectedResponses;
        },
        bindSkipRulesOn: function(gridInstance) {
            $(gridInstance).find('div[class^="form-group form-group-question-"]').show();
            $(gridInstance).find('li[class^="form-group-question-"]').show();
            createScopedHybridRules(gridInstance);
        }
    };
})();