var gridTypeFactories = angular.module('gridTypeFactories', []);

gridTypeFactories.factory('NonHybridPayload', function () {
    var generatePayload = function (selectedQuestions, type) {
        var columnsIds = selectedQuestions.otherColumns.map(function (question) {
            return question.pk;
        });
        return {
            'type': type,
            'primary_question': selectedQuestions.primary.pk,
            'columns': columnsIds,
            'csrfmiddlewaretoken': window.csrfToken
        };
    };
    return {payload: generatePayload};
});

gridTypeFactories.factory('NonHybridQuestionSelection', function () {
    var addColumn = function (index) {
        this.otherColumns.splice(index, 0, {});
    };

    var removeColumn = function (index) {
        this.otherColumns.splice(index, 1);
    };

    return {
        primary: {},
        otherColumns: [
            {}
        ],
        addColumn: addColumn,
        removeColumn: removeColumn
    };

});

gridTypeFactories.factory('AddMoreGridFactory', function (NonHybridPayload, NonHybridQuestionSelection) {
    var addMoreGrid = function () {
        var thePayload = function(){
          return   NonHybridPayload.payload(this.initialSelectedQuestions, this.value);
        };
        return {
            value: 'allow_multiples',
            text: 'Add More',
            addMore: true,
            hybrid: false,
            primary_questions_criteria: {is_primary: true},
            payload: thePayload,
            initialSelectedQuestions: NonHybridQuestionSelection
        }
    };
    return {
        create: function () {
            return new addMoreGrid();
        }}
});

gridTypeFactories.factory('DisplayAllGridFactory', function (NonHybridPayload, NonHybridQuestionSelection) {
    var DisplayAllGrid = function () {
        var thePayload = function(){
          return   NonHybridPayload.payload(this.initialSelectedQuestions, this.value);
        };

        return {
            value: 'display_all',
            text: 'Display All',
            displayAll: true,
            hybrid: false,
            primary_questions_criteria: {
                is_primary: true,
                answer_type: 'MultiChoice'
            },
            payload: thePayload,
            initialSelectedQuestions: NonHybridQuestionSelection
        }
    };
    return {
        create: function () {
            return new DisplayAllGrid();
        }};
});

gridTypeFactories.factory('HybridGridFactory', function (hybridGridQuestionSelection) {
    function generatePayload() {
        var self = this;
        var hybridNonPrimaryQuestionMatrix = this.initialSelectedQuestions.dynamicGridQuestion;
        function getIds(wrappedQuestion) {
            return wrappedQuestion.question.pk;
        }

        var columns = hybridNonPrimaryQuestionMatrix.reduce(function (prev, curr) {
            return prev.concat(curr);
        }, []).map(getIds);

        var subgroup = hybridNonPrimaryQuestionMatrix.filter(function (column) {
            return column.length > 1;
        })[0];

        var subGroupQuestions = subgroup && subgroup.map(getIds);

        return {
            'csrfmiddlewaretoken': window.csrfToken,
            'type': self.value,
            'primary_question': this.initialSelectedQuestions.primary.pk,
            'columns': columns,
            'subgroup': subGroupQuestions || []
        }
    }

    var HybridGrid = function () {
        return {
            value: 'hybrid',
            text: 'Hybrid',
            hybrid: true,
            addMore: true,
            primary_questions_criteria: {is_primary: true},
            payload: generatePayload,
            initialSelectedQuestions: hybridGridQuestionSelection
        }
    };
    return {
        create: function () {
            return new HybridGrid();
        }};
});


gridTypeFactories.factory('hybridGridQuestionSelection', function () {

    var addElement = function (rowIndex, columnIndex) {
        this.dynamicGridQuestion[rowIndex].splice(columnIndex, 0, {});
    };

    var addRow = function (rowIndex) {
        this.dynamicGridQuestion.splice(rowIndex, 0, [
            {}
        ]);
        return rowIndex;
    };

    var removeElement = function (rowIndex, columnIndex) {
        this.dynamicGridQuestion[rowIndex].splice(columnIndex, 1);
    };

    return {
        primary: {},
        dynamicGridQuestion: [
            [
                {}
            ]
        ],
        addElement: addElement,
        addRow: addRow,
        removeElement: removeElement
    };
});
