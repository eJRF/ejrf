var gridTypeFactories = angular.module('gridTypeFactories', []);

gridTypeFactories.factory('NonHybridPayload', function () {
    var generatePayload = function (selectedQuestions, type) {
        var columnsIds = selectedQuestions.otherColumns.map(function (question) {
            return question.pk;
        });
        return {
            'type': type,
            'primary_question': selectedQuestions.primary.pk,
            'columns': columnsIds,
            'csrfmiddlewaretoken': window.csrfToken
        };
    };
    return {payload: generatePayload};
});

gridTypeFactories.factory('QuestionInitializer', function () {
    var gridQuestionsFrom = function (allQuestions, gridQuestionIds) {
        return allQuestions.filter(function (qn) {
            var qnIndex = gridQuestionIds.indexOf(qn.pk);
            return qnIndex != -1;
        })
    };

    var primaryQuestionIn = function (gridQuestions, questionIds) {
        return gridQuestions.filter(function (qn) {
            var qnIndex = questionIds.indexOf(qn.pk);
            return qnIndex != -1 && qn.fields.is_primary;
        })[0]
    };

    var init = function (grid, allQuestions) {
        var gridQuestionIds = grid.fields && grid.fields.question || [];
        var gridQuestions = gridQuestionsFrom(allQuestions, gridQuestionIds);

        var primary = primaryQuestionIn(gridQuestions, gridQuestionIds);
        var otherColumns = gridQuestions.filter(function (qn) {
            var qnIndex = gridQuestionIds.indexOf(qn.pk);
            return qnIndex != -1 && !qn.fields.is_primary;
        });
        return {
            primary: primary || {},
            otherColumns: otherColumns.length && otherColumns || [{}],
            questions: gridQuestions.length && gridQuestions || []
        }
    };
    return {
        init: init
    }
});

gridTypeFactories.factory('NonHybridQuestionSelection', function (QuestionInitializer) {
    var addColumn = function (index) {
        this.otherColumns.splice(index, 0, {});
    };

    var removeColumn = function (index) {
        this.otherColumns.splice(index, 1);
    };
    var moveRight = function (index) {
        var otherColumns = this.otherColumns;
        if (!(index == otherColumns.length - 1)) {
            this.otherColumns.splice(index, 2, otherColumns[index + 1], otherColumns[index]);
        }
    };
    var moveLeft = function (index) {
        var otherColumns = this.otherColumns;
        if (index > 0) {
            var toIndex = index - 1;
            this.otherColumns.splice(toIndex, 2, otherColumns[index], otherColumns[toIndex]);
        }
    };

    return function (grid, allQuestions) {
        var theGrid = grid || {};
        var questions = allQuestions || [];
        var initial = QuestionInitializer.init(theGrid, questions);

        return {
            addColumn: addColumn,
            removeColumn: removeColumn,
            moveLeft: moveLeft,
            moveRight: moveRight,
            primary: initial.primary,
            otherColumns: initial.otherColumns,
            questions: initial.questions
        };
    };
});

gridTypeFactories.factory('AddMoreGridFactory', function (NonHybridPayload, NonHybridQuestionSelection) {
    var addMoreGrid = function (grid, allQuestions) {
        var thePayload = function () {
            return NonHybridPayload.payload(this.initialSelectedQuestions, this.value);
        };
        return {
            value: 'allow_multiples',
            text: 'Add More',
            addMore: true,
            hybrid: false,
            primary_questions_criteria: {is_primary: true},
            payload: thePayload,
            initialSelectedQuestions: new NonHybridQuestionSelection(grid, allQuestions)
        }
    };
    return {
        create: function (grid, allQuestions) {
            return new addMoreGrid(grid, allQuestions);
        }
    }
});

gridTypeFactories.factory('DisplayAllGridFactory', function (NonHybridPayload, NonHybridQuestionSelection) {
    var DisplayAllGrid = function (grid, allQuestions) {
        var thePayload = function () {
            return NonHybridPayload.payload(this.initialSelectedQuestions, this.value);
        };

        return {
            value: 'display_all',
            text: 'Display All',
            displayAll: true,
            hybrid: false,
            primary_questions_criteria: {
                is_primary: true,
                answer_type: 'MultiChoice'
            },
            payload: thePayload,
            initialSelectedQuestions: new NonHybridQuestionSelection(grid, allQuestions)
        }
    };
    return {
        create: function (grid, allQuestions) {
            return new DisplayAllGrid(grid, allQuestions);
        }
    };
});

gridTypeFactories.factory('HybridGridFactory', function (hybridGridQuestionSelection) {
    function generatePayload() {
        var self = this;
        var hybridNonPrimaryQuestionMatrix = this.initialSelectedQuestions.dynamicGridQuestion;

        function getIds(wrappedQuestion) {
            return wrappedQuestion.question.pk;
        }

        var columns = hybridNonPrimaryQuestionMatrix.reduce(function (prev, curr) {
            return prev.concat(curr);
        }, []).map(getIds);

        var subgroup = hybridNonPrimaryQuestionMatrix.filter(function (column) {
            return column.length > 1;
        })[0];

        var subGroupQuestions = subgroup && subgroup.map(getIds);

        return {
            'csrfmiddlewaretoken': window.csrfToken,
            'type': self.value,
            'primary_question': this.initialSelectedQuestions.primary.pk,
            'columns': columns,
            'subgroup': subGroupQuestions || []
        }
    }

    var HybridGrid = function (grid, allQuestions, orders) {
        return {
            value: 'hybrid',
            text: 'Hybrid',
            hybrid: true,
            addMore: true,
            primary_questions_criteria: {is_primary: true},
            payload: generatePayload,
            initialSelectedQuestions: new hybridGridQuestionSelection(grid, allQuestions, orders)
        }
    };

    return {
        create: function (grid, allQuestions, orders) {
            return new HybridGrid(grid, allQuestions, orders);
        }
    };
});

gridTypeFactories.factory('hybridGridQuestionInitializer', function () {
    var gridQuestionsFrom = function (gridQuestionIds, allQuestions) {
        return allQuestions.filter(function (qn) {
            var qnIndex = gridQuestionIds.indexOf(qn.pk);
            return qnIndex != -1;
        })
    };

    var primaryQuestionIn = function (gridQuestions, questionIds) {
        return gridQuestions.filter(function (qn) {
            var qnIndex = questionIds.indexOf(qn.pk);
            return qnIndex != -1 && qn.fields.is_primary;
        })[0]
    };

    var init = function (grid, allQuestions, orders) {
        var dynamicColumns = [[{}]],
            hasAddedSubgroup = false,
            primary = {},
            gridQuestions = [];

        if (grid && grid.fields) {
            var gridQuestionIds = grid.fields.question || [],
                childGrid = grid.children.length && grid.children[0],
                parentGridQuestions = gridQuestionsFrom(gridQuestionIds, allQuestions),
                childGridQuestions = childGrid && gridQuestionsFrom(childGrid.fields.question, allQuestions) || [];

            dynamicColumns = [];
            gridQuestions = parentGridQuestions.concat(childGridQuestions);
            primary = primaryQuestionIn(parentGridQuestions, gridQuestionIds);
            var nonPrimaryQuestionOrders = orders.filter(function (order) {
                return order.fields.question != primary.pk
            });

            nonPrimaryQuestionOrders.forEach(function (order) {
                var gridQuestionIndex = gridQuestionIds.indexOf(order.fields.question);
                if (gridQuestionIndex != -1) {
                    var singleQuestionRow = parentGridQuestions.filter(function (question) {
                        return question.pk == order.fields.question;
                    });
                    dynamicColumns.push([{'question': singleQuestionRow[0]}]);
                } else if (!hasAddedSubgroup) {
                    hasAddedSubgroup = true;
                    dynamicColumns.push(childGridQuestions.map(function (question) {
                        return {'question': question};
                    }));
                }
            });
        }
        return {
            primary: primary,
            dynamicGridQuestion: dynamicColumns,
            questions: gridQuestions.length && gridQuestions || []
        }
    };

    return {
        init: init
    }
});

gridTypeFactories.factory('hybridGridQuestionSelection', function (hybridGridQuestionInitializer) {
    var maxColumns = function () {
        var questions = this.dynamicGridQuestion;
        var rowLengths = questions.map(function (questionRows) {
            return questionRows.length;
        });
        return Math.max.apply(Math, rowLengths);
    };

    var allowAddColumn = function (rowIndex) {
        var questions = this.dynamicGridQuestion;
        var rowWithColumns = questions.filter(function (questionRows) {
            return questionRows.length > 1;
        });
        return (rowWithColumns.length == 0) || (questions.indexOf(rowWithColumns[0]) == rowIndex);
    };

    var addElement = function (rowIndex, columnIndex) {
        this.dynamicGridQuestion[rowIndex].splice(columnIndex, 0, {});
    };

    var addRow = function (rowIndex) {
        this.dynamicGridQuestion.splice(rowIndex, 0, [
            {}
        ]);
    };

    var removeElement = function (rowIndex, columnIndex) {
        var dynamicGridQuestion = this.dynamicGridQuestion[rowIndex];
        dynamicGridQuestion.splice(columnIndex, 1);
        if (!dynamicGridQuestion.length) {
            this.dynamicGridQuestion.splice(rowIndex, 1);
        }
    };

    return function (grid, allQuestions, orders) {
        var theGrid = grid || {};
        var questions = allQuestions || [];
        var theOrders = orders || [];
        var initial = hybridGridQuestionInitializer.init(theGrid, questions, theOrders);

        return {
            primary: initial.primary,
            dynamicGridQuestion: initial.dynamicGridQuestion,
            questions: initial.questions,
            addElement: addElement,
            addRow: addRow,
            allowAddColumn: allowAddColumn,
            removeElement: removeElement,
            maxColumns: maxColumns
        };
    }
});