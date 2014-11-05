var skipRules = skipRules || {};

angular.module('questionnaireApp', [])
    .controller('SkipRuleController', ['$scope', function($scope) {
        $scope.skipRule = {selectedQuestion: {}, rootQuestion: {}};
        $scope.questions = [];
        $scope.matchSelectedQuestion = function(question) {
            return !($scope.skipRule.rootQuestion.pk == question.pk);
        };

<<<<<<< Updated upstream
=======
        var updateRules = function(subsectionId){
            $http.get( "/questionnaire/subsection/" + subsectionId + "/skiprules/").
                success(function(data, status, headers, config) {
                $scope.existingRules = data;
            });
        };

>>>>>>> Stashed changes
        $scope.updateSkipRuleModal = function(subsectionId) {
            $.get( "/questionnaire/subsection/" + subsectionId + "/questions/", function( data ) {
                var questions = data.questions;
                $scope.$apply(function() {
                    $scope.questions = questions;
                    $scope.skipRule = {selectedQuestion: {}, rootQuestion: {}};
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
                skip_question: $scope.skipRule.skipQuestion.pk
            };
        };

        $( "#sumbit-skip-rule" ).submit(function( event ) {
            event.preventDefault();
            data = getFormData();
            data.csrfmiddlewaretoken = $('#sumbit-skip-rule input[name=csrfmiddlewaretoken]').val();
            $.post($( "#sumbit-skip-rule" ).attr('action'), data)
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
        });
    }]);

skipRules.updateSubsection = function(subsectionId) {
    angular.element(document.getElementById('skip-rule-controller')).scope().updateSkipRuleModal(subsectionId);
};

skipRules.submit = function(event) {
    event.preventDefault();
};
