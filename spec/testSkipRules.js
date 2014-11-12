function setUpHTMLFixture() {
	$('body').append('<div>'
					+ '<option class="singleElementNoAttr" data-skip-rules></option>'
					+ '<option class="singleElementWithAttr" data-skip-rules="23"></option>'
					+'</div>');
}


describe("skip rules", function() {
    describe("getQuestionIdsToSkip", function() {    	
		setUpHTMLFixture();

    	it("should return an empty collection when passed an empty collection", function(){
			expect(SkipRules.getQuestionIdsToSkip($('.nonexistentClass')).length).toEqual(0);
    	});
    	it("should return an empty collection when none of the elements have a value for data-skip-rule attribute", function(){
			expect(SkipRules.getQuestionIdsToSkip($('.singleElementNoAttr')).length).toEqual(0);
    	});
    	
    	it("should return an single element collection when one elements has a data-skip-rule attribute", function(){
    		var actualResult = SkipRules.getQuestionIdsToSkip($('.singleElementWithAttr'));
			expect(actualResult.length).toEqual(1);
			expect(actualResult[0]).toEqual('23');
    	});
    });
    describe("showQuestions", function() {
    	it("should not call show if both lists are empty", function() {
    		spyOn($.fn, 'show');
    		SkipRules.showQuestions([],[]);
    		expect($.fn.show.calls).toEqual([]);
    	});
    	it("should call show once if currently hidden questions has an id that is not in the questions to hide", function() {
    		spyOn($.fn, 'show');
    		SkipRules.showQuestions(["23"],[]);
    		expect($.fn.show).toHaveBeenCalled();
    	});
    	it("should not call show currently hidden questions no ids", function() {
    		spyOn($.fn, 'show');
    		SkipRules.showQuestions([],["23","43"]);
    		expect($.fn.show.calls.length).toEqual(0);
    	});
    	it("should not call show if both lists contain the same elements", function() {
    		spyOn($.fn, 'show');
    		SkipRules.showQuestions(["23","43"],["23","43"]);
    		expect($.fn.show.calls.length).toEqual(0);
    	});
    });
});
