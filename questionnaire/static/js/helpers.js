var validateDynamicForms = function (dynamicForm) {
    var formKeys = Object.keys(dynamicForm);
    return formKeys.filter(function (key) {
        return dynamicForm[key] && !dynamicForm[key].$valid
    }).length == 0;
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
