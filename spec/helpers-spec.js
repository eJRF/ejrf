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

});