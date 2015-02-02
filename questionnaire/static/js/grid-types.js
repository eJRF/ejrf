var gridTypeFactories = angular.module('gridTypeFactories', []);

gridTypeFactories.factory('NonHybridPayload', function () {
    var generatePayload = function (selectedQuestions) {
        var self = this;
        var columnsIds = selectedQuestions.otherColumns.map(function (question) {
            return question.pk;
        });
        return {
            'type': self.value,
            'primary_question': selectedQuestions.primary.pk,
            'columns': columnsIds,
            'csrfmiddlewaretoken': window.csrfToken
        };
    };
    return {
        payload: generatePayload,
        selectedQuestions: {
            primary: {},
            otherColumns: [
                {}
            ]
        }};

});

gridTypeFactories.factory('AddMoreGridFactory', function (NonHybridPayload) {
    var addMoreGrid = function () {
        return {
            value: 'allow_multiples',
            text: 'Add More',
            addMore: true,
            hybrid: false,
            primary_questions_criteria: {is_primary: true},
            payload: NonHybridPayload.payload,
            initialSelectedQuestions: NonHybridPayload.selectedQuestions
        }
    };
    return {
        create: function () {
            return new addMoreGrid();
        }}
});

gridTypeFactories.factory('DisplayAllGridFactory', function (NonHybridPayload) {
    var DisplayAllGrid = function () {
        return {
            value: 'display_all',
            text: 'Display All',
            displayAll: true,
            hybrid: false,
            primary_questions_criteria: {
                is_primary: true,
                answer_type: 'MultiChoice'
            },
            payload: NonHybridPayload.payload,
            initialSelectedQuestions: NonHybridPayload.selectedQuestions
        }
    };
    return {
        create: function () {
            return new DisplayAllGrid();
        }};
});

gridTypeFactories.factory('HybridGridFactory', function () {
    function generatePayload(selectedQuestions) {
        var self = this;
        var hybridNonPrimaryQuestionMatrix = selectedQuestions.dynamicGridQuestion;

        function getIds(question) {
            return question.pk;
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
            'primary_question': selectedQuestions.primary.pk,
            'columns': columns,
            'subgroup': subGroupQuestions || []
        }
    }

    var initialSelectedQuestions = {
        primaryQuestion: {},
        dynamicGridQuestion: [
            []
        ]
    };

    var HybridGrid = function () {
        return {
            value: 'hybrid',
            text: 'Hybrid',
            hybrid: true,
            addMore: true,
            primary_questions_criteria: {is_primary: true},
            payload: generatePayload,
            initialSelectedQuestions: initialSelectedQuestions
        }
    };
    return {
        create: function () {
            return new HybridGrid();
        }};
});
