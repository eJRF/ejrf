function setUpHTMLFixture() {
	$('body').append('<div>'
					+ '<option class="singleElementNoAttr" data-skip-rules></option>'
					+ '<option class="singleElementWithAttr" data-skip-rules="23"></option>'
					+'</div>');
}


describe("skip rules", function() {
    describe("getElementsToSkip", function() {    	
		setUpHTMLFixture();

    	it("should return an empty collection when passed an empty collection", function(){
			expect(applySkipRules.getElementsToSkip($('.nonexistentClass'), 'data-skip-rules').length).toEqual(0);
    	});
    	it("should return an empty collection when none of the elements have a value for data-skip-rule attribute", function(){
			expect(applySkipRules.getElementsToSkip($('.singleElementNoAttr'), 'data-skip-rules').length).toEqual(0);
    	});
    	
    	it("should return an single element collection when one elements has a data-skip-rule attribute", function(){
    		var actualResult = applySkipRules.getElementsToSkip($('.singleElementWithAttr'), 'data-skip-rules');
			expect(actualResult.length).toEqual(1);
			expect(actualResult[0]).toEqual('23');
    	});
    });
    describe("showElements", function() {
        var fns = {
            hide: function(val) { return; },
            show: function(val) { return; }
        };
    	it("should not call show if both lists are empty", function() {
    		spyOn(fns, 'show');
    		applySkipRules.showElements([],[]);
    		expect(fns.show.calls.length).toEqual(0);
    	});
    	it("should call show once if currently hidden questions has an id that is not in the questions to hide", function() {
    		spyOn(fns, 'show');
    		applySkipRules.showElements(["23"],[], fns.show);
    		expect(fns.show).toHaveBeenCalled();
    	});
    	it("should not call show currently hidden questions no ids", function() {
    		spyOn(fns, 'show');
    		applySkipRules.showElements([],["23","43"], fns.show);
    		expect(fns.show.calls.length).toEqual(0);
    	});
    	it("should not call show if both lists contain the same elements", function() {
    		spyOn(fns, 'show');
    		applySkipRules.showElements(["23","43"],["23","43"], fns.show);
    		expect(fns.show.calls.length).toEqual(0);
    	});
    });
});
