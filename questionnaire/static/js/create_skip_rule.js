var skipRules = skipRules || {};
skipRules.subsection = "";

var ngModule = angular.module('questionnaireApp', []);
ngModule.controller('SkipRuleController', ['$scope', '$http', 'skipRuleService', function ($scope, $http, skipRuleService) {

    $scope.fns = {};
    $scope.fns.createRule = function () {
    };
    $scope.questions = [];

    $scope.reset = function() {
        $scope.activeTab = "newRuleTab";
        $scope.existingRules = [];

        $scope.filterQuestions = function (question) { return true; };
        $scope.filterRules = function (rule) { return true; };
        $scope.skipRule = {selectedQuestion: {}, rootQuestion: {}, csrfToken: window.csrfToken};
        $scope.skipResult = {show: false};
        $scope.deleteResult = {};
    };
    $scope.reset();

    $scope.setActiveTab = function (activeTabName) {
        $scope.skipResult = {show: false};
        $scope.activeTab = activeTabName;
    };

    $scope.getSubsectionTitle = function (subsection) {
        var res = subsection.order + ". ";
        if (subsection.title !== '') {
            res += subsection.title;
        } else {
            res += "[Un-named subsection]";
        }
        return res;
    };

    $scope.matchSelectedQuestion = function (question) {
        return !($scope.skipRule.rootQuestion.pk == question.pk) && question.canSkip;
    };

    $scope.deleteRule = function (rule) {
        skipRuleService.deleteRule(rule.id).
            then(function(data) {
                $scope.deleteResult = data;
                updateRules($scope.subsectionId);
            });
    };

    var updateRules = function (subsectionId) {
        skipRuleService.getRules(subsectionId).
            then(function(data) {
                $scope.existingRules = data;
            });
    };

    var updateQuestions = function (subsectionId) {
        skipRuleService.getQuestions(subsectionId).
            then(function(data) {
                $scope.questions = data.questions;
            });
    };

    var updateSubsections= function (sectionId) {
        skipRuleService.getSubsections(sectionId).
            then(function(data) {
                $scope.subsections = data;
            });
    };

    $scope.updateSkipRuleModal = function (subsectionId, gridId) {
        $scope.reset();

        updateRules(subsectionId);
        updateQuestions(subsectionId);
        updateSubsections(window.sectionId);

        $scope.subsectionId = subsectionId;

        if (gridId != undefined) {
            $scope.subsectionTabHidden = true;
            $scope.filterQuestions = function (question) { return question.parentQuestionGroup == gridId; };
            $scope.filterRules = function (rule) { return rule.is_in_hygrid; };
        }
    };

    var getSkipRuleFormData = function (keyWord, value) {
        var formData = {
            "root_question": $scope.skipRule.rootQuestion.pk,
            "response": $scope.skipRule.questionResponse,
            "subsection": $scope.subsectionId,
            "csrfmiddlewaretoken": $scope.skipRule.csrfToken
        };
        formData[keyWord] = value;
        return formData;
    };

    var getQuestionFormData = function () {
        return getSkipRuleFormData("skip_question", $scope.skipRule.skipQuestion.pk);
    };

    var getSubsectionFormData = function () {
        return getSkipRuleFormdata("skip_subsection", $scope.skipRule.subsection.id);
    };

    var createSkipRule = function (postData) {
        $.post(window.url, postData)
            .done(function (data) {
                $scope.reset();
                $scope.$apply(function () {
                    $scope.skipResult = { className: "alert-success", message: data.result, show: true};
                });
                $scope.skipRule.subsectionId = postData.subsection;
                updateRules(postData.subsection);
            })
            .fail(function (data) {
                if (data.result) {
                    $scope.$apply(function () {
                        $scope.skipResult = { className: "alert-danger", message: data.result, show: true};
                    });
                } else {
                    $scope.$apply(function () {
                        $scope.skipResult = { className: "alert-danger", message: data.responseJSON.result.join(","), show: true};
                    });
                }
            });
    };

    $scope.submitQuestionForm = function () {
        var postData = getQuestionFormData();
        createSkipRule(postData);
    };


    $scope.submitSubsectionForm = function () {
        var postData = getSubsectionFormData();
        createSkipRule(postData);
    };
}]).run(function ($http) {
    $http.defaults.headers.common['X-CSRFToken'] = window.csrfToken;
});

ngModule.factory('skipRuleService', ['$http', '$q', function($http, $q) {
    var service = {};
    var getData = function(url) {
        var res = $q.defer();
        $http.get(url).
            success(function(data) {
                res.resolve(data);
            }).
            error(function() {
                res.reject("unable to get data");
            });
        return res.promise;
    };
    service.getRules = function(subsectionId) {
        return getData("/questionnaire/subsection/" + subsectionId + "/skiprules/");
    };

    service.getQuestions= function(subsectionId) {
        return getData("/questionnaire/subsection/" + subsectionId + "/questions/");
    };

    service.getSubsections = function(sectionId) {
        return getData("/questionnaire/section/" + window.sectionId + "/subsections/");
    };

    service.deleteRule = function(ruleId) {
        var res = $q.defer();
        $http.delete("/questionnaire/subsection/skiprule/" + ruleId + "/")
            .success(function (data, status) {
                res.resolve({ className: "alert-success", message: "Rule successfully deleted", show: true});
            })
            .error(function (data, status) {
                var message = "Rule was not deleted";
                if (status == 403) {
                    message = "You do not have permission to delete this rule";
                }
                res.resolve({ className: "alert-danger", message: message, show: true});
            });
        return res.promise;
    };

    return service;
}]);

skipRules.updateSubsection = function (subsectionId) {
    angular.element(document.getElementById('skip-rule-controller')).scope().updateSkipRuleModal(subsectionId);
};

skipRules.updateGrid = function (subsectionId, gridId) {
    angular.element(document.getElementById('skip-rule-controller')).scope().updateSkipRuleModal(subsectionId, gridId);
};
