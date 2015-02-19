describe("Drag and Drop directives", function () {
    var element, scope,
        initElement,
        ngElement,
        tableBody;

    beforeEach(function () {
        module('editGridModule');
        spyOn($.fn, 'sortable').andCallThrough();

        inject(function ($httpBackend, $compile, $rootScope) {
            scope = $rootScope.$new();
            initElement = function (aHtml) {
                ngElement = angular.element(aHtml);
                element = $compile(ngElement)(scope);
                scope.$apply();
            };
        });
    });

    describe("dndTable", function () {
        it('should initialize table dnd on non-hybrid grid table', function () {
            tableBody = '<table dnd-table><tbody>'
                + '<tr class="tr-sortable"></tr>'
                + '<tr class="tr-sortable"></tr>'
                + '</tbody></table>';

            initElement(tableBody);
            expect($.fn.sortable).toHaveBeenCalled();
        });
    });

    describe("hybridDndTable", function () {
        it('should initialize table dnd on hybrid grid table', function () {
            tableBody = '<table hybrid-dnd-table>'
                +'<tbody>'
                + '<tr></tr>'
                + '<tr></tr>'
                + '</tbody></table>';

            initElement(tableBody);
            expect($.fn.sortable).toHaveBeenCalled();
        });
    });
});