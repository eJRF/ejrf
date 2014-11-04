jQuery(function ($) {
    var allRadiosAndSelects = $("select, :radio");

    var skipRuleScope = {
        questions: [],
        add: function (hiddenQuestion) {
            if (!this.isElem(hiddenQuestion)) {
                this.questions.push(hiddenQuestion);
            }
        },
        isElem: function (question) {
            var self = this;
            return this.questions.filter(function (item) {
                return self.isEql(question, item);
            }).length > 0
        },
        isEql: function (question, other) {
            return question.element == other.element && question.skipQuestion == other.skipQuestion;
        },
        pop: function (question) {
            var self = this;
            this.questions = this.questions.filter(function (qn) {
                return !self.isEql(question, qn);
            });
        }
    };

    var hideQuestion = function (element) {
        var skipQuestionId = $(element).parent('label').parent('li').attr('data-skip-rules');
        if (skipQuestionId) {
            skipRuleScope.add({element: element, skipQuestion: skipQuestionId});
            var qnGroupFormDiv = $('.form-group-question-' + skipQuestionId);
            qnGroupFormDiv.removeClass('show');
            qnGroupFormDiv.addClass('hide');
        }
    };

    var showQuestion = function (element) {
        var skipQuestionId = $(element).parent('label').parent('li').attr('data-skip-rules');
        if (skipQuestionId) {
            skipRuleScope.pop({element: element, skipQuestion: skipQuestionId});
            var qnFormGroupDiv = $('.form-group-question-' + skipQuestionId);
            qnFormGroupDiv.removeClass('hide');
            qnFormGroupDiv.addClass('show');
        }
    };

    allRadiosAndSelects.map(function () {
        var element = this;
        $(this).on('change', function () {
            var allSiblings = $(element).parent('label').parent('li').siblings().andSelf();
            allSiblings.map(function (_, item) {
                var inputElement = $(item).children('label').children('input');
                if (inputElement.length) {
                    var el = inputElement[0];
                    if (skipRuleScope.isElem({element: el, skipQuestion: $(item).attr('data-skip-rules')})) {
                        showQuestion(el);
                    }
                }
            });
            hideQuestion(element);
        });
    })
});