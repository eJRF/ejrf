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
    $scope.gridFormErrors = {};
    $scope.updateScope = function (questionnaireId, subsectionId, gridId) {
        $scope.gridId = gridId;
        $scope.selectedQuestions = {
            primary: {},
            otherColumns: []
        };

        var primaryQuestionIn = function (questionIds) {
            return $scope.grid.questions.filter(function (qn) {
                var qnIndex = questionIds.indexOf(qn.pk);
                return qnIndex != -1 && qn.fields.is_primary;
            })[0]
        };

        var getSelectedQuestions = function (question) {
            return {
                primary: primaryQuestionIn(question),
                otherColumns: $scope.grid.questions.filter(function (qn) {
                    var qnIndex = question.indexOf(qn.pk);
                    return qnIndex != -1 && !qn.fields.is_primary;
                })
            }
        };

        function getTheme(grid) {
            var primaryQuestion = primaryQuestionIn(grid.fields.question);
            return primaryQuestion.fields.theme;
        }

        function getType(grid) {
            if (grid.fields.hybrid) {
                return HybridGridFactory.create();
            }
            if (grid.fields.allow_multiples) {
                return AddMoreGridFactory.create();
            }
            return DisplayAllGridFactory
                .create();
        }


        GridService.fetch(subsectionId, gridId).then(function (gridResponse) {
            var gridData = gridResponse.data;
            QuestionService.all().then(function (response) {
                $scope.grid.questions = response.data;
                var grid = gridData[0],
                    type = getType(grid),
                    selectedQuestionsFromGrid = getSelectedQuestions(grid.fields.question);

                $scope.grid.selectedTheme = getTheme(grid);
                $scope.grid.gridType = type;
                $scope.selectedQuestions = type.initialSelectedQuestions;

                $scope.selectedQuestions.primary = selectedQuestionsFromGrid.primary;
                $scope.selectedQuestions.otherColumns = selectedQuestionsFromGrid.otherColumns;
                QuestionService.options(selectedQuestionsFromGrid.primary).then(function (response) {
                    $scope.grid.questionOptions = response.data;
                });
            });

        });

    };

    $scope.postUpdateGrid = function () {
        var gridType = $scope.grid.gridType;

        GridService.update($scope.subsectionId, $scope.gridId, gridType.payload())
            .success(function (response) {
                $scope.message = response[0].message;
                $scope.gridFormErrors.formHasErrors = false;
            }).error(function (response) {
                $scope.error = response[0].message;
                $scope.gridFormErrors.formHasErrors = true;
                $scope.gridFormErrors.backendErrors = response[0].form_errors;
            });
    };
};

editGridModule.controller('EditGridController', editGridController);

editGrid.updateEditGridScope = function (questionnaireId, subsectionId, gridId) {
    angular.element(document.getElementById('edit-grid-controller')).scope().updateScope(questionnaireId, subsectionId, gridId);
};
