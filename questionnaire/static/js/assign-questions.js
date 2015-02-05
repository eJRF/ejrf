if (typeof assignQuestions == 'undefined') {
    var assignQuestions = {};
}

var assignQuestionsModule = angular.module('assignQuestionsModule', ['gridService']);

var assignQuestionController = function ($scope, QuestionService, ThemeService) {

    $scope.allThemes = [];
    $scope.updateModal = function (questionnaireId, _) {
        ThemeService.all().then(function (response) {
            $scope.allThemes = response.data;
        });
        QuestionService.filter({questionnaire: questionnaireId, unused: true})
            .then(function (response) {
                var unUsedQuestionsPks = response.data.map(function (question) {
                    return question.pk;
                });
                QuestionService.all()
                    .then(function (response) {
                        var unmarkedQuestions = response.data;
                        $scope.allQuestions = unmarkedQuestions && unmarkedQuestions.map(function (question) {
                            var used = (unUsedQuestionsPks.indexOf(question.pk) == -1);
                            return {question: question, used: used}
                        });
                    });
            });
    };
};

assignQuestionsModule.controller('AssignQuestionController', ['$scope', 'QuestionService', 'ThemeService', assignQuestionController]);

var filterByTheme = function () {
    return function (questions, selectedTheme) {
        if (!selectedTheme){
            return questions;
        }

        return questions.filter(function (wrappedQuestion) {
            return wrappedQuestion.question.fields.theme == selectedTheme.pk;
        });
    };
};

assignQuestionsModule.filter('byTheme', filterByTheme);

assignQuestions.updateModal = function (questionnaireId, subsectionId) {
    angular.element(document.getElementById('assign-question-controller')).scope().updateModal(questionnaireId, subsectionId);
};