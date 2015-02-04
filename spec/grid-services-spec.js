describe("Grid Services", function () {

    beforeEach(function () {
            module('gridService');
        }
    );

    describe("AnswerInput", function () {
        var answerInput, question, rendered, scope, httpMock,
            element,
            initElement,
            ngElement,
            html = "<primary-question-input/>",
            options=[{fields:{text: 'option1'}}, {fields:{text: 'option2'}}];

        beforeEach(function () {

            inject(function ($httpBackend, $compile, $rootScope, AnswerInput) {
                answerInput = AnswerInput;
                scope = $rootScope;
                initElement = function (aHtml) {
                    ngElement = angular.element(aHtml);
                    element = $compile(ngElement)(scope);
                    scope.$digest();
                };
                initElement(html);
                httpMock = $httpBackend;
            });
        });

        it('should render number question', function () {
            question = {fields: {answer_type: 'number'}};
            spyOn(element, 'replaceWith').andCallThrough();
            answerInput.render(question, element);
            scope.$digest();
            rendered = '<input type="text" class=""/>';
            expect(element.replaceWith).toHaveBeenCalledWith(rendered);
        });

        it('should render text question', function () {
            question = {fields: {answer_type: 'text'}};
            spyOn(element, 'replaceWith').andCallThrough();
            answerInput.render(question, element);
            scope.$digest();
            rendered = '<input type="text" class=""/>';
            expect(element.replaceWith).toHaveBeenCalledWith(rendered);
        });


        it('should render date question', function () {
            question = {fields: {answer_type: 'date'}};
            spyOn(element, 'replaceWith').andCallThrough();
            spyOn($.fn, 'datepicker').andCallThrough();
            answerInput.render(question, element);
            scope.$digest();
            rendered = '<input type="text" class="datetimepicker"/>';
            expect(element.replaceWith).toHaveBeenCalledWith(rendered);
            expect($.fn.datepicker).toHaveBeenCalledWith({pickTime: false, autoclose: false});
        });


        it('should render multichoice question', function () {
            question = {fields: {answer_type: 'multichoice'}, pk:1};
            spyOn(element, 'replaceWith').andCallThrough();
            httpMock.expectGET('/api/v1/question/1/options/').respond(options);
            answerInput.render(question, element);
            scope.$digest();
            httpMock.flush();
            rendered = '<select><option>Choose One</option><option>option1</option><option>option2</option></select>';
            expect(element.replaceWith).toHaveBeenCalledWith(rendered);
        });

        it('should render multipleresponse question', function () {
            question = {fields: {answer_type: 'multipleresponse'}, pk:1};
            spyOn(element, 'replaceWith').andCallThrough();
            httpMock.expectGET('/api/v1/question/1/options/').respond(options);
            answerInput.render(question, element);
            scope.$digest();
            httpMock.flush();
            rendered = '<select><option>Choose One</option><option>option1</option><option>option2</option></select>';
            expect(element.replaceWith).toHaveBeenCalledWith(rendered);
        });

    });

});
