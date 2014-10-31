var skipRules = skipRules || {};
skipRules.subsection = "";

angular.module('questionnaireApp', [])
    .controller('SkipRuleController', ['$scope', '$http', function($scope, $http) {
        var resetSkipRule = function() {
            $scope.skipRule = {selectedQuestion: {}, rootQuestion: {}, csrfToken: window.csrfToken};
        };
        resetSkipRule();
        $scope.questions = [];
        $scope.matchSelectedQuestion = function(question) {
            return !($scope.skipRule.rootQuestion.pk == question.pk);
        };

        $scope.updateSkipRuleModal = function(subsectionId) {
            $.get( "/questionnaire/subsection/" + subsectionId + "/questions/", function( data ) {
                var questions = data.questions;
                $scope.questions = questions;
                $scope.$apply(function() {
                    // resetSkipRule();
                    $scope.questions = questions;
                    $scope.skipRule.subsectionId = subsectionId;
                    $scope.skipResult = {show: false};
                });
            }, dataType="json");
        };
        $scope.fns = {};
        $scope.fns.createRule = function() {
        };

        var getFormData = function() {
            return {
                root_question: $scope.skipRule.rootQuestion.pk,
                response: $scope.skipRule.questionResponse,
                subsection: $scope.skipRule.subsectionId,
                skip_question: $scope.skipRule.skipQuestion.pk,
                csrfmiddlewaretoken: $scope.skipRule.csrfToken
            };
        };

        $scope.submitForm = function() {
            console.log($scope.skipForm);
            data = getFormData();
            $.post(window.url, data)
                .done(function(data) {
                    $scope.$apply(function() {
                        $scope.skipResult = { className: "alert-success", message: data.result, show: true};
                    });
                })
                .fail(function(data) {
                    $scope.$apply(function() {
                        $scope.skipResult = { className: "alert-danger", message: data.result, show: true};
                    });
                });
        };
    }]);

skipRules.updateSubsection = function(subsectionId) {
    angular.element(document.getElementById('skip-rule-controller')).scope().updateSkipRuleModal(subsectionId);
};

skipRules.submit = function(event) {
    event.preventDefault();
};
