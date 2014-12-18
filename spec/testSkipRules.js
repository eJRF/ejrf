function setUpHTMLFixture(html) {
    $('body').append(html);
}

var fns = {
    hide: function(val) { return; },
    show: function(val) { return; }
};

describe("skip rules", function() {

    beforeEach(function() {
        $('body').html('<div></div>');
    });

    describe('Skipping Simple Questions', function(){
        describe("getElementsToSkip", function() {
            var unselectedOptions = '<div>'
                    + '<select>'
                    + '<option class="singleElementNoAttr" data-skip-rules></option>'
                    + '<option class="singleElementWithAttr" data-skip-rules="23"></option>'
                    + '</select>'
                    +'</div>';

            setUpHTMLFixture(unselectedOptions);

            var gridInstanceRule = new scopedSkipRules($('body'), 'data-skip-rules', fns.hide, fns.show);

            it("should return an empty collection when passed an empty collection", function(){
                expect(gridInstanceRule.getElementsToSkip().length).toEqual(0);
            });

            it("should return an single element collection when one elements has a data-skip-rule attribute and a ", function(){
                var html = '<div>'
                    + '<select>'
                    + '<option class="singleElementNoAttr" data-skip-rules></option>'
                    + '<option class="singleElementWithAttr" data-skip-rules="23" selected="selected"></option>'
                    + '</select>'
                    +'</div>'
                setUpHTMLFixture(html)

                var actualResult = gridInstanceRule.getElementsToSkip();
                gridInstanceRule.hideQuestions()
                expect(actualResult.length).toEqual(1);
                expect(actualResult[0]).toEqual('23');
            });
        });

        describe("showElements", function() {
            it("should not call show if both lists are empty", function() {
                spyOn(fns, 'show');
                var gridInstanceRule = new scopedSkipRules($('body'), 'data-skip-rules', fns.hide, fns.show);

                gridInstanceRule.showGridElements([]);
                expect(fns.show.calls.length).toEqual(0);
            });

            it("should call show once if currently hidden questions has an id that is not in the questions to hide", function() {
                spyOn(fns, 'show');
                var gridInstanceRule = new scopedSkipRules($('body'), 'data-skip-rules', fns.hide, fns.show);

                gridInstanceRule.hiddenQuestionIds.push("22", '43')
                gridInstanceRule.showGridElements(["23"]);

                expect(fns.show).toHaveBeenCalledWith("22");
                expect(fns.show).toHaveBeenCalledWith("43");
             });

            it("should not call show currently hidden questions no ids", function() {
                spyOn(fns, 'show');
                var gridInstanceRule = new scopedSkipRules($('body'), 'data-skip-rules', fns.hide, fns.show);

                gridInstanceRule.showGridElements(["23"]);
                expect(fns.show.calls.length).toEqual(0);
            });

            it("should not call show if both lists contain the same elements", function() {
                spyOn(fns, 'show');
                var gridInstanceRule = new scopedSkipRules($('body'), 'data-skip-rules', fns.hide, fns.show);

                gridInstanceRule.hiddenQuestionIds.push("23", '43')

                gridInstanceRule.showGridElements(["23","43"]);
                expect(fns.show.calls.length).toEqual(0);
            });
        });

        describe('getAllSelectedResponses', function(){
            it('returns the selected HTML nodes', function(){
                var html = '<div>'
                    + '<select>'
                    + '<option class="singleElementNoAttr" data-skip-rules></option>'
                    + '<option class="singleElementWithAttr" data-skip-rules="23" selected="selected"></option>'
                    + '</select>'
                    +'</div>'
                setUpHTMLFixture(html)
                var gridInstanceRule = new scopedSkipRules($('body'), 'data-skip-rules', fns.hide, fns.show);
                var actualResult = gridInstanceRule.getAllSelectedResponses()
                expect(actualResult.length).toEqual(1);
            });
        });
    });
});
