var gridService = angular.module('gridService', []);

gridService.factory('QuestionService', function ($http) {
    return {
        all: function () {
            return $http.get('/api/v1/questions/');
        },
        filter: function (filterObj) {
            var queryParams = transformRequestHelper(filterObj);
            return $http.get('/api/v1/questions/?' + queryParams)
        },
        options: function (question) {
            return $http.get('/api/v1/question/' + question.pk + '/options/')
        }
    };
});

gridService.factory('ThemeService', function ($http) {
    return {
        all: function () {
            return $http.get('/api/v1/themes/');
        }
    };
});

gridService.factory('GridService', function ($http) {
    return {
        create: function (subSectionId, payload) {
            var url = '/subsection/' + subSectionId + '/grid/new/';
            return $http({
                method: 'POST',
                url: url,
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                transformRequest: transformRequestHelper,
                data: payload
            });
        },
        fetch: function (gridId) {
        var gridUrl = '/api/v1/grids/' + gridId + '/';
            return $http.get(gridUrl)
        },
        update: function (gridId, payload) {
            var gridUrl = '/api/v1/grids/' + gridId + '/';
            return $http({
                method: 'POST',
                url: gridUrl,
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                transformRequest: transformRequestHelper,
                data: payload
            });
        }
    };
});


gridService.factory('AnswerInput', function (QuestionService, $q) {

    var answerInput = function (question) {
        var createSelectOptionsFrom = function (questionOptions) {
            var initialValue = '<select><option>Choose One</option>',
                closingTag = '</select>';
            return questionOptions.reduce(function (prev, curr) {
                    return prev + '<option>' + curr.fields.text + '</option>'
                }, initialValue)
                + closingTag;
        };

        var generateSelect = function (question) {
            return QuestionService.options(question).then(function (response) {
                return createSelectOptionsFrom(response.data);
            });
        };

        var textInput = function (question) {
            var aklass = isDate(question) ? "datetimepicker" : "";

            var deferred = $q.defer();
            deferred.resolve('<input type="text" class="' + aklass + '"/>');
            return deferred.promise
        };

        var answerInputMap = {
            number: textInput,
            text: textInput,
            date: textInput,
            multichoice: generateSelect,
            multipleresponse: generateSelect
        };
        var answerInputFor = answerInputMap[question.fields.answer_type.toLowerCase()];
        return answerInputFor(question);
    };

    function isDate(question) {
        return (question.fields.answer_type.toLowerCase() == 'date')
    }

    var renderDirective = function (newVal, elem) {
        newVal && newVal.fields && answerInput(newVal).then(function (inputField) {
            elem.replaceWith(inputField);
            isDate(newVal) && $('.datetimepicker').datepicker({
                pickTime: false,
                autoclose: false
            });
        });
    };

    return {render: renderDirective};
});