var unselectedOptions = '<div>'
                    + '<option class="singleElementNoAttr" data-skip-rules></option>'
                    + '<option class="singleElementWithAttr" data-skip-rules="23"></option>'
                    +'</div>';

var gridInstance = '<div class="hybrid-group-row">' +
                    '<div class="col-sm-5 center-fields">' +
                        '<input type="hidden" id="id_MultiChoice-1-response" name="MultiChoice-1-response" value="0,55">' +
                        '<input type="hidden" id="id_MultiChoice-1-response" name="MultiChoice-1-response" value="" exclude="true">' +
                        '<ul>' +
                            '<li>' +
                                '<label for="id_MultiChoice-1-response_0">' +
                                    '<input id="id_MultiChoice-1-response_0" name="MultiChoice-1-response" type="radio" value="61"> Acellular</label>' +
                            '</li>' +
                            '<li>' +
                                '<label for="id_MultiChoice-1-response_1">' +
                                    '<input checked="checked" id="id_MultiChoice-1-response_1" name="MultiChoice-1-response" type="radio" value="62"> Whole cell </label>'+
                            '</li>' +
                        '</ul>' +
                    '</div>';
var otherSelectedOption =  '<div class="col-sm-5 center-fields">' +
                           '<input type="hidden" id="id_MultiChoice-6-response" name="MultiChoice-6-response" value="0,56">' +
                           '     <select id="id_MultiChoice-6-response" name="MultiChoice-6-response">' +
                           '         <option value="" selected="selected">Choose One</option>' +
                           '         <option value="73">UNICEF, WHO or PAHO</option>' +
                           '         <option value="74">donating agency</option>' +
                           '         <option value="72">government agency</option>' +
                           '         <option value="75">other</option>' +
                           '     </select>' +
                           ' </div>';

function setUpHTMLFixture(html) {
    $('body').append(html);
}


describe("skip rules", function() {

    describe('Skipping Simple Questions', function(){
        describe("getElementsToSkip", function() {
            setUpHTMLFixture(unselectedOptions);

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

    describe('Skipping In Hybrid Group', function(){

        describe("getallSelectedResponses", function() {

            it('should get empty collection when no radions are selected in the body', function(){
                setUpHTMLFixture(unselectedOptions);

                var selectedOptions = applySkipRules.getAllSelectedResponses($('.hybrid-group-row'));
                expect(selectedOptions.length).toEqual(0);
            });

            it('should get all selected checkboxes in a grid', function(){
                setUpHTMLFixture(gridInstance);

                var selectedOptions = applySkipRules.getAllSelectedResponses($('.hybrid-group-row'));
                expect(selectedOptions.length).toEqual(1);
            });

            it('should get all selected checkboxes in the page', function(){
                var gridInstance = gridInstance + otherSelectedOption;
                setUpHTMLFixture(gridInstance);

                var selectedOptions = applySkipRules.getAllSelectedResponses($('body'));
                expect(selectedOptions.length).toEqual(2);
            });
        });
    });
});
