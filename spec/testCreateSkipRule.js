describe("skip rule service", function() {

    beforeEach(module('questionnaireApp'));
    var scope, service, controller;

    describe("skip rule controller", function() {
        beforeEach(
            inject(function($rootScope){
                scope = $rootScope.$new();
                service = {};
                controller = new skipRuleController(scope, {});
            })
        );
        it("should set some intial values when calling reset", function() {
            expect(scope.activeTab).toEqual("newRuleTab");
        });
    });
});
