if (typeof createGrid == 'undefined') {
    var createGrid = {};
}

var createGridController = function ($scope, $http) {
    $scope.questions = [];
    $scope.options = [];
    $scope.selectedQuestions = {primary: {}};
    $scope.createGridModal = function (questionnaireId) {
        $http.get('/api/v1/questions/?questionnaire='+ questionnaireId +'&unused=true').then(function (response) {
            $scope.questions = response.data;
        });

        $http.get('/api/v1/themes/').then(function (response) {
            $scope.themes = response.data;
        });

        $scope.types = ['Display All']
    };


    $scope.$watch('selectedQuestions.primary', function (selectedPrimary) {
        selectedPrimary.pk &&
            $http.get('/api/v1/question/'+ selectedPrimary.pk +'/options/').then(function (response) {
                $scope.questionOptions = response.data;
            });
    });

};

ngModule.controller('CreateGridController', ['$scope', '$http', createGridController]);
createGrid.updateCreateGrid = function (questionnaireId) {
    angular.element(document.getElementById('create-grid-controller')).scope().createGridModal(questionnaireId);
};