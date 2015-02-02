if (typeof createGrid == 'undefined') {
    var createGrid = {};
}

var gridModule = angular.module('gridModule', ['gridService', 'gridTypeFactories']);

var createGridController = function ($scope, QuestionService, ThemeService, GridService, hybridGridService, DisplayAllGridFactory, AddMoreGridFactory, HybridGridFactory) {

    function resetScope() {
        $scope.gridForm = {};

        $scope.gridFormErrors = {backendErrors: [], formHasErrors: false};
        $scope.subsectionId = $scope.subsectionId || "";

        $scope.error = '';
        $scope.message = '';

        $scope.grid.questionOptions = [];
        $scope.grid.selectedTheme = '';
    }

    $scope.hybridGrid = {
        rows: hybridGridService.rows,
        columns: hybridGridService.columns,
        addElement: hybridGridService.addElement,
        addRow: function (rowIndex) {
            $scope.selectedQuestions.dynamicGridQuestion[rowIndex] = [];
            hybridGridService.addRow(rowIndex);
        },
        removeElement: function (rowIndex, columnIndex) {
            $scope.selectedQuestions.dynamicGridQuestion[rowIndex].splice(columnIndex, 1);
            hybridGridService.removeElement(rowIndex, columnIndex);
        }
    };

    $scope.grid = {
        questions: [],
        questionOptions: [],
        gridType: '',
        selectedTheme: '',
        primaryQuestions: [],
        addGridRow: false
    };

    resetScope();

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
                $scope.grid.questions = response.data;
            });

        ThemeService.all().then(function (response) {
            $scope.themes = response.data;
        });

        $scope.types = [DisplayAllGridFactory.create(),
            AddMoreGridFactory.create(), HybridGridFactory.create()];
    };

    $scope.postNewGrid = function () {
        function createNewGrid() {
            if ($scope.newGrid.$valid && validateDynamicForms($scope.gridForm)) {
                $scope.error = '';
                var gridType = $scope.grid.gridType;

                GridService.create($scope.subsectionId, gridType.payload($scope.selectedQuestions))
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
    'ThemeService', 'GridService', 'hybridGridService', 'AddMoreGridFactory',
    'DisplayAllGridFactory', 'HybridGridFactory', createGridController]);

gridModule.directive('questionInput', function (QuestionService, $q) {

    var answerInput = function (question) {
        var generateSelect = function (question) {

            return QuestionService.options(question).then(function (response) {
                var questionOptions = response.data,
                    initialValue = '<select><option>Choose One</option>',
                    closingTag = '</select>';

                return questionOptions.reduce(function (prev, curr) {
                        return prev + '<option>' + curr.fields.text + '</option>'
                    }, initialValue)
                    + closingTag;
            });
        };

        var textInput = function (klass) {
            var aklass = klass || '';
            var deferred = $q.defer();
            deferred.resolve('<input type="text" class="' + aklass + '"/>');
            return deferred.promise
        };

        var answerInputMap = {
            number: textInput(),
            text: textInput(),
            date: textInput("datetimepicker"),
            multichoice: generateSelect(question),
            multipleresponse: generateSelect(question)
        };
        return answerInputMap[question.fields.answer_type.toLowerCase()]
    };

    return {
        restrict: 'E',
        scope: false,
        link: function ($scope, elem) {
            var correspondingColumnQuestion = function () {
                return $scope.selectedQuestions.otherColumns[$scope.$index];
            };

            $scope.$watch(correspondingColumnQuestion, function (newVal) {
                newVal && newVal.fields && answerInput(newVal).then(function (inputField) {
                    elem.replaceWith(inputField);
                    (newVal.fields.answer_type.toLowerCase() == 'date') && $('.datetimepicker').datepicker({
                        pickTime: false,
                        autoclose: false
                    });
                })
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

gridModule.filter('notInHybridGrid', function () {
    return function (questions, otherColumnMatrix, rowIndex, columnIndex) {
        var otherColumnQuestions = otherColumnMatrix.reduce(function (prev, curr) {
            return prev.concat(curr);
        });

        return questions.filter(function (question) {
            var indexInMatrix = otherColumnQuestions.indexOf(question);

            var questionIndex = otherColumnMatrix[rowIndex].indexOf(question);
            return indexInMatrix == -1 || questionIndex == columnIndex;
        });
    }
});

gridModule.run(function ($http) {
    $http.defaults.headers.common['X-CSRFToken'] = window.csrfToken;
});

createGrid.updateCreateGrid = function (questionnaireId, subsectionId) {
    angular.element(document.getElementById('create-grid-controller')).scope().createGridModal(questionnaireId, subsectionId);
};