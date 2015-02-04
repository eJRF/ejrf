describe("grid Type Factories", function () {

    beforeEach(module('gridTypeFactories'));

    describe("hybridGridQuestionSelection", function () {
        var selectedQuestions;

        beforeEach(
            inject(function (hybridGridQuestionSelection) {
                selectedQuestions = hybridGridQuestionSelection;
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
            selectedQuestions.dynamicGridQuestion[1] = [{'row1': 'column0'},{'row1': 'column1'},{'row1': 'column2'}];
            selectedQuestions.removeElement(1, 1);
            expect(selectedQuestions.dynamicGridQuestion).toEqual([[{}],[{'row1': 'column0'},{'row1': 'column2'}]]);
        });

        it('should remove entire row if empty after removing element in the row', function () {
            selectedQuestions.dynamicGridQuestion[1] = [{'row1': 'column0'}];
            selectedQuestions.dynamicGridQuestion[2] = [{'row2': 'column0'},{'row2': 'column2'}];
            selectedQuestions.removeElement(1, 0);
            expect(selectedQuestions.dynamicGridQuestion).toEqual([[{}],[{'row2': 'column0'},{'row2': 'column2'}]]);
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
                selectedQuestions = NonHybridQuestionSelection;
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
    });

    describe("NonHybridPayload", function () {
        var selectedQuestions = {},
            payLoadService,
            primaryQuestionPk = 666;

        beforeEach(function () {
            selectedQuestions.primary = {pk: primaryQuestionPk, fields: { text: "FAKE devil ", answer_type: "Text", is_primary: true}};
            selectedQuestions.otherColumns = [
                {pk: 224, fields: {text: "q4", answer_type: "Date" }},
                {pk: 225, fields: {text: "q5", answer_type: "Text" }},
                {pk: 142, fields: {text: "q6", answer_type: "Number" }}
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
        var selectedQuestions = {},
            hybridGrid,
            primaryQuestionPk = 666;

        beforeEach(function () {

            module(function ($provide) {
                selectedQuestions.primary = {pk: primaryQuestionPk, fields: { text: "FAKE devil ", answer_type: "Text", is_primary: true}};
                selectedQuestions.dynamicGridQuestion = [
                    [
                        {question: {pk: 149, fields: {text: "Name of person", answer_type: "Text" }}}
                    ],
                    [
                        {question: {pk: 224, fields: {text: "q4", answer_type: "Date"}}},
                        {question: {pk: 225, fields: {text: "q5", answer_type: "Text" }}}
                    ],
                    [
                        {question: {pk: 142, fields: {text: "Total Cases", answer_type: "Number"}}}
                    ]
                ];

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
            expect(grid.initialSelectedQuestions).toEqual(selectedQuestions);
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
});
