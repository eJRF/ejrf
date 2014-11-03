var skipRules = skipRules || {};
skipRules.subsection = "";

angular.module('questionnaireApp', [])
    .controller('SkipRuleController', ['$scope', '$http', function($scope, $http) {
        var resetSkipRule = function() {
            $scope.skipRule = {selectedQuestion: {}, rootQuestion: {}, csrfToken: window.csrfToken};
        };
        resetSkipRule();
        $scope.questions = [];
        $scope.existingRules = [];
        $scope.matchSelectedQuestion = function(question) {
            return !($scope.skipRule.rootQuestion.pk == question.pk);
        };

        var updateRules = function(subsectionId){
            $http.get( "/questionnaire/subsection/" + subsectionId + "/skiprules/").
                success(function(data, status, headers, config) {
                $scope.existingRules = data;
            });
        }

        $scope.updateSkipRuleModal = function(subsectionId) {
            updateRules(subsectionId);

            $http.get( "/questionnaire/subsection/" + subsectionId + "/questions/").
                success(function(data, status, headers, config) {
                    var questions = data.questions;
                    resetSkipRule();
                    $scope.questions = questions;
                    $scope.skipRule.subsectionId = subsectionId;
                    $scope.skipResult = {show: false};
                });
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
            if($scope.skipForm.$valid) {
                postData = getFormData();
                $.post(window.url, postData)
                    .done(function(data) {
                        resetSkipRule();
                        $scope.$apply(function() {
                            $scope.skipResult = { className: "alert-success", message: data.result, show: true};
                        });
                        $scope.skipRule.subsectionId = postData.subsection;
                        updateRules(postData.subsection);

                    })
                    .fail(function(data) {
                        $scope.$apply(function() {
                            $scope.skipResult = { className: "alert-danger", message: data.result, show: true};
                        });
                    });
            }
        };
    }]);

skipRules.updateSubsection = function(subsectionId) {
    angular.element(document.getElementById('skip-rule-controller')).scope().updateSkipRuleModal(subsectionId);
};
