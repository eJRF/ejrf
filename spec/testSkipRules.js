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
    		// console.log($('.singleElementWithAttr'));
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

    describe("hideQuestions", function() {
    	it("should not hide any questions when no radios or selects have been seleceted", function() {
			spyOn($.fn, 'hide');
			SkipRules.hideQuestions([],[]);
			expect($.fn.hide.calls.length).toEqual(0);
    	});
    	it("should call hide once hide for one radio being selected", function() {
			spyOn($.fn, 'hide');
			SkipRules.hideQuestions(["1"],[]);
			expect($.fn.hide.calls.length).toEqual(1);
    	});
    	it("should call hide once hide for one select being selected", function() {
			spyOn($.fn, 'hide');
			SkipRules.hideQuestions([],["2"]);
			expect($.fn.hide.calls.length).toEqual(1);
    	});

    	it("should call hide twice hide for one select being selected and one radio buttun being selected", function() {
			spyOn($.fn, 'hide');
			SkipRules.hideQuestions(["1"],["2"]);
			expect($.fn.hide.calls.length).toEqual(2);
    	});
    });
});
