describe("assign questions", function () {
    var scope, httpMock,
        subsectionId = 3,
        questionUrl,
        themeUrl,
        questionnaireId = 1,
        unUsedStubQuestions = [
            {
                pk: 186,
                fields: {
                    text: "unused",
                    theme: 66,
                    answer_type: "MultiChoice",
                    is_primary: true
                }
            }
        ],
        usedStubQuestions = [
            {
                pk: 187,
                fields: {
                    text: 'used',
                    theme: 6,
                    answer_type: "MultiChoice",
                    is_primary: true
                }
            }
        ],
        themeStubs = [{
            pk: 6,
            fields: {
                description: "A placeholder theme for all questions.",
                name: "Common theme"
            }
        }];


    beforeEach(function () {
            module('assignQuestionsModule');
            module('gridService');
        }
    );

    describe("assignQuestionsController", function () {
        var initController;
        beforeEach(function () {
            inject(function ($controller, $rootScope, $httpBackend) {
                scope = $rootScope.$new();
                httpMock = $httpBackend;

                initController = function () {
                    $controller('assignQuestionController', {$scope: scope});
                };

            });
            questionUrl = '/api/v1/questions/';
            themeUrl = '/api/v1/themes/';
            httpMock.when('GET', '/api/v1/questions/?questionnaire=' + questionnaireId + '&unused=true').respond(unUsedStubQuestions);
            httpMock.when('GET', questionUrl).respond(unUsedStubQuestions.concat(usedStubQuestions));
            httpMock.when('GET', themeUrl).respond(themeStubs);
        });

        it('should fetch unused and all questions, mark if used, show them by default', function () {
            initController();
            httpMock.expectGET('/api/v1/questions/?questionnaire=' + questionnaireId + '&unused=true');
            httpMock.expectGET(questionUrl);


            scope.updateModal(questionnaireId, subsectionId);
            httpMock.flush();

            expect(scope.allQuestions).toContain({'question': unUsedStubQuestions[0], used: false});
            expect(scope.allQuestions).toContain({'question': usedStubQuestions[0], used: true});
        });

        it('should fetch all themes', function () {
            httpMock.expectGET(themeUrl).respond(themeStubs);

            initController();
            scope.updateModal(questionnaireId, subsectionId);

            httpMock.flush();
            expect(scope.allThemes).toEqual(themeStubs);
        });
    });

    describe("byTheme", function () {
        var wrappedunUsedStubQuestions = {'question': unUsedStubQuestions[0]},
            wrappedusedStubQuestions = {'question': usedStubQuestions[0]},
            wrappedAllQuestions = [wrappedusedStubQuestions, wrappedunUsedStubQuestions];

        it('should return all questions when no theme selected', function () {
            var byThemeFilter = filterByTheme();
            expect(byThemeFilter(wrappedAllQuestions, undefined)).toEqual(wrappedAllQuestions);
        });

        it('should return questions with selected theme', function () {
            var byThemeFilter = filterByTheme();
            expect(byThemeFilter(wrappedAllQuestions, {pk: 66})).toEqual([wrappedunUsedStubQuestions]);
            expect(byThemeFilter(wrappedAllQuestions, {pk: 6})).toEqual([wrappedusedStubQuestions]);
        });
    });

    describe("byUsed", function () {
        var wrappedunUsedStubQuestions = {'question': unUsedStubQuestions[0], used: false},
            wrappedusedStubQuestions = {'question': usedStubQuestions[0], used: true},
            wrappedAllQuestions = [wrappedusedStubQuestions, wrappedunUsedStubQuestions];

        it('should return all questions when no theme selected', function () {
            var byUsedFilter = filterByUsed();
            expect(byUsedFilter(wrappedAllQuestions, undefined)).toEqual(wrappedAllQuestions);
        });

        it('should return questions with selected theme', function () {
            var byUsedFilter = filterByUsed();
            expect(byUsedFilter(wrappedAllQuestions, true)).toEqual([wrappedunUsedStubQuestions]);
        });
    });
});