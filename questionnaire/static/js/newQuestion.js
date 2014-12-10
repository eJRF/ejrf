var app = angular.module('questionnaireApp', [])
    .controller('newQuestionController', ['$scope', function ($scope) {
        $scope.options = window.options ? window.options : [];

        $scope.answerType = window.answerType || "";

        if (typeof window.answerSubType !== 'undefined'){
            $scope.answerSubType = { text: window.answerSubType, value: window.answerSubType }
        }

        var answerTypes = Object.keys(window.options);
        var options = answerTypes.map(function (key) {
            return { ansType: key, subTypes: $scope.options[key].map(function (subType) {
                return { 'text': subType, 'value': subType };
            })}
        });

        $scope.$watch('answerType', function (answerType) {
            var answerTypeToShow = options.filter(function (option) {
                return option.ansType == answerType
            })[0];

            $scope.allOptions = answerTypeToShow && answerTypeToShow.subTypes
        });
    }]);