var validateDynamicForms = function (dynamicForm) {
    var formKeys = Object.keys(dynamicForm);
    var invalidFormsKeys = formKeys.filter(function (key) {
        return dynamicForm[key] && (!dynamicForm[key].$valid || (dynamicForm[key].columns && !dynamicForm[key].columns.$viewValue.pk))
    });

    invalidFormsKeys.forEach(function (key) {
        if (dynamicForm[key].columns) {
            dynamicForm[key].columns.$error.required = true
        }
    });

    return invalidFormsKeys.length == 0;
};

var transformRequestHelper = function (obj) {
    var str = [];
    for (var key in obj) {
        var value = obj[key];
        if (Array.isArray(value)) {
            value.forEach(function (column) {
                str.push(encodeURIComponent(key) + "=" + encodeURIComponent(column));
            })
        } else {
            str.push(encodeURIComponent(key) + "=" + encodeURIComponent(value));
        }
    }
    return str.join("&");
};

var questionFilterCriteria = function (obj, criteria) {
    var criteriaKeys = Object.keys(criteria);
    var matched = criteriaKeys.filter(function (key) {
        return obj[key] != criteria[key];
    });
    return matched.length == 0;
};

var questionFilter = function (questions, filterCriteria) {
    return questions.filter(function (question) {
        return questionFilterCriteria(question.fields, filterCriteria);
    });
};

function reArrange(elem) {
    var tableRow = $(elem).find('tbody tr');
    return $.map(tableRow, function (row) {
        return $(row).data('option');
    });
}

function reorderedQuestionRows(elem) {
    var tableRow = $(elem).find('tbody tr');
    return $.map(tableRow, function (row) {
        return $(row).find('td.drag');
    }).map(function (td) {
        return $(td).data('option');
    }).filter(function (row) {
        return row;
    });
}
