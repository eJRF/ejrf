describe("create display all grid", function () {

    beforeEach(module('questionnaireApp'));
    var scope, httpMock, stubQuestions,
        subsectionId = 3,
        questionnaireId = 1;


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
            };

        beforeEach(function () {
            inject(function ($controller, $rootScope, $httpBackend) {
                scope = $rootScope.$new();
                httpMock = $httpBackend;

                httpMock.when('GET', '/api/v1/themes/').respond(themeStub);

                initController = function () {
                    $controller('createGridController', {$scope: scope});
                }
            })
        });

        it('should ensure there are empty initial primary and non-primary questions', function () {
            initController();
            expect(scope.selectedQuestions.primary).toEqual({});
            expect(scope.selectedQuestions.otherColumns).toEqual([{}]);
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
            expect(scope.selectedQuestions.otherColumns).toEqual([{}, {}]);
        });

        it('should remove non-primary question column', function () {
            initController();
            scope.selectedQuestions.otherColumns = [{}, {}];

            scope.grid.removeColumn(1);
            expect(scope.selectedQuestions.otherColumns).toEqual([{}]);

            scope.selectedQuestions.otherColumns = [{}, {one: 1}, {two: 2}];

            scope.grid.removeColumn(2);
            expect(scope.selectedQuestions.otherColumns).toEqual([{}, {one: 1}]);
        });

        it('should create grid modal', function () {
            initController();

            stubQuestions = [{
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
            }];
            var url = '/api/v1/questions/?questionnaire=' + questionnaireId + '&unused=true';
            scope.createGridModal(questionnaireId, subsectionId);

            httpMock.expectGET(url).respond(stubQuestions);
            httpMock.flush();

            expect(scope.grid.questions).toEqual(stubQuestions);
            expect(scope.themes).toEqual(themeStub);
            expect(scope.types).toEqual([{value: 'display_all', text: 'Display All'}]);
        });

        it('should post new grid', function () {
            initController();

            stubQuestions = [{
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
            }];
            var url = '/api/v1/questions/?questionnaire=' + questionnaireId + '&unused=true';
            scope.createGridModal(questionnaireId, subsectionId);

            httpMock.expectGET(url).respond(stubQuestions);
            httpMock.flush();

            expect(scope.grid.questions).toEqual(stubQuestions);
            expect(scope.themes).toEqual(themeStub);
            expect(scope.types).toEqual([{value: 'display_all', text: 'Display All'}]);
        });

        describe('Post Grid', function () {
            it('should add form errors and backend errors on failure', function () {

                var errorMessage = 'Something went wrong';
                var url = '/subsection/' + subsectionId + '/grid/new/';
                var backendError = 'Some errors';
                httpMock.expectPOST(url).respond(400, [{message: errorMessage, form_errors: [backendError]}]);
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
                httpMock.expectPOST(url).respond(200, [{message: successMessage}]);
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
});
