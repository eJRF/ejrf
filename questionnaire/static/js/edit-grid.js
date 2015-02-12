if (typeof editGrid == 'undefined') {
    var editGrid = {};
}

var editGridModule = angular.module('editGridModule', ['gridService', 'gridTypeFactories']);

var editGridController = function ($scope, GridService, QuestionService, DisplayAllGridFactory, AddMoreGridFactory, HybridGridFactory) {
    $scope.grid = {
        selectedTheme: {},
        gridType: {},
        questions: []
    };
    $scope.allQuestions = [];
    $scope.gridFormErrors = {};
    $scope.editGridForm = {};
    $scope.gridForm = {};


    $scope.updateScope = function (questionnaireId, subsectionId, gridId) {
        $scope.gridId = gridId;
        $scope.selectedQuestions = {
            primary: {},
            otherColumns: []
        };

        function getTheme(primaryQuestion) {
            return primaryQuestion.fields.theme;
        }

        function initializeType(grid,  allQuestions, gridQuestionIds) {
            if (grid.fields.hybrid) {
                return HybridGridFactory.create(allQuestions, gridQuestionIds);
            }
            if (grid.fields.allow_multiples) {
                return AddMoreGridFactory.create( allQuestions, gridQuestionIds);
            }
            return DisplayAllGridFactory.create( allQuestions, gridQuestionIds);
        }


        GridService.fetch(gridId).then(function (gridResponse) {
            var gridData = gridResponse.data,
                grid = gridData[0];
            var gridQuestionIds = grid.fields.question;

            QuestionService.all().then(function (allQuestionsResponse) {
                var allQuestions = allQuestionsResponse.data;
                QuestionService.filter({questionnaire: questionnaireId, unused: true}).then(function (response) {
                    var type = initializeType(grid, allQuestions, gridQuestionIds),
                        unUsedQuestions = response.data;

                    $scope.selectedQuestions = type.initialSelectedQuestions;

                    var usedQuestions = $scope.selectedQuestions.questions;
                    $scope.grid.questions = usedQuestions.concat(unUsedQuestions);

                    var primaryQuestion = $scope.selectedQuestions.primary;
                    $scope.grid.selectedTheme = getTheme(primaryQuestion);
                    $scope.grid.gridType = type;

                    QuestionService.options(primaryQuestion).then(function (response) {
                        $scope.grid.questionOptions = response.data;
                    });
                });
            });

        });

    };

    $scope.postUpdateGrid = function () {
        var gridType = $scope.grid.gridType;
        if ($scope.editGridForm.$valid && validateDynamicForms($scope.gridForm)) {
            $scope.error = '';

            GridService.update($scope.gridId, gridType.payload())
                .success(function (response) {
                    $scope.message = response[0].message;
                    $scope.gridFormErrors.formHasErrors = false;
                }).error(function (response) {
                    $scope.error = response[0].error;
                    $scope.gridFormErrors.formHasErrors = true;
                    $scope.gridFormErrors.backendErrors = response[0].form_errors;
                });
        } else {
            $scope.gridFormErrors.formHasErrors = true;
            $scope.error = 'The are errors in the form. Please fix them and submit again.';
            $scope.message = '';
        }
    };
};

editGridModule.controller('EditGridController', editGridController);

editGrid.updateEditGridScope = function (questionnaireId, subsectionId, gridId) {
    angular.element(document.getElementById('edit-grid-controller')).scope().updateScope(questionnaireId, subsectionId, gridId);
};
