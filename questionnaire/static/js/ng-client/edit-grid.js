if (typeof editGrid == 'undefined') {
    var editGrid = {};
}

var editGridModule = angular.module('editGridModule', ['gridService', 'gridTypeFactories']);

var editGridController = function ($scope, $q, GridService, QuestionService, DisplayAllGridFactory, AddMoreGridFactory, HybridGridFactory) {
        $scope.grid = {
            selectedTheme: {},
            gridType: {},
            questions: [],
            reOrderedOptions: []
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

            function initializeType(grid, allQuestions) {
                var deferred = $q.defer();
                if (grid.fields.hybrid) {
                    return GridService.orders(grid.pk).then(function (response) {
                        return response.data;
                    }).then(function (orders) {
                        return HybridGridFactory.create(grid, allQuestions, orders);
                    });
                }
                if (grid.fields.allow_multiples) {
                    deferred.resolve(AddMoreGridFactory.create(grid, allQuestions));
                    return deferred.promise;
                }
                deferred.resolve(DisplayAllGridFactory.create(grid, allQuestions));
                return deferred.promise;
            }

            GridService.fetch(gridId).then(function (gridResponse) {
                $scope.loading = true;
                var gridData = gridResponse.data;

                QuestionService.all().then(function (allQuestionsResponse) {
                    var allQuestions = allQuestionsResponse.data;
                    QuestionService.filter({questionnaire: questionnaireId, unused: true}).then(function (response) {
                        initializeType(gridData, allQuestions).then(function (type) {
                            var unUsedQuestions = response.data;
                            $scope.selectedQuestions = type.initialSelectedQuestions;
                            var usedQuestions = $scope.selectedQuestions.questions;
                            $scope.grid.questions = usedQuestions.concat(unUsedQuestions);

                            var primaryQuestion = $scope.selectedQuestions.primary;
                            $scope.grid.selectedTheme = getTheme(primaryQuestion);
                            $scope.grid.gridType = type;
                            $scope.loading = false;
                            QuestionService.options(primaryQuestion).then(function (response) {
                                $scope.grid.questionOptions = response.data;
                            });
                        });
                    });
                });
            });
        };

        var updateQuestionOptionOrders = function () {
            var primaryQuestion = $scope.selectedQuestions.primary;
            var payload = {options: $scope.grid.reOrderedOptions};
            QuestionService.updateOptions(primaryQuestion, payload)
                .success(function (data) {
                    $scope.message = data.message;
                })
                .error(function (err) {
                    $scope.message = err.message;
                });
        };

        $scope.postUpdateGrid = function () {
            var gridType = $scope.grid.gridType;


            if ($scope.editGridForm.$valid && validateDynamicForms($scope.gridForm)) {
                $scope.error = '';
                GridService.update($scope.gridId, gridType.payload())
                    .success(function (response) {
                        if ($scope.grid.reOrderedOptions.length) {
                            updateQuestionOptionOrders();
                        }
                        $scope.message = response.message;
                        $scope.gridFormErrors.formHasErrors = false;
                    }).error(function (response) {
                        $scope.error = response.error;
                        $scope.gridFormErrors.formHasErrors = true;
                        $scope.gridFormErrors.backendErrors = response.form_errors;
                    });
            } else {
                $scope.gridFormErrors.formHasErrors = true;
                $scope.error = 'The are errors in the form. Please fix them and submit again.';
                $scope.message = '';
            }
        };
    }
    ;

editGridModule.controller('EditGridController', editGridController);

function reArrange(elem) {
    var tableRow = $(elem).find('tbody tr');
    return $.map(tableRow, function (row) {
        return $(row).data('option');
    });
}

function reorderedQuestionRows(elem) {
    var tableRow = $(elem).find('tbody tr');
    return $.map(tableRow, function (row) {
        return $(row).find('td.drag');
    }).map(function (td) {
        return $(td).data('option');
    }).filter(function (row) {
        return row;
    });
}

editGridModule.directive('dndTable', function () {
    return {
        restrict: 'A',
        scope: false,
        link: function ($scope, elem) {
            $(elem).sortable({
                containerSelector: 'table',
                itemPath: '>tbody',
                itemSelector: '.tr-sortable',
                onDrop: function ($item, _, _super) {
                    $scope.grid.reOrderedOptions = reArrange(elem, $item);
                    callOnDropSuper($item);
                }
            });
        }
    }
});

editGridModule.directive('hybridDndTable', function () {
    return {
        restrict: 'A',
        scope: false,
        link: function ($scope, elem) {
            $(elem).sortable({
                containerSelector: 'table',
                itemPath: '>tbody',
                itemSelector: '.tr-sortable',
                handle: '.drag',
                onDrop: function ($item, _, _super) {
                    $scope.selectedQuestions.dynamicGridQuestion = reorderedQuestionRows(elem);
                    callOnDropSuper($item);
                }
            });
        }
    }
});

editGrid.updateEditGridScope = function (questionnaireId, subsectionId, gridId) {
    angular.element(document.getElementById('edit-grid-controller')).scope().updateScope(questionnaireId, subsectionId, gridId);
};
