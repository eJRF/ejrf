//require('grid-service.js');

if (typeof createGrid == 'undefined') {
    var createGrid = {};
}

var gridModule = angular.module('gridModule', ['gridService']);

var createGridController = function ($scope, QuestionService, ThemeService, GridService) {
    $scope.selectedQuestions =
    {
        primary: {},
        otherColumns: [
            {}
        ]
    };

    $scope.grid = {
        questions: [],
        questionOptions: [],
        gridType: '',
        selectedTheme: '',
        primaryQuestions: []
    };
    $scope.gridForm = {};

    $scope.gridFormErrors = {backendErrors: [], formHasErrors: false};
    $scope.subsectionId = $scope.subsectionId || "";

    $scope.grid.addColumn = function () {
        $scope.selectedQuestions.otherColumns.push({});
    };

    $scope.grid.removeColumn = function (index) {
        $scope.selectedQuestions.otherColumns.splice(index, 1);
    };

    $scope.createGridModal = function (questionnaireId, subsectionId) {
        $scope.subsectionId = subsectionId;
        QuestionService.filter({questionnaire: questionnaireId, unused: true})
            .then(function (response) {
                var questions = response.data;
                $scope.grid.questions = questions;

                $scope.grid.primaryQuestions = questions.filter(function (question) {
                    return question.fields.is_primary && question.fields.answer_type == 'MultiChoice';
                });
            });

        ThemeService.all().then(function (response) {
            $scope.themes = response.data;
        });

        $scope.types = [
            {value: 'display_all', text: 'Display All'}
        ];
    };

    $scope.postNewGrid = function () {
        var columnsIds = $scope.selectedQuestions.otherColumns.map(function (question) {
            return question && question.pk;
        });
        var payload = {
            'type': $scope.grid.gridType && $scope.grid.gridType.value,
            'primary_question': $scope.selectedQuestions.primary.pk,
            'columns': columnsIds,
            'csrfmiddlewaretoken': window.csrfToken
        };

        function createNewGrid() {
            if ($scope.newGrid.$valid && validateDynamicForms($scope.gridForm)) {
                $scope.error = '';
                GridService.create($scope.subsectionId, payload)
                    .success(function (response) {
                        $scope.message = response[0].message;
                        $scope.gridFormErrors.formHasErrors = false;
                    }).error(function (response) {
                        $scope.error = response[0].message;
                        $scope.gridFormErrors.formHasErrors = true;
                        $scope.gridFormErrors.backendErrors = response[0].form_errors;
                    });
            } else {
                $scope.gridFormErrors.formHasErrors = true;
                $scope.error = 'The are errors in the form. Please fix them and submit again.';
                $scope.message = '';
            }
        }

        createNewGrid();
    };

    $scope.$watch('grid.selectedTheme', function () {
        $scope.grid.questionOptions = [];
    });

    $scope.$watch('selectedQuestions.primary', function (selectedPrimary) {
        $scope.selectedQuestions.primary = selectedPrimary;

        if (selectedPrimary) {
            selectedPrimary.pk &&
            QuestionService.options(selectedPrimary)
                .then(function (response) {
                    $scope.grid.questionOptions = response.data;
                });
        } else {
            $scope.grid.questionOptions = [];
        }
    });
};

gridModule.controller('CreateGridController', ['$scope', 'QuestionService',
    'ThemeService', 'GridService', createGridController]);

var notSelectedFilter = function () {
    return function (questions, existingColumnQuestions, index) {
        return questions.filter(function (question) {
            var questionIndex = existingColumnQuestions.indexOf(question);
            return questionIndex == -1 || questionIndex == index;
        });
    };
};

gridModule.filter('notSelected', notSelectedFilter);

gridModule.run(function ($http) {
    $http.defaults.headers.common['X-CSRFToken'] = window.csrfToken;
});

createGrid.updateCreateGrid = function (questionnaireId, subsectionId) {
    angular.element(document.getElementById('create-grid-controller')).scope()
        .createGridModal(questionnaireId, subsectionId);
};