describe("create display all grid", function () {

    beforeEach(module('gridModule'));
    var scope, httpMock, stubQuestions,
        subsectionId = 3,
        questionnaireId = 1,
        questionService;


    describe("CreateGridController", function () {
        var initController,
            themeStub = {
                pk: 6,
                model: "questionnaire.theme",
                fields: {
                    region: null,
                    description: "A placeholder theme for all questions.",
                    modified: "2014-04-03T15:05:03.225Z",
                    name: "Common theme",
                    created: "2014-04-03T15:05:03.215Z"
                }
            },
            availableGridTypes = [
                {value: 'display_all', text: 'Display All', displayAll: true},
                {value: 'allow_multiples', text: 'Add More', addMore: true}
            ];

        beforeEach(function () {

            inject(function ($controller, $rootScope, $httpBackend, QuestionService) {
                scope = $rootScope.$new();
                httpMock = $httpBackend;

                httpMock.when('GET', '/api/v1/themes/').respond(themeStub);

                initController = function () {
                    $controller('createGridController', {$scope: scope, 'QuestionService': QuestionService});
                };

            });
        });

        it('should ensure there are empty initial primary and non-primary questions', function () {

            initController();
            expect(scope.selectedQuestions.primary).toEqual({});
            expect(scope.selectedQuestions.otherColumns).toEqual([
                {}
            ]);
        });

        it('should ensure there are empty initial grid attributes', function () {
            initController();

            expect(scope.grid.questions).toEqual([]);
            expect(scope.grid.questionOptions).toEqual([]);
            expect(scope.grid.gridType).toEqual('');
            expect(scope.grid.selectedTheme).toEqual('');
            expect(scope.grid.primaryQuestions).toEqual([]);
        });

        it('should set initial grid form errors', function () {
            initController();
            expect(scope.gridFormErrors).toEqual({backendErrors: [], formHasErrors: false});
        });

        it('should add new non-primary question column', function () {
            initController();
            scope.grid.addColumn();
            expect(scope.selectedQuestions.otherColumns).toEqual([
                {},
                {}
            ]);
        });

        it('should remove non-primary question column', function () {
            initController();
            scope.selectedQuestions.otherColumns = [
                {},
                {}
            ];

            scope.grid.removeColumn(1);
            expect(scope.selectedQuestions.otherColumns).toEqual([
                {}
            ]);

            scope.selectedQuestions.otherColumns = [
                {},
                {one: 1},
                {two: 2}
            ];

            scope.grid.removeColumn(2);
            expect(scope.selectedQuestions.otherColumns).toEqual([
                {},
                {one: 1}
            ]);
        });

        it('should create grid modal', function () {
            initController();

            stubQuestions = [
                {
                    pk: 186,
                    model: "questionnaire.question",
                    fields: {
                        UID: "C00097",
                        created: "2014-12-17T12:31:19.231Z",
                        text: "PAB (protection at birth)",
                        theme: 6,
                        answer_type: "MultiChoice",
                        is_primary: true
                    }
                }
            ];
            var url = '/api/v1/questions/?questionnaire=' + questionnaireId + '&unused=true';
            scope.createGridModal(questionnaireId, subsectionId);

            httpMock.expectGET(url).respond(stubQuestions);
            httpMock.flush();

            expect(scope.grid.questions).toEqual(stubQuestions);
            expect(scope.themes).toEqual(themeStub);
            expect(scope.types).toEqual(availableGridTypes);
        });

        it('should get question options when themes change', function () {
            initController();

            var questionId = 1;
            var url = '/api/v1/question/' + questionId + '/options/';
            var questionsOptions = [
                {text: 'Disease', pk: 1, question_id: questionId}
            ];
            httpMock.expectGET(url).respond(questionsOptions);

            scope.selectedQuestions = {primary: {pk: questionId}};
            scope.$apply();
            httpMock.flush();

            expect(scope.grid.questionOptions).toEqual(questionsOptions);
        });

        it('should get question options when primary question changes', function () {
            initController();
            scope.selectedQuestions = {primary: ''};
            scope.$apply();

            expect(scope.grid.questionOptions).toEqual([]);
        });

        it('should get question options when theme changes', function () {
            initController();
            scope.selectedTheme = '';
            scope.$apply();

            expect(scope.grid.questionOptions).toEqual([]);
        });

        it('should post new grid', function () {
            initController();

            stubQuestions = [
                {
                    pk: 186,
                    model: "questionnaire.question",
                    fields: {
                        UID: "C00097",
                        created: "2014-12-17T12:31:19.231Z",
                        text: "PAB (protection at birth)",
                        theme: 6,
                        answer_type: "MultiChoice",
                        is_primary: true
                    }
                }
            ];
            var url = '/api/v1/questions/?questionnaire=' + questionnaireId + '&unused=true';
            scope.createGridModal(questionnaireId, subsectionId);

            httpMock.expectGET(url).respond(stubQuestions);
            httpMock.flush();

            expect(scope.grid.questions).toEqual(stubQuestions);
            expect(scope.themes).toEqual(themeStub);

            expect(scope.types).toEqual(availableGridTypes);
        });

        describe('Post Grid', function () {
            it('should add form errors and backend errors on failure', function () {

                var errorMessage = 'Something went wrong';
                var url = '/subsection/' + subsectionId + '/grid/new/';
                var backendError = 'Some errors';
                httpMock.expectPOST(url).respond(400, [
                    {message: errorMessage, form_errors: [backendError]}
                ]);
                initController();
                scope.subsectionId = subsectionId;

                scope.newGrid = {$valid: true};
                scope.gridForm = {someField: {$valid: true}};

                scope.postNewGrid();
                httpMock.flush();

                expect(scope.gridFormErrors.backendErrors).toEqual([backendError]);
                expect(scope.gridFormErrors.formHasErrors).toBeTruthy();
                expect(scope.error).toEqual(errorMessage);
            });

            it('should add return success message when form is valid', function () {
                var successMessage = 'Grid was created';
                var url = '/subsection/' + subsectionId + '/grid/new/';
                httpMock.expectPOST(url).respond(200, [
                    {message: successMessage}
                ]);
                initController();
                scope.subsectionId = subsectionId;

                scope.newGrid = {$valid: true};
                scope.gridForm = {someField: {$valid: true}};

                scope.postNewGrid();
                httpMock.flush();

                expect(scope.gridFormErrors.formHasErrors).toBeFalsy();
                expect(scope.message).toEqual(successMessage);
            });

            it('should show errors and not not post when form is not valid', function () {
                var errorMessage = 'The are errors in the form. Please fix them and submit again.';
                initController();

                scope.newGrid = {$valid: false};
                scope.gridForm = {someField: {$valid: true}};
                scope.postNewGrid();
                expect(scope.error).toEqual(errorMessage);
            });
        });
    });
    describe("notSelectedFilter", function () {
        it('should return unselected questions', function () {
            var allQuestions = [11, 22, 33, 44, 55],
                selectedQuestions = [22, 33];

            var unselectedQuestionsFilter = notSelectedFilter();
            expect(unselectedQuestionsFilter(allQuestions, selectedQuestions, 4)).toEqual([11, 44, 55]);
        });

        it('should return question even if selected', function () {
            var allQuestions = [11, 22, 33, 44, 55],
                selectedQuestions = [22, 33];

            var unselectedQuestionsFilter = notSelectedFilter();
            expect(unselectedQuestionsFilter(allQuestions, selectedQuestions, 1)).toEqual([11, 33, 44, 55]);
            expect(unselectedQuestionsFilter(allQuestions, selectedQuestions, 0)).toEqual([11, 22, 44, 55]);
        });
    });
});
