describe("create hybrid grid", function () {

    beforeEach(module('gridTypeFactories'));

    describe("hybridGridQuestionSelection", function(){
        var selectedQuestions;

        beforeEach(
            inject(function(hybridGridQuestionSelection){
                selectedQuestions = hybridGridQuestionSelection;
            })
        );

        it('should have initial primary question as object', function(){
            expect(selectedQuestions.primary).toEqual({});
        });

        it('should have initial dynamicQuestions an array of arrays of objects', function(){
            expect(selectedQuestions.dynamicGridQuestion).toEqual([[{}]]);
        });

        it('should add element given row and column', function(){
            selectedQuestions.dynamicGridQuestion[1] = [{'row1': 'column0'},  {'row1': 'column2'}];
            selectedQuestions.addElement(1,1);

            expect(selectedQuestions.dynamicGridQuestion).toEqual([[{}], [{'row1': 'column0'}, {}, {'row1': 'column2'}]]);
        });

        it('should add new row', function(){
            selectedQuestions.dynamicGridQuestion[1] = [{'row1': 'column0'}];
            selectedQuestions.addRow(2);
            expect(selectedQuestions.dynamicGridQuestion).toEqual([[{}], [{'row1': 'column0'}], [{}]]);
        });

        it('should remove element given row and column', function(){
            selectedQuestions.dynamicGridQuestion[1] = [{'row1': 'column0'}, {'row1': 'column1'}, {'row1': 'column2'}];
            selectedQuestions.removeElement(1,1);
            expect(selectedQuestions.dynamicGridQuestion).toEqual([[{}], [{'row1': 'column0'}, {'row1': 'column2'}]]);
        });
    });

});
