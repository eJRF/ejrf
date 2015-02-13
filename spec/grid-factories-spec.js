describe("grid Type Factories", function () {

    beforeEach(module('gridTypeFactories'));

    describe("hybridGridQuestionSelection", function () {
        var selectedQuestions;

        beforeEach(
            inject(function (hybridGridQuestionSelection) {
                selectedQuestions = new hybridGridQuestionSelection({}, []);
            })
        );

        it('should have initial primary question as object', function () {
            expect(selectedQuestions.primary).toEqual({});
        });

        it('should have initial dynamicQuestions an array of arrays of objects', function () {
            expect(selectedQuestions.dynamicGridQuestion).toEqual([
                [
                    {}
                ]
            ]);
        });

        it('should add element given row and column', function () {
            selectedQuestions.dynamicGridQuestion[1] = [
                {'row1': 'column0'},
                {'row1': 'column2'}
            ];
            selectedQuestions.addElement(1, 1);

            expect(selectedQuestions.dynamicGridQuestion).toEqual([
                [
                    {}
                ],
                [
                    {'row1': 'column0'},
                    {},
                    {'row1': 'column2'}
                ]
            ]);
        });

        it('should add new row', function () {
            selectedQuestions.dynamicGridQuestion[1] = [
                {'row1': 'column0'}
            ];
            selectedQuestions.addRow(2);
            expect(selectedQuestions.dynamicGridQuestion).toEqual([
                [
                    {}
                ],
                [
                    {'row1': 'column0'}
                ],
                [
                    {}
                ]
            ]);
        });

        it('should remove element given row and column', function () {
            selectedQuestions.dynamicGridQuestion[1] = [{'row1': 'column0'}, {'row1': 'column1'}, {'row1': 'column2'}];
            selectedQuestions.removeElement(1, 1);
            expect(selectedQuestions.dynamicGridQuestion).toEqual([[{}], [{'row1': 'column0'}, {'row1': 'column2'}]]);
        });

        it('should remove entire row if empty after removing element in the row', function () {
            selectedQuestions.dynamicGridQuestion[1] = [{'row1': 'column0'}];
            selectedQuestions.dynamicGridQuestion[2] = [{'row2': 'column0'}, {'row2': 'column2'}];
            selectedQuestions.removeElement(1, 0);
            expect(selectedQuestions.dynamicGridQuestion).toEqual([[{}], [{'row2': 'column0'}, {'row2': 'column2'}]]);
        });

        it('should return max columns length', function () {
            selectedQuestions.dynamicGridQuestion[1] = [{'row1': 'column0'}];
            selectedQuestions.dynamicGridQuestion[2] = [{'row2': 'column0'}, {'row2': 'column2'}];

            expect(selectedQuestions.maxColumns()).toEqual(2);
        });

        it('should allow adding columns if no rows has columns yet', function () {
            selectedQuestions.dynamicGridQuestion[1] = [{'row1': 'column0'}];
            expect(selectedQuestions.allowAddColumn(1)).toBeTruthy();
        });

        it('should allow adding columns if on row that already has columns', function () {
            selectedQuestions.dynamicGridQuestion[1] = [{'row1': 'column0'}, {'row1': 'column1'}, {'row1': 'column2'}];
            expect(selectedQuestions.allowAddColumn(1)).toBeTruthy();
        });

        it('should not allow adding columns if not on row that already has columns', function () {
            selectedQuestions.dynamicGridQuestion[1] = [{'row1': 'column0'}, {'row1': 'column1'}, {'row1': 'column2'}];
            selectedQuestions.dynamicGridQuestion[2] = [{'row2': 'column0'}];
            expect(selectedQuestions.allowAddColumn(2)).toBeFalsy();
        });
    });

    describe("NonHybridQuestionSelection", function () {
        var selectedQuestions;

        beforeEach(inject(function (NonHybridQuestionSelection) {
                selectedQuestions = new NonHybridQuestionSelection([], []);
            })
        );

        it('should have initial primary question as object', function () {
            expect(selectedQuestions.primary).toEqual({});
        });

        it('should have initial dynamicQuestions an array of objects', function () {
            expect(selectedQuestions.otherColumns).toEqual([
                {}
            ]);
        });

        it('should add column', function () {
            selectedQuestions.otherColumns = [
                {'row1': 'column0'},
                {'row1': 'column2'}
            ];
            selectedQuestions.addColumn(1);

            expect(selectedQuestions.otherColumns).toEqual([
                {'row1': 'column0'},
                {},
                {'row1': 'column2'}
            ]);
        });

        it('should remove element given index', function () {
            selectedQuestions.otherColumns = [
                {'row1': 'column0'},
                {'row1': 'column1'},
                {'row1': 'column2'}
            ];
            selectedQuestions.removeColumn(1);
            expect(selectedQuestions.otherColumns).toEqual([
                {'row1': 'column0'},
                {'row1': 'column2'}
            ]);
        });

        it('should move question to the left given index', function () {
            selectedQuestions.otherColumns = [
                {'row1': 'column0'},
                {'row1': 'column1'},
                {'row1': 'column2'},
                {'row1': 'column3'}
            ];
            selectedQuestions.moveLeft(2);
            expect(selectedQuestions.otherColumns).toEqual([
                {'row1': 'column0'},
                {'row1': 'column2'},
                {'row1': 'column1'},
                {'row1': 'column3'}
            ]);
        });
        it('should move question to the right given index', function () {
            selectedQuestions.otherColumns = [
                {'row1': 'column0'},
                {'row1': 'column1'},
                {'row1': 'column2'},
                {'row1': 'column3'}
            ];
            selectedQuestions.moveRight(1);
            expect(selectedQuestions.otherColumns).toEqual([
                {'row1': 'column0'},
                {'row1': 'column2'},
                {'row1': 'column1'},
                {'row1': 'column3'}
            ]);
        });

        it('should not move question to the left when index is 0', function () {
            selectedQuestions.otherColumns = [
                {'row1': 'column0'},
                {'row1': 'column1'}
            ];
            selectedQuestions.moveLeft(0);

            expect(selectedQuestions.otherColumns).toEqual([
                {'row1': 'column0'},
                {'row1': 'column1'}
            ]);
        });

        it('should not move question to the right when its index is last in the array', function () {
            selectedQuestions.otherColumns = [
                {'row1': 'column0'},
                {'row1': 'column1'}
            ];
            selectedQuestions.moveRight(1);
            expect(selectedQuestions.otherColumns).toEqual([
                {'row1': 'column0'},
                {'row1': 'column1'}
            ]);
        });

    });

    describe("NonHybridPayload", function () {
        var selectedQuestions = {},
            payLoadService,
            primaryQuestionPk = 666;

        beforeEach(function () {
            selectedQuestions.primary = {
                pk: primaryQuestionPk,
                fields: {text: "FAKE devil ", answer_type: "Text", is_primary: true}
            };
            selectedQuestions.otherColumns = [
                {pk: 224, fields: {text: "q4", answer_type: "Date"}},
                {pk: 225, fields: {text: "q5", answer_type: "Text"}},
                {pk: 142, fields: {text: "q6", answer_type: "Number"}}
            ];

            inject(function (NonHybridPayload) {
                payLoadService = NonHybridPayload;
            });
        });

        it('should generate payload', function () {
            var csrfToken = 'gkjb@mbzmcz';
            window.csrfToken = csrfToken;
            var gridType = 'add_more';
            var expectedPayload = {
                'csrfmiddlewaretoken': csrfToken,
                'type': gridType,
                'primary_question': primaryQuestionPk,
                'columns': [224, 225, 142]
            };

            expect(payLoadService.payload(selectedQuestions, gridType)).toEqual(expectedPayload);
        });
    });

    describe("HybridGridFactory", function () {
        var selectedQuestions,
            hybridGrid,
            primaryQuestionPk = 666;

        beforeEach(function () {

            module(function ($provide) {
                selectedQuestions = function () {
                    return {
                        primary: {
                            pk: primaryQuestionPk,
                            fields: {text: "FAKE devil ", answer_type: "Text", is_primary: true}
                        },
                        dynamicGridQuestion: [
                            [
                                {question: {pk: 149, fields: {text: "Name of person", answer_type: "Text"}}}
                            ],
                            [
                                {question: {pk: 224, fields: {text: "q4", answer_type: "Date"}}},
                                {question: {pk: 225, fields: {text: "q5", answer_type: "Text"}}}
                            ],
                            [
                                {question: {pk: 142, fields: {text: "Total Cases", answer_type: "Number"}}}
                            ]
                        ]
                    };
                };
                $provide.value('hybridGridQuestionSelection', selectedQuestions);
            });


            inject(function (HybridGridFactory) {
                hybridGrid = HybridGridFactory;
            });
        });

        it('should create hybridGrid', function () {
            var grid = hybridGrid.create();

            expect(grid.value).toEqual('hybrid');
            expect(grid.text).toEqual('Hybrid');
            expect(grid.hybrid).toEqual(true);
            expect(grid.addMore).toEqual(true);
            expect(grid.primary_questions_criteria).toEqual({is_primary: true});
            expect(grid.initialSelectedQuestions).toEqual(selectedQuestions());
        });

        it('should generate payload', function () {
            var csrfToken = 'gkjb@mbzmcz';
            window.csrfToken = csrfToken;
            var grid = hybridGrid.create(),
                expectedPayload = {
                    'csrfmiddlewaretoken': csrfToken,
                    'type': 'hybrid',
                    'primary_question': primaryQuestionPk,
                    'columns': [149, 224, 225, 142],
                    'subgroup': [224, 225]
                };

            expect(grid.payload()).toEqual(expectedPayload);
        });
    });

    describe("QuestionInitializer", function () {
        var question1 =
            {
                pk: 186,
                fields: {
                    text: "PAB (protection at birth)",
                    theme: 6,
                    is_primary: false
                }
            },
            question2 =
            {
                pk: 187,
                fields: {
                    text: "Another Question",
                    theme: 6,
                    is_primary: false
                }
            },
            primary = {
                pk: 188,
                fields: {
                    text: "PAB (protection at birth)",
                    theme: 6,
                    answer_type: "MultiChoice",
                    is_primary: true
                }
            },
            questionInitializer;

        beforeEach
        (inject(function (QuestionInitializer) {
                questionInitializer = QuestionInitializer;
            })
        );

        it('should have initial primary question an empty object and other columns as an array of objects', function () {
            var allQuestions = [],
                grid = {};

            var initial = questionInitializer.init(grid, allQuestions);
            expect(initial.primary).toEqual({});
            expect(initial.otherColumns).toEqual([{}]);
        });

        it('should set the primary question from questions given gridIds', function () {
            var allQuestions = [question1, question2, primary],
                gridQuestionIds = [question1.pk, question2.pk, primary.pk],
                grid = {fields: {question: gridQuestionIds}};


            var initial = questionInitializer.init(grid, allQuestions);
            expect(initial.primary).toEqual(primary);
            expect(initial.otherColumns).toEqual([question1, question2]);
        });
    });

    describe("HybridQuestionInitializer", function () {
        var question1 =
            {
                pk: 186,
                fields: {
                    text: "PAB (protection at birth)",
                    theme: 6,
                    is_primary: false
                }
            },
            question2 =
            {
                pk: 187,
                fields: {
                    text: "Another Question",
                    theme: 6,
                    is_primary: false
                }
            },
            primary = {
                pk: 188,
                fields: {
                    text: "PAB (protection at birth)",
                    theme: 6,
                    answer_type: "MultiChoice",
                    is_primary: true
                }
            },
            questionInitializer;

        beforeEach(inject(function (hybridGridQuestionInitializer) {
                questionInitializer = hybridGridQuestionInitializer;
            })
        );

        it('should have initial primary question an empty object and other columns as an array of objects', function () {
            var allQuestions = [],
                orders = [],
                grid = {};

            var initial = questionInitializer.init(grid, allQuestions, orders);
            expect(initial.primary).toEqual({});
            expect(initial.dynamicGridQuestion).toEqual([[{}]]);
        });

        it('should set the primary question from questions given gridIds', function () {
            var allQuestions = [question1, question2, primary],
                orders = [{fields: {order: 1, question: primary.pk}},
                    {fields: {order: 0, question: primary.pk}},
                    {fields: {order: 1, question: question1.pk}},
                    {fields: {order: 2, question: question2.pk}}],

                gridQuestionIds = [question1.pk, question2.pk, primary.pk],
                grid = {fields: {question: gridQuestionIds}, children: []};

            var initial = questionInitializer.init(grid, allQuestions, orders);
            expect(initial.primary).toEqual(primary);
            expect(initial.dynamicGridQuestion).toEqual([[{question: question1}], [{question: question2}]]);
        });
    });
});
