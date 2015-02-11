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

        var gridQuestionsFrom = function (allQuestions, gridQuestionIds) {
            return allQuestions.filter(function (qn) {
                var qnIndex = gridQuestionIds.indexOf(qn.pk);
                return qnIndex != -1;
            })
        };

        var primaryQuestionIn = function (gridQuestions, questionIds) {
            return gridQuestions.filter(function (qn) {
                var qnIndex = questionIds.indexOf(qn.pk);
                return qnIndex != -1 && qn.fields.is_primary;
            })[0]
        };

        var getSelectedQuestions = function (allQuestions, questionIds) {
            var gridQuestions = gridQuestionsFrom(allQuestions, questionIds);

            return {
                primary: primaryQuestionIn(gridQuestions, questionIds),
                otherColumns: gridQuestions.filter(function (qn) {
                    var qnIndex = questionIds.indexOf(qn.pk);
                    return qnIndex != -1 && !qn.fields.is_primary;
                })
            }
        };

        function getTheme(gridQuestions, gridQuestionIds) {
            var primaryQuestion = primaryQuestionIn(gridQuestions, gridQuestionIds);
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


        GridService.fetch(gridId).then(function (gridResponse) {
            var gridData = gridResponse.data,
                grid = gridData[0];
            var gridQuestionIds = grid.fields.question;

            QuestionService.all().then(function (allQuestionsResponse) {
                var allQuestions = allQuestionsResponse.data;
                var gridQuestions = gridQuestionsFrom(allQuestions, gridQuestionIds);
                QuestionService.filter({questionnaire: questionnaireId, unused: true}).then(function (response) {
                    $scope.grid.questions = gridQuestions.concat(response.data);

                    var type = getType(grid),
                        selectedQuestionsFromGrid = getSelectedQuestions(gridQuestions, gridQuestionIds);

                    $scope.grid.selectedTheme = getTheme(gridQuestions, gridQuestionIds);
                    $scope.grid.gridType = type;
                    $scope.selectedQuestions = type.initialSelectedQuestions;

                    $scope.selectedQuestions.primary = selectedQuestionsFromGrid.primary;
                    $scope.selectedQuestions.otherColumns = selectedQuestionsFromGrid.otherColumns;
                    QuestionService.options(selectedQuestionsFromGrid.primary).then(function (response) {
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
