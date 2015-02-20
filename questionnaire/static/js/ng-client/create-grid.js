if (typeof createGrid == 'undefined') {
    var createGrid = {};
}

var gridModule = angular.module('gridModule', ['gridService', 'gridTypeFactories']);

var createGridController = function ($scope, QuestionService, ThemeService, GridService, DisplayAllGridFactory, AddMoreGridFactory, HybridGridFactory) {

    function resetScope() {
        $scope.gridForm = {};
        $scope.gridFormErrors = {backendErrors: [], formHasErrors: false};
        $scope.subsectionId = $scope.subsectionId || "";

        $scope.error = '';
        $scope.message = '';

        $scope.grid.questionOptions = [];
        $scope.grid.selectedTheme = '';
    }


    $scope.grid = {
        questions: [],
        questionOptions: [],
        gridType: '',
        selectedTheme: '',
        primaryQuestions: [],
        addGridRow: false
    };

    resetScope();

    $scope.createGridModal = function (questionnaireId, subsectionId) {
        $scope.subsectionId = subsectionId;
        QuestionService.filter({questionnaire: questionnaireId, unused: true})
            .then(function (response) {
                $scope.grid.questions = response.data;
            });

        ThemeService.all().then(function (response) {
            $scope.themes = response.data;
        });

        $scope.types = [DisplayAllGridFactory.create(),
            AddMoreGridFactory.create(), HybridGridFactory.create()];
    };

    $scope.postNewGrid = function () {
        if ($scope.newGrid.$valid && validateDynamicForms($scope.gridForm)) {
            $scope.error = '';
            var gridType = $scope.grid.gridType;

            GridService.create($scope.subsectionId, gridType.payload())
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
    };

    $scope.isNotMultiChoice = function (question) {
        return !(question.fields.answer_type == 'MultiChoice' || question.fields.answer_type == 'MultipleResponse');
    };

    $scope.$watch('grid.selectedTheme', function () {
        $scope.grid.questionOptions = [];
    });

    $scope.$watch('grid.gridType', function (type) {
        if (type) {
            resetScope();
            $scope.selectedQuestions = type.initialSelectedQuestions;
            $scope.grid.primaryQuestions = questionFilter($scope.grid.questions, type.primary_questions_criteria);
        }
    });

    $scope.$watch('selectedQuestions.primary', function (selectedPrimary) {
        if (selectedPrimary) {
            $scope.selectedQuestions.primary = selectedPrimary;

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
    'ThemeService', 'GridService', 'AddMoreGridFactory',
    'DisplayAllGridFactory', 'HybridGridFactory', createGridController]);

gridModule.directive('questionInput', function (AnswerInput) {
    return {
        restrict: 'E',
        scope: false,
        link: function ($scope, elem) {
            var correspondingColumnQuestion = function () {
                return $scope.selectedQuestions.otherColumns[$scope.$index];
            };

            $scope.$watch(correspondingColumnQuestion, function (newVal) {
                AnswerInput.render(newVal, elem);
            });
        }
    }
});

gridModule.directive('primaryQuestionInput', function (AnswerInput) {
    return {
        restrict: 'E',
        scope: false,
        link: function ($scope, elem) {
            $scope.$watch('selectedQuestions.primary', function (newVal) {
                AnswerInput.render(newVal, elem);
            });
        }
    }
});

var notSelectedFilter = function () {
    return function (questions, existingColumnQuestions, index) {
        return questions.filter(function (question) {
            var questionIndex = existingColumnQuestions.indexOf(question);
            return questionIndex == -1 || questionIndex == index;
        });
    };
};


gridModule.filter('notSelected', notSelectedFilter);

var filterByCriteria = function () {
    return function (questions, field, value) {
        return questions.filter(function (question) {
            return question.fields[field] == value;
        });
    };
};
gridModule.filter('satisfy', filterByCriteria);

gridModule.filter('notInHybridGrid', function () {
    return function (questions, otherColumnMatrix, selectedQuestion) {
        function extractQuestion(wrappedQuestion) {
            return wrappedQuestion.question;
        }

        var otherColumnQuestions = otherColumnMatrix.reduce(function (prev, curr) {
            return prev.concat(curr);
        }).map(extractQuestion);

        return questions.filter(function (question) {
            var indexInMatrix = otherColumnQuestions.indexOf(question);

            return indexInMatrix == -1 || question == selectedQuestion;
        });
    }
});

gridModule.run(function ($http) {
    $http.defaults.headers.common['X-CSRFToken'] = window.csrfToken;
});

createGrid.updateCreateGrid = function (questionnaireId, subsectionId) {
    angular.element(document.getElementById('create-grid-controller')).scope().createGridModal(questionnaireId, subsectionId);
};