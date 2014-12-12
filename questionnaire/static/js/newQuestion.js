var app = angular.module('questionnaireApp', [])
    .controller('newQuestionController', ['$scope', function ($scope) {
        $scope.options = window.options || {};
        var questionOptions = window.questionOptions;
        $scope.knowOptions = 'custom';
        var clickCustomCount = 0;

        $scope.answerType = window.answerType || "";

        $scope.isAnswerTypeIsMultiChoice = function(){
            return $scope.answerType == 'MultipleResponse' || $scope.answerType == 'MultiChoice';
        };

        $scope.addOption = function() {
            $scope.existingQuestionOptions.push({});
        };


        $scope.removeOption = function(index) {
            if($scope.existingQuestionOptions.length > 1) {
                $scope.existingQuestionOptions.splice(index, 1);
            } else {
                $scope.existingQuestionOptions[0].text = "";
            }
        };
        $scope.answerTypeIsMultiChoice = $scope.answerType && $scope.isAnswerTypeIsMultiChoice();

        if (typeof window.answerSubType !== 'undefined'){
            $scope.answerSubType = { text: window.answerSubType, value: window.answerSubType };
        }

        $scope.existingQuestionOptions = window.questionOptions || [];

        var answerTypes = Object.keys(window.options);

        var options = answerTypes.map(function (key) {
            return { ansType: key, subTypes: $scope.options[key].map(function (subType) {
                return { 'text': subType, 'value': subType };
            })};
        });

        var createOptions = function(strOptions) {
            var options = strOptions.split(",");

            return options.map(function(option) {
                return {text: option};
            });
        };



        $scope.$watch('knowOptions', function(knownOption) {
            if (knownOption === 'custom') {
                if(clickCustomCount === 0) {
                    $scope.existingQuestionOptions = window.questionOptions
                        .filter(function(o) { return o != "" && o != null; })
                        .map(function(o) { return {text: o}; });
                } else {
                    $scope.existingQuestionOptions = [];
                }
                if($scope.existingQuestionOptions.length === 0) {
                    $scope.addOption();
                }
                clickCustomCount ++;
            } else {
                $scope.existingQuestionOptions = createOptions(knownOption);
            }
        });


        $scope.$watch('answerType', function (answerType) {
            var answerTypeToShow = options.filter(function (option) {
                return option.ansType == answerType;
            })[0];

            $scope.allOptions = answerTypeToShow && answerTypeToShow.subTypes;
        });
    }]);
