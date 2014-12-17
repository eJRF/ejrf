var scopedSkipRules = (function(scope, dataAttribute, hideFn, showFn) {
    var scope = scope;

    return {
        hiddenQuestionIds: [],
        getElementsToSkip: function() {
            var selectedElements = this.getAllSelectedResponses();
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
        },
        showGridElements: function(elementsToBeHidden) {
            var self = this;
            $.map(self.hiddenQuestionIds, function(val, _) {
                if ($.inArray(val, elementsToBeHidden) === -1) {
                    showFn(val);
                }
            });
        },
        getAllSelectedResponses: function() {
            var checkedRadios = scope.find('[type=radio]:checked').toArray(),
                selectedOptions = scope.find('option:checked').toArray();
            return checkedRadios.concat(selectedOptions);
        },
        hideQuestions: function() {
            var questionIdsToHide = this.getElementsToSkip();
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
    var hideFn = function(val) {
        $(scope).find(questionSelector + val).hide();
    };
    var showFn = function(val) {
        $(scope).find(questionSelector + val).show();
    };

    var gridInstanceRule = new scopedSkipRules($(scope), 'data-skip-hybrid-grid-rules', hideFn, showFn);
    gridInstanceRule.bindAddMoreListener();
    gridInstanceRule.hideQuestions();
    return gridInstanceRule;
};

var createScopedDisplayAllRules = function(scope) {
    var questionSelector = '.input-question-id-';

    var hideFn = function(val) {
        var element = $(scope).find(questionSelector + val);
        element.prop('disabled', true);
    };
    var showFn = function(val) {
        var element = $(scope).find(questionSelector + val);
        element.prop('disabled', false);
    };

    var gridInstanceRule = new scopedSkipRules($(scope), 'data-skip-rules', hideFn, showFn);
    gridInstanceRule.bindOnChangeEventListener();
    gridInstanceRule.hideQuestions();
    return gridInstanceRule;
};


var createSkipQuestionRules = function(){
    var questionSelector = '.form-group-question-';
    var scope = $('body');

    var hideFn = function(val) {
        scope.find(questionSelector + val).hide();
    };
    var showFn = function(val) {
        scope.find(questionSelector + val).show();
    };

    var gridInstanceRule = new scopedSkipRules(scope, 'data-skip-rules', hideFn, showFn);
    gridInstanceRule.bindOnChangeEventListener();
    gridInstanceRule.hideQuestions();
    return gridInstanceRule;
}

var createSkipSubsectionRules = function(){
    var scope = $('body');

    var hideFn = function(id) {
        scope.find('#subsection-' + id + '-content').hide();
    };
    var showFn = function(id) {
        scope.find('#subsection-' + id + '-content').show();
    };

    var gridInstanceRule = new scopedSkipRules(scope, 'data-skip-subsection', hideFn, showFn);
    gridInstanceRule.bindOnChangeEventListener();
    gridInstanceRule.hideQuestions();
    return gridInstanceRule;
}

var applySkipRules = (function() {

    $(document).ready(function() {

        var allgrids = $('.hybrid-group-row');
        $.map(allgrids, function(gridInstance) {
            createScopedHybridRules(gridInstance);
        });

        var tableRows = $('.grid tr');
        $.map(tableRows, function(tableRow) {
            createScopedDisplayAllRules(tableRow);
        });

        createSkipQuestionRules();
        createSkipSubsectionRules();
    });
    return {
        bindSkipRulesOn: function(gridInstance) {
            $(gridInstance).find('div[class^="form-group form-group-question-"]').show();
            $(gridInstance).find('li[class^="form-group-question-"]').show();
            createScopedHybridRules(gridInstance);
        }
    };
})();