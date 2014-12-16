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

var scopedSkipRules = (function(scope) {
    var scope = $(scope);

    return {
        hiddenQuestionIds : [],
        showGridQuestion: function(val) {
            scope.find('.form-group-question-' + val).show();
        },
        showGridElements: function(elementsToBeHidden, showFn) {
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
                questionIdsToHide = getElementsToSkip(allSelectedResponses, 'data-skip-hybrid-grid-rules');
            this.showGridElements(questionIdsToHide, this.showGridQuestion);
            $.map(questionIdsToHide, function(val) {
                scope.find('.form-group-question-' + val).hide();
            });
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

var applySkipRules = (function () {
    var self = this;
    var allRadios = $(":radio"),
        allOptions = $("select"),
        allHiddenQuestions = [],
        allHiddenSubsections = [];

    $(document).ready(function () {
        var allgrids = $('.hybrid-group-row');
        for(grid in allgrids.toArray()){
            var gridInstanceRule = new scopedSkipRules(allgrids[grid]);
            gridInstanceRule.bindAddMoreListener();
        }

        hideAllQuestions();
        hideAllSubsections();
        applySkipRules && applySkipRules.bindSkipRulesOnDisplayAll();
        var tableRows = $('.grid tr');
        $.map(tableRows, function(tableRow){
            applySkipRules && applySkipRules.hideAllDisplayAllQuestions(tableRow);
        });
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
        showDisplayAllGridQuestion: function (val, tableRow) {
            var element = $(tableRow).find('.input-question-id-' + val);
                element.prop('disabled', false);
        },
        showGridElements: function (elementsToBeHidden, gridInstance, showFn) {
            var self = this;
            $.map(self.hiddenGridQuestions, function (val, _) {
                if ($.inArray(val, elementsToBeHidden) === -1) {
                    showFn(val, gridInstance);
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
            this.showGridElements(questionIdsToHide, gridInstance, this.showGridQuestion);
            $.map(questionIdsToHide, function (val) {
                $(gridInstance).find('.form-group-question-' + val).hide();
            });
            this.hiddenGridQuestions = questionIdsToHide;
        },
        hideAllDisplayAllQuestions: function (tableRow) {
            var allSelectedResponses = this.getAllSelectedResponses(tableRow),
                questionIdsToHide = getElementsToSkip(allSelectedResponses, 'data-skip-rules');
            this.showGridElements(questionIdsToHide, tableRow, this.showDisplayAllGridQuestion);
            $.map(questionIdsToHide, function (val) {
                var element = $(tableRow).find('.input-question-id-' + val);
                element.prop('disabled', true);
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
            var gridInstanceRule = new scopedSkipRules(gridInstance);
            gridInstanceRule.bindAddMoreListener();
        },
        bindSkipRulesOnDisplayAll: function(){
            var self = this;
            var tableRows = $('.grid tr');
            $.map(tableRows, function(tableRow){
                var allOptions = $(tableRow).find('[type="radio"], select');
                $.map(allOptions, function (element) {
                    $(element).on('change', function () {
                        self.hideAllDisplayAllQuestions(tableRow);
                    })
                })
            });
        }
    };
})();
