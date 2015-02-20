describe("create display all grid", function () {
    var scope, httpMock,
        subsectionId = 3,
        questionnaireId = 1,
        expectedTypes = ['display_all', 'allow_multiples', 'hybrid'],
        availableGridTypes = [
            {
                value: 'display_all',
                text: 'Display All',
                displayAll: true,
                primary_questions_criteria: {is_primary: true, answer_type: 'MultiChoice'},
                initialSelectedQuestions: {
                    primary: {},
                    otherColumns: [
                        {}
                    ]
                }
            },
            {
                value: 'allow_multiples',
                text: 'Add More',
                addMore: true,
                primary_questions_criteria: {is_primary: true},
                initialSelectedQuestions: {
                    primary: {},
                    otherColumns: [
                        {}
                    ]
                }
            },
            {
                value: 'hybrid',
                text: 'Hybrid',
                hybrid: true,
                addMore: true,
                primary_questions_criteria: {is_primary: true},
                initialSelectedQuestions: {
                    primaryQuestion: {},
                    dynamicGridQuestion: [
                        []
                    ]
                }
            }
        ],
        stubQuestions = [
            {
                pk: 186,
                fields: {
                    text: "PAB (protection at birth)",
                    theme: 6,
                    answer_type: "MultiChoice",
                    is_primary: true
                }
            }
        ];

    beforeEach(function () {
            module('gridModule');
            module('gridTypeFactories');
            module('gridService');
        }
    );


    describe("CreateGridController", function () {
        var initController,
            chooseGrid,
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

            inject(function ($controller, $rootScope, $httpBackend, AddMoreGridFactory, DisplayAllGridFactory, HybridGridFactory) {
                scope = $rootScope.$new();
                httpMock = $httpBackend;

                httpMock.when('GET', '/api/v1/themes/').respond(themeStub);

                initController = function () {
                    $controller('createGridController', {$scope: scope});
                };

                chooseGrid = function (type, real) {
                    var isReal = real || false;
                    var mapping_stubs = {displayAll: 0, addMore: 1, hybrid: 2};
                    var mapping_reals = {displayAll: DisplayAllGridFactory, addMore: AddMoreGridFactory, hybrid: HybridGridFactory};

                    if (isReal) {
                        scope.grid.gridType = mapping_reals[type].create();
                    } else {
                        scope.grid.gridType = availableGridTypes[mapping_stubs[type]];
                    }
                    scope.$apply();
                };

            });
        });

        it('should ensure  initial selected questions are set when grid type is chosen', function () {

            var url = '/api/v1/questions/?questionnaire=' + questionnaireId + '&unused=true';
            httpMock.expectGET(url).respond(stubQuestions);
            initController();

            var displayAll = availableGridTypes[0];
            var fakeSelctedQuestions = {};
            displayAll.initialSelectedQuestions = fakeSelctedQuestions;

            scope.grid.gridType = displayAll;
            scope.$apply();

            expect(scope.selectedQuestions).toEqual(fakeSelctedQuestions);
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
            chooseGrid('addMore', true);
            scope.selectedQuestions.addColumn();
            expect(scope.selectedQuestions.otherColumns).toEqual([
                {},
                {}
            ]);
        });

        it('should remove non-primary question column', function () {
            initController();
            chooseGrid('displayAll', true);
            scope.selectedQuestions.otherColumns = [
                {},
                {}
            ];

            scope.$apply();

            scope.selectedQuestions.removeColumn(1);
            expect(scope.selectedQuestions.otherColumns).toEqual([
                {}
            ]);

            scope.selectedQuestions.otherColumns = [
                {},
                {one: 1},
                {two: 2}
            ];

            scope.selectedQuestions.removeColumn(2);
            expect(scope.selectedQuestions.otherColumns).toEqual([
                {},
                {one: 1}
            ]);
        });

        it('should create grid modal', function () {
            initController();

            var url = '/api/v1/questions/?questionnaire=' + questionnaireId + '&unused=true';
            scope.createGridModal(questionnaireId, subsectionId);

            httpMock.expectGET(url).respond(stubQuestions);
            httpMock.flush();

            expect(scope.grid.questions).toEqual(stubQuestions);
            expect(scope.themes).toEqual(themeStub);
            var types = scope.types.map(function (type) {
                return type.value;
            });

            expect(types.length).toEqual(3);
            expect(types).toEqual(expectedTypes);
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

        it('should get new grid', function () {
            initController();

            var url = '/api/v1/questions/?questionnaire=' + questionnaireId + '&unused=true';
            scope.createGridModal(questionnaireId, subsectionId);

            httpMock.expectGET(url).respond(stubQuestions);
            httpMock.flush();

            expect(scope.grid.questions).toEqual(stubQuestions);
            expect(scope.themes).toEqual(themeStub);
            var types = scope.types.map(function (type) {
                return type.value;
            });

            expect(types.length).toEqual(3);
            expect(types).toEqual(expectedTypes);
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
                chooseGrid('displayAll', true);

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
                chooseGrid('displayAll', true);

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

        describe("grid primary question column", function () {
            it("should filter primary questions that are multichoice for display all grids", function () {

                initController();
                var url = '/api/v1/questions/?questionnaire=' + questionnaireId + '&unused=true';
                var non_primary_question = {
                    pk: 186,
                    model: "questionnaire.question",
                    fields: {
                        UID: "C00097",
                        created: "2014-12-17T12:31:19.231Z",
                        text: "PAB (protection at birth)",
                        theme: 6,
                        answer_type: "MultiChoice",
                        is_primary: false
                    }
                };

                var stubQuestions_with_non_primary = [stubQuestions[0], non_primary_question];
                httpMock.when('GET', url).respond(stubQuestions_with_non_primary);
                scope.createGridModal(questionnaireId, subsectionId);
                httpMock.flush();

                scope.grid.gridType = availableGridTypes[0];
                scope.$apply();

                expect(scope.grid.primaryQuestions).toEqual(stubQuestions);

            });

            it("should filter primary questions even non-multichoice for add more grids", function () {

                initController();
                var url = '/api/v1/questions/?questionnaire=' + questionnaireId + '&unused=true';
                var non_multi_choice_primary_question = {
                    pk: 186,
                    model: "questionnaire.question",
                    fields: {
                        UID: "C00097",
                        created: "2014-12-17T12:31:19.231Z",
                        text: "PAB (protection at birth)",
                        theme: 6,
                        answer_type: "numeric",
                        is_primary: true
                    }
                };

                var stubQuestions_with_non_multichoice_primary = [stubQuestions[0], non_multi_choice_primary_question];
                httpMock.when('GET', url).respond(stubQuestions_with_non_multichoice_primary);
                scope.createGridModal(questionnaireId, subsectionId);
                httpMock.flush();

                scope.grid.gridType = availableGridTypes[1];
                scope.$apply();

                expect(scope.grid.primaryQuestions).toEqual(stubQuestions_with_non_multichoice_primary);

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

    describe("satisfy filter", function () {
        it('should return question even if selected', function () {
            var question1 = {
                pk: 186,
                fields: {
                    theme: 6,
                    answer_type: "MultiChoice",
                    is_primary: true
                }
                },
                question2 = {
                    pk: 187,
                    fields: {
                        theme: 6,
                        answer_type: "Text",
                        is_primary: false
                    }
                };

            var questions = [question1, question2];
            var satisfyFilter = filterByCriteria();

            expect(satisfyFilter(questions, 'is_primary', false)).toEqual([question2]);
            expect(satisfyFilter(questions, 'is_primary', true)).toEqual([question1]);
            expect(satisfyFilter(questions, 'theme', 6)).toEqual(questions);
            expect(satisfyFilter(questions, 'answer_type', 'Text')).toEqual([question2]);
            expect(satisfyFilter(questions, 'answer_type', 'MultiChoice')).toEqual([question1]);
        });
    });

    describe("QuestionInput directive", function () {

        var answerInput, element, scope,
            initElement,
            ngElement,
            html;

        beforeEach(function () {
            module(function ($provide) {
                answerInput = jasmine.createSpyObj('AnswerInput', ['render']);
                $provide.value('AnswerInput', answerInput);
            });


            inject(function ($httpBackend, $compile, $rootScope) {
                scope = $rootScope;
                initElement = function (aHtml) {
                    ngElement = angular.element(aHtml);
                    element = $compile(ngElement)(scope);
                    scope.$digest();
                };
            });
        });

        describe("primaryQuestionInput", function () {
            beforeEach(function () {
                html = "<primary-question-input/>";
            });

            it('should call the rendering service', function () {
                var stubbedQuestion = {pk: 666, fields: {answer_type: 'text'}};
                scope.selectedQuestions = {primary: stubbedQuestion};
                initElement(html);
                expect(answerInput.render).toHaveBeenCalledWith(stubbedQuestion, element);
            });

        });

        describe("questionInput", function () {
            beforeEach(function () {
                html = "<question-input/>";
            });

            it('should call the rendering service', function () {
                var stubbedQuestion = {pk: 666, fields: {answer_type: 'text'}};
                scope.selectedQuestions = {otherColumns: [stubbedQuestion]};
                scope.$index = 0;
                initElement(html);
                expect(answerInput.render).toHaveBeenCalledWith(stubbedQuestion, element);
            });

        });


    });


});
