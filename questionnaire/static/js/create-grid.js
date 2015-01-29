if (typeof createGrid == 'undefined') {
    var createGrid = {};
}

var gridModule = angular.module('gridModule', ['gridService']);

gridModule.factory('hybridGridService', function () {
    var hybridGrid = [[{}]];

    var addElement = function (rowIndex) {
        hybridGrid[rowIndex].push({});
    };

    var createNewRow = function (rowIndex) {
        hybridGrid[rowIndex].splice(rowIndex, 0, []);
    };

    var addRow = function (rowIndex) {
        hybridGrid[rowIndex] = [];
        addElement(rowIndex, 0);
    };

    var rows = function () {
        return hybridGrid
    };

    var columns = function (rowIndex) {
        return hybridGrid[rowIndex];
    };

    var removeElement = function (rowIndex, columnIndex) {
        hybridGrid[rowIndex].splice(columnIndex, 1);
    };

    return {
        rows: rows,
        columns: columns,
        addElement: addElement,
        addRow: addRow,
        removeElement: removeElement
    }
});

var createGridController = function ($scope, QuestionService, ThemeService, GridService, hybridGridService) {

    $scope.selectedQuestions =
    {
        primary: {},
        otherColumns: [
            {}
        ]
    };


    $scope.hybridGrid = {
        selectedQuestions: {
            primaryQuestion: {},
            dynamicGridQuestion: [[]]
        },
        rows: hybridGridService.rows,
        columns: hybridGridService.columns,
        addElement: hybridGridService.addElement,
        addRow: function (rowIndex) {
            $scope.hybridGrid.selectedQuestions.dynamicGridQuestion[rowIndex] = [];
            hybridGridService.addRow(rowIndex);
        },
        removeElement: function (rowIndex, columnIndex) {
            $scope.hybridGrid.selectedQuestions.dynamicGridQuestion[rowIndex].splice(columnIndex, 1);
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
                $scope.grid.questions = response.data;
            });

        ThemeService.all().then(function (response) {
            $scope.themes = response.data;
        });

        var hybridGrid = function () {
            return {
                value: 'hybrid',
                text: 'Hybrid',
                hybrid: true,
                addMore: true,
                primary_questions_criteria: {is_primary: true},
                payload: function (selectedQuestions) {
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
                        'type': $scope.grid.gridType && $scope.grid.gridType.value,
                        'primary_question': $scope.selectedQuestions.primary.pk,
                        'columns': columns,
                        'subgroup': subGroupQuestions
                    }
                }
            }
        };


        var addMoreGrid = function () {
            return {
                value: 'allow_multiples',
                text: 'Add More',
                addMore: true,
                hybrid: false,
                primary_questions_criteria: {is_primary: true},
                payload: function (selectedQuestions) {
                    var columnsIds = selectedQuestions.otherColumns.map(function (question) {
                        return question && question.pk;
                    });
                    var gridType = $scope.grid.gridType;
                    return {
                        'type': gridType && gridType.value,
                        'primary_question': selectedQuestions.primary.pk,
                        'columns': columnsIds,
                        'csrfmiddlewaretoken': window.csrfToken
                    };
                }
            }
        };

        var DisplayAllGrid = function () {
            return {
                value: 'display_all',
                text: 'Display All',
                displayAll: true,
                primary_questions_criteria: {
                    is_primary: true,
                    answer_type: 'MultiChoice'
                },
                payload: function (selectedQuestions) {
                    var columnsIds = selectedQuestions.otherColumns.map(function (question) {
                        return question && question.pk;
                    });
                    var gridType = $scope.grid.gridType;
                    return {
                        'type': gridType && gridType.value,
                        'primary_question': selectedQuestions.primary.pk,
                        'columns': columnsIds,
                        'csrfmiddlewaretoken': window.csrfToken
                    };
                }

            }
        };

        $scope.types = [new DisplayAllGrid(), new addMoreGrid(), new hybridGrid()];
    };

    $scope.postNewGrid = function () {
        function createNewGrid() {
            if ($scope.newGrid.$valid && validateDynamicForms($scope.gridForm)) {
                $scope.error = '';
                var gridType = $scope.grid.gridType;
                var selectedQuestions = gridType.value == 'hybrid' ? $scope.hybridGrid.selectedQuestions : $scope.selectedQuestions;
                GridService.create($scope.subsectionId, gridType && gridType.payload(selectedQuestions))
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

    $scope.$watch('grid.gridType', function (type) {
        if (type) {
            $scope.grid.primaryQuestions = questionFilter($scope.grid.questions, type.primary_questions_criteria);
        }
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
    'ThemeService', 'GridService', 'hybridGridService', createGridController]);

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
    angular.element(document.getElementById('create-grid-controller')).scope().createGridModal(questionnaireId, subsectionId);
};