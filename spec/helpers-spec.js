describe("Helpers", function () {
    describe("transformRequestHelper", function () {
        it('should transform object pots data', function () {
            var obj = {
                type: "display_all",
                primary_question: 186,
                columns: [198, 199]
            };
            var transformedObj = 'type=display_all&primary_question=186&columns=198&columns=199';

            expect(transformRequestHelper(obj)).toEqual(transformedObj);

        });
    });

    describe("validateDynamicForms", function () {
        it('should be true when grid fields of form are valid', function () {
            var gridForm = {someField: {$valid: true}, anotherField: {$valid: true}};

            expect(validateDynamicForms(gridForm)).toEqual(true);
        });

        it('should be false when any grid form field is invalid', function () {
            var gridForm = {invalidField: {$valid: true}, someField: {$valid: false}};
            var filename = validateDynamicForms(gridForm);

            expect(filename).toEqual(false);
        });
    });

    describe("questions filter", function () {

        var criteria = {is_primary: true, answer_type: 'MultiChoice'};

        it('should accept both fields matching', function () {
            expect(questionFilterCriteria({is_primary: true, answer_type: 'MultiChoice',
                other_field: 'hehe1'}, criteria)).toEqual(true);
        });

        it('should reject if first field not matching', function () {
            expect(questionFilterCriteria({is_primary: false, answer_type: 'MultiChoice',
                other_field: 'hehe2'}, criteria)).toEqual(false);
        });

        it('should reject if second field not matching', function () {
            expect(questionFilterCriteria({is_primary: true, answer_type: 'Numeric',
                other_field: 'hehe3'}, criteria)).toEqual(false);
        });

        it('should reject if  both fields not matching', function () {
            expect(questionFilterCriteria({is_primary: false, answer_type: 'Numeric',
                other_field: 'hehe4'}, criteria)).toEqual(false);
        });

        it('should filter  questions with fields satisfying criteria', function () {
            var questions = [
                {name: 'haha1', fields: {is_primary: true, answer_type: 'MultiChoice', other_field: 'hehe1'}},
                {name: 'haha2', fields: {is_primary: false, answer_type: 'MultiChoice', other_field: 'hehe2'}},
                {name: 'haha3', fields: {is_primary: true, answer_type: 'Numeric', other_field: 'hehe3'}},
                {name: 'haha4', fields: {is_primary: false, answer_type: 'Numeric', other_field: 'hehe4'}},
            ];

            var expected = [
                {name: 'haha1', fields: {is_primary: true, answer_type: 'MultiChoice', other_field: 'hehe1'}}
            ];

            expect(questionFilter(questions, criteria)).toEqual(expected);
        });

    });

})
;