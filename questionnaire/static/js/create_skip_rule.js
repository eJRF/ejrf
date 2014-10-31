var skipRules = skipRules || {};

angular.module('questionnaireApp', [])
    .controller('SkipRuleController', ['$scope', function($scope) {
        $scope.skipRule = {selectedQuestion: {}, rootQuestion: {}};
        $scope.questions = [];
        $scope.matchSelectedQuestion = function(question) {
            return !($scope.skipRule.rootQuestion.pk == question.pk);
        };

        $scope.updateSkipRuleModal = function(subsectionId) {
            $.get( "/questionnaire/subsection/" + subsectionId + "/questions/", function( data ) {
                var questions = data.questions;
                $scope.$apply(function() {
                    $scope.questions = questions;
                    $scope.skipRule = {selectedQuestion: {}, rootQuestion: {}};
                    $scope.skipRule.subsectionId = subsectionId;
                });
            }, dataType="json");
        };
        $scope.fns = {};
        $scope.fns.createRule = function() {
            console.log($('#submit-skip-rule'));
        };

        var getFormData = function() {
            return {
                root_question: $scope.skipRule.rootQuestion.pk,
                response: $scope.skipRule.questionResponse,
                subsection: $scope.skipRule.subsectionId,
                skip_question: $scope.skipRule.skipQuestion.pk
            };
        };

        $( "#sumbit-skip-rule" ).submit(function( event ) {
            event.preventDefault();
            data = getFormData();
            data.csrfmiddlewaretoken = $('#sumbit-skip-rule input[name=csrfmiddlewaretoken]').val();
            $.post("/questionnaire/subsection/skiprules/", data)
                .done(function(data) {
                    console.log("success");
                })
                .fail(function(data) {
                    console.log("fail");
                });
        });
    }]);

skipRules.updateSubsection = function(subsectionId) {
    angular.element(document.getElementById('skip-rule-controller')).scope().updateSkipRuleModal(subsectionId);
};

skipRules.submit = function(event) {
    event.preventDefault();
};
