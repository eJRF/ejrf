if (typeof createGrid == 'undefined') {
    var createGrid = {};
}

var createGridController = function ($scope, $http) {
    $scope.selectedQuestions = {primary: {}, otherColumns: [{}]};
    $scope.grid = {questions: [], questionOptions: [], gridType: '', selectedTheme: ''};
    $scope.gridForm = {backendErrors: []};
    $scope.subsectionId = $scope.subsectionId || "";

    $scope.grid.addColumn = function () {
        $scope.selectedQuestions.otherColumns.push({});
    };

    $scope.grid.removeColumn = function (index) {
        $scope.selectedQuestions.otherColumns.splice(index, 1);
    };

    $scope.createGridModal = function (questionnaireId, subsectionId) {
        $scope.subsectionId = subsectionId;
        $http.get('/api/v1/questions/?questionnaire=' + questionnaireId + '&unused=true').then(function (response) {
            $scope.grid.questions = response.data;
        });

        $http.get('/api/v1/themes/').then(function (response) {
            $scope.themes = response.data;
        });

        $scope.types = [{value: 'display_all', text: 'Display All'}]
    };

    $scope.postNewGrid = function () {
        var columnsIds = $scope.selectedQuestions.otherColumns.map(function (question) {
            return question && question.pk;
        });
        var payload = {
            'type': $scope.grid.gridType.value,
            'primary_question': $scope.selectedQuestions.primary.pk,
            'columns': columnsIds,
            'csrfmiddlewaretoken': window.csrfToken
        };

        var url = '/subsection/' + $scope.subsectionId + '/grid/new/';

        var transformRequestHelper = function (obj) {
            var str = [];
            for (var key in obj) {
                var value = obj[key];
                if (Array.isArray(value)) {
                    value.forEach(function (column) {
                        str.push(encodeURIComponent(key) + "=" + encodeURIComponent(column));
                    })
                } else {
                    str.push(encodeURIComponent(key) + "=" + encodeURIComponent(value));
                }
            }
            return str.join("&");
        };

        function createNewGrid() {
            if ($scope.newGrid.$valid && validateDynamicForms($scope.gridForm)) {
                $scope.error = '';
                $http({
                    method: 'POST',
                    url: url,
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    transformRequest: transformRequestHelper,
                    data: payload
                }).success(function (response) {
                    $scope.message = response[0].message;
                }).error(function (response) {
                    $scope.error = response[0].message;
                    $scope.newGrid.primary_question.$invalid = true;
                    $scope.newGrid.type.$invalid = true;

                    $scope.gridForm.backendErrors = response[0].form_errors;
                });
            } else {
                $scope.error = 'The are errors in the form. Please fix them and submit again.';
                $scope.message = '';
            }
        }

        var validateDynamicForms = function (dynamicForm) {
            Object.keys(dynamicForm).forEach(function (key) {
                if (!dynamicForm[key].$valid) {
                    return false;
                }
            });
            return true;
        };
        createNewGrid();
    };

    $scope.$watch('selectedQuestions.primary', function (selectedPrimary) {
        $scope.selectedQuestions.primary = selectedPrimary;
        selectedPrimary && selectedPrimary.pk &&
        $http.get('/api/v1/question/' + selectedPrimary.pk + '/options/').then(function (response) {
            $scope.grid.questionOptions = response.data;
        });
    });
};

ngModule.controller('CreateGridController', ['$scope', '$http', createGridController]);

ngModule.filter('notSelected', function () {
    return function (questions, existingColumnQuestions, index) {
        return questions.filter(function (question) {
            var questionIndex = existingColumnQuestions.indexOf(question);
            return questionIndex == -1 || questionIndex == index;
        });
    };
});

ngModule.run(function ($http) {
    $http.defaults.headers.common['X-CSRFToken'] = window.csrfToken;
});

createGrid.updateCreateGrid = function (questionnaireId, subsectionId) {
    angular.element(document.getElementById('create-grid-controller')).scope().createGridModal(questionnaireId, subsectionId);
};