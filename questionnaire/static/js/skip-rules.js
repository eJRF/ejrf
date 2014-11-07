jQuery(function ($) {
    var allRadios = $(":radio");

    var allOptions = $("select");

    var allQuestionsToSkipFromSelects = [];
    var allQuestionsToSkipFromRadios = [];

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
        drop: function (question) {
            var self = this;
            this.questions = this.questions.filter(function (qn) {
                return !self.isEql(question, qn);
            });
        }
    };

    var hideQuestion = function (element) {

        var skipQuestionId = getIdToHide(element);
        if (skipQuestionId) {
            skipRuleScope.add({element: element, skipQuestion: skipQuestionId});
            hideQuestionById(skipQuestionId);
        }
    };

    var hideQuestionById = function (id) {
        var qnGroupFormDiv = $('.form-group-question-' + id);
        qnGroupFormDiv.removeClass('show');
        qnGroupFormDiv.addClass('hide');

    };
    var showQuestionById = function (id) {
        var qnFormGroupDiv = $('.form-group-question-' + id);
        qnFormGroupDiv.removeClass('hide');
        qnFormGroupDiv.addClass('show');
    }

    var showQuestion = function (element) {
        var skipQuestionId = getIdToHide(element)
        if (skipQuestionId) {
            skipRuleScope.drop({element: element, skipQuestion: skipQuestionId});
        }
    };

    allRadios.map(function (_, element) {
        $(this).on('change', function () {
            var allRadios = $('[type="radio"]:checked');
            var currentSkipQuestions = allRadios.map(function (index, val) {
                if (val.attributes['data-skip-rules']) {
                    return val.attributes['data-skip-rules'].value;
                } else {
                    return false;
                }
//                if (this.selected && this.attributes['data-skip-rule']) {
//                    return this.attributes['data-skip-rule'].value;
//                } else {
//                    return false;
//                }
            })
                .filter(function (index, val) {
                    return val !== false;
                })

            allQuestionsToSkipFromRadios.map(function (index, val) {
                if ($.inArray(val, currentSkipQuestions) == -1) {
                    showQuestionById(val);
                }
            })
            allQuestionsToSkipFromRadios = currentSkipQuestions;
            //diff with allQuestionsToSkipFromSelects and hide or show based on the diff
            currentSkipQuestions.extend(allQuestionsToSkipFromSelects).map(function (index, val) {
                hideQuestionById(val);
            })


//            var allSiblings = $(element).parent('label').parent('li').siblings().andSelf();
//            var el = $(element)[0];
//            console.log($(el).children());
//            allSiblings.map(function (_, item) {
//                var inputElement = $(item).children('label').children('input');
//                if (inputElement.length) {
//                    var el = inputElement[0];
//                    if (skipRuleScope.isElem({element: el, skipQuestion: $(item).attr('data-skip-rules')})) {
//                        showQuestion(el);
//                    }
//                }
//            });
//            hideQuestion(element);
        });
    });


    allOptions.map(function (_, element) {
        $(this).on('change', function (element) {

            var currentQuestionsToSkip = $('option')
                .map(function () {
                    if (this.selected && this.attributes['data-skip-rule']) {
                        return this.attributes['data-skip-rule'].value;
                    } else {
                        return false;
                    }
                })
                .filter(function (index, val) {
                    return val !== false;
                })

            allQuestionsToSkipFromSelects.map(function (index, val) {
                if ($.inArray(val, currentQuestionsToSkip) == -1) {
                    showQuestionById(val);
                }
            })
            allQuestionsToSkipFromSelects = currentQuestionsToSkip;
            //diff with allQuestionsToSkipFromSelects and hide or show based on the diff
            currentQuestionsToSkip.extend(allQuestionsToSkipFromRadios).map(function (index, val) {
                hideQuestionById(val);
            })
        });

    });

    function getIdToHide(element) {
        if ($(element).is('select')) {
            return $('#' + $(element).attr('id') + ' :selected').data('skip-rule');
        } else {
            return $(element).parent('label').parent('li').attr('data-skip-rules');
        }
    }

    function getIdToShow(element) {

    }

})
;
//when select an option we add root-question, response, question to skip to array, remove old rules
//when any select or radio changes we hide all of the the questions in the array
