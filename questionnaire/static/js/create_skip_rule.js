var skipRules = skipRules || {};
skipRules.subsection = "";

angular.module('questionnaireApp', [])
    .controller('SkipRuleController', ['$scope', '$http', function($scope, $http) {
        $scope.activeTab = "newRuleTab";
        $scope.setActiveTab = function(activeTabName){
            $scope.activeTab = activeTabName;
        };

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
        };
        var updateCreateQuestionRuleForm = function(subsectionId) {
            $http.get( "/questionnaire/subsection/" + subsectionId + "/questions/").
                success(function(data, status, headers, config) {
                    var questions = data.questions;
                    resetSkipRule();
                    $scope.questions = questions;
                    $scope.skipRule.subsectionId = subsectionId;
                    $scope.skipResult = {show: false};
                });
        };

        var updateCreateSubsectionRuleForm = function(subsectionId) {
            $http.get( "/questionnaire/section/" + window.sectionId + "/subsections/").
                success(function(data, status, headers, config) {
                    $scope.subsections = data;

                    resetSkipRule();
                    $scope.skipRule.subsectionId = subsectionId;
                    $scope.skipResult = {show: false};
                });
        };

        $scope.updateSkipRuleModal = function(subsectionId) {
            updateRules(subsectionId);
            updateCreateQuestionRuleForm(subsectionId);
            updateCreateSubsectionRuleForm(subsectionId);
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

        var getSubsectionFormData = function() {
            return {
                root_question: $scope.skipRule.rootQuestion.pk,
                response: $scope.skipRule.questionResponse,
                subsection: $scope.skipRule.subsectionId,
                skip_subsection: $scope.skipRule.subsection.id,
                csrfmiddlewaretoken: $scope.skipRule.csrfToken
            };
        };

        $scope.submitQuestionForm = function() {
            var postData = getFormData();
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
                    if(data.result){
                        $scope.$apply(function() {
                            $scope.skipResult = { className: "alert-danger", message: data.result, show: true};
                        });
                    } else {
                        $scope.$apply(function() {
                            $scope.skipResult = { className: "alert-danger", message: data.responseJSON.result.join(","), show: true};
                        });
                    }
                });
        };


        $scope.submitSubsectionForm = function() {
            var postData = getSubsectionFormData();
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
                    if(data.result){
                        $scope.$apply(function() {
                            $scope.skipResult = { className: "alert-danger", message: data.result, show: true};
                        });
                    } else {
                        $scope.$apply(function() {
                            $scope.skipResult = { className: "alert-danger", message: data.responseJSON.result.join(","), show: true};
                        });
                    }
                });
        };
    }]);

skipRules.updateSubsection = function(subsectionId) {
    angular.element(document.getElementById('skip-rule-controller')).scope().updateSkipRuleModal(subsectionId);
};
