function setUpHTMLFixture(html) {
    $('body').append(html);
}

describe("skip rules", function() {

    describe('Skipping Simple Questions', function(){
        describe("getElementsToSkip", function() {
            var unselectedOptions = '<div>'
                    + '<select>'
                    + '<option class="singleElementNoAttr" data-skip-rules></option>'
                    + '<option class="singleElementWithAttr" data-skip-rules="23"></option>'
                    + '</select>'
                    +'</div>';

            setUpHTMLFixture(unselectedOptions);

            var questionSelector = '.form-group-question-';
            var scope = $('body');

            var hideFn = function(val) {
                scope.find(questionSelector + val).hide();
            };
            var showFn = function(val) {
                scope.find(questionSelector + val).show();
            };

            var gridInstanceRule = new scopedSkipRules(scope, 'data-skip-rules', hideFn, showFn);

            it("should return an empty collection when passed an empty collection", function(){
                expect(gridInstanceRule.getElementsToSkip().length).toEqual(0);
            });

            it("should return an single element collection when one elements has a data-skip-rule attribute and a ", function(){
                var html = '<div>'
                    + '<select>'
                    + '<option class="singleElementNoAttr" data-skip-rules></option>'
                    + '<option class="singleElementWithAttr" data-skip-rules="23" selected></option>'
                    + '</select>'
                    +'</div>'
                setUpHTMLFixture(html)

                var actualResult = gridInstanceRule.getElementsToSkip();
                expect(actualResult.length).toEqual(1);
                expect(actualResult[0]).toEqual('23');
            });
        });

        describe("showElements", function() {
           var html = '<div class="grid-group">'
            + '<select>'
            + '<option class="singleElementNoAttr" data-skip-rules></option>'
            + '<option class="singleElementWithAttr" data-skip-rules="23" selected></option>'
            + '</select>'
            +'</div>'

            var fns = {
                hide: function(val) { return; },
                show: function(val) { return; }
            };

            var gridInstanceRule = new scopedSkipRules($('.grid-group'), 'data-skip-rules', fns.hide, fns.show);

            it("should not call show if both lists are empty", function() {
                spyOn(fns, 'show');
                gridInstanceRule.showGridElements([]);
                expect(fns.show.calls.length).toEqual(0);
            });

            xit("should call show once if currently hidden questions has an id that is not in the questions to hide", function() {
                spyOn(fns, 'show');
                gridInstanceRule.hiddenQuestionIds.push("22")
                gridInstanceRule.showGridElements(["23"]);
                expect(fns.show.calls.length).toEqual(1);
             });
            xit("should not call show currently hidden questions no ids", function() {
                spyOn(fns, 'show');
                applySkipRules.showGridElements([],["23","43"], fns.show);
                expect(fns.show.calls.length).toEqual(0);
            });
            xit("should not call show if both lists contain the same elements", function() {
                spyOn(fns, 'show');
                applySkipRules.showGridElements(["23","43"],["23","43"], fns.show);
                expect(fns.show.calls.length).toEqual(0);
            });
        });
    });
});
