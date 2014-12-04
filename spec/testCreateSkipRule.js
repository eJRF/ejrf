describe("skip rule service", function() {

    beforeEach(module('questionnaireApp'));
    var scope, service, controller;


    describe("skip rule controller", function() {
        var rules = [{"name": "rule 1"}];
        var questions = {"questions": [{"name": "question 1"}]};
        var subsections = [{"name": "subsection 1"}];
        beforeEach(
            inject(function($rootScope, $q){
                var createPromise = function(value) {
                    var res = $q.defer();
                    res.resolve(value);
                    return res.promise;
                };

                scope = $rootScope.$new();
                service = {
                    getRules: function() {
                        return createPromise(rules);
                    },
                    getQuestions: function() {
                        var res = $q.defer();
                        res.resolve(questions);
                        return res.promise;
                    },
                    getSubsections: function() {
                        var res = $q.defer();
                        res.resolve(subsections);
                        return res.promise;
                    }
                };
                controller = new skipRuleController(scope, service);
            })
        );
        it("should set some intial values when calling reset", function() {
            expect(scope.activeTab).toEqual("newRuleTab");
            expect(scope.skipResult).toEqual({show: false});
            expect(scope.deleteResult).toEqual({});
            expect(scope.existingRules).toEqual([]);
            expect(scope.skipRule).toEqual({selectedQuestion: {}, rootQuestion: {}, csrfToken: window.csrfToken});
        });
        describe("updateSkipRuleModal", function() {
            it("should update rules", function() {
                scope.updateSkipRuleModal(1);
                scope.$digest();
                expect(scope.existingRules).toEqual(rules);
            });

            it("should update questions", function() {
                scope.updateSkipRuleModal(1);
                scope.$digest();
                expect(scope.questions).toEqual(questions.questions);
            });

            it("should update subsections", function() {
                scope.updateSkipRuleModal(1);
                scope.$digest();
                expect(scope.subsections).toEqual(subsections);
            });
        });
        describe("filterQuestions inside grid", function() {
            beforeEach(function() {
                scope.updateSkipRuleModal(12, 13);
                scope.$digest();
            });
            it("return false for questions who's parentQuestionGroup is not the grid", function() {
                var actualResult = scope.filterQuestions({"parentQuestionGroup": 24});
                expect(actualResult).toEqual(false);
            });
            it("return true for questions who's parentQuestionGroup is the grid", function() {
                var actualResult = scope.filterQuestions({"parentQuestionGroup": 13});
                expect(actualResult).toEqual(true);
            });
        });

        describe("getSubsectionTitle", function() {
            it("should return order and title when title exists", function() {
                var actualResult = scope.getSubsectionTitle({"title":"Test Title","order":1});
                expect(actualResult).toEqual("1. Test Title");
            });
            it("should return order and default text when title does not exists", function() {
                var actualResult = scope.getSubsectionTitle({"title":"","order":1});
                expect(actualResult).toEqual("1. [Un-named subsection]");
            });

        });

    });
});
