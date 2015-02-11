describe("create display all grid", function () {
    var scope, httpMock,
        subsectionId = 3,
        gridId = 1,
        questionnaireId = 1,
        primary = {
            pk: 188,
            fields: {
                text: "PAB (protection at birth)",
                theme: 6,
                answer_type: "MultiChoice",
                is_primary: true
            }
        },
        options = [{
            pk: 1,
            fields: {
                text: 'Yes'
            }
        }, {
            pk: 2,
            fields: {
                text: 'No'
            }
        }],
        question1 =
        {
            pk: 186,
            fields: {
                text: "PAB (protection at birth)",
                theme: 6,
                answer_type: "MultiChoice",
                is_primary: false
            }
        },
        question2 =
        {
            pk: 187,
            fields: {
                text: "Another Question",
                theme: 6,
                answer_type: "MultiChoice",
                is_primary: false
            }
        },
        grid = [{
            pk: 12,
            fields: {
                theme: 6,
                question: [186, 187, 188],
                allow_multiples: true
            }
        }],
        stubQuestions = [question1, question2];

    beforeEach(function () {
            module('editGridModule');
            module('gridService');
            module('gridTypeFactories');
        }
    );

    describe("EditGridController", function () {
        var initController,
            themeStub = 6;

        beforeEach(function () {
            inject(function ($controller, $rootScope, $httpBackend) {
                scope = $rootScope.$new();
                httpMock = $httpBackend;

                initController = function () {
                    $controller('editGridController', {$scope: scope});
                };
            });
        });


        it('should grid data as initial', function () {
            var expectedQuestion = [primary, question1, question2];
            initController();

            httpMock.expectGET('/api/v1/grids/' + gridId + '/').respond(grid);
            httpMock.expectGET('/api/v1/questions/').respond(expectedQuestion);
            httpMock.expectGET('/api/v1/question/' + primary.pk + '/options/').respond(options);

            scope.updateScope(questionnaireId, subsectionId, gridId);
            scope.$apply();
            httpMock.flush();

            expect(scope.grid.selectedTheme).toEqual(themeStub);
            expect(scope.selectedQuestions.primary).toEqual(primary);
            expect(scope.selectedQuestions.otherColumns).toEqual([question1, question2]);
            expect(scope.grid.questionOptions).toEqual(options);
        });
        it('should update grid details', function () {
            var expectedGrid = {
                value: 'display_all',
                text: 'Display All',
                displayAll: true,
                initialSelectedQuestions: {
                    primary: primary,
                    otherColumns: stubQuestions
                },
                payload: function () {
                    return {
                        pk: gridId,
                        primary: 188,
                        columns: [186, 187],
                        type: 'hybrid'
                    }
                }
            };

            initController();
            scope.grid = {gridType: expectedGrid};
            scope.gridId = gridId;
            scope.subsectionId = subsectionId;

            var successMessage = {message: 'Grid has been updated successfully!'};
            httpMock.expectPOST('/api/v1/grids/' + gridId + '/').respond([successMessage]);

            scope.postUpdateGrid();
            httpMock.flush();
            expect(scope.message).toEqual(successMessage.message);
        });
    })
});