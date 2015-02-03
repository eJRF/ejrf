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
        }
    };
});


gridService.factory('AnswerInput', function (QuestionService, $q) {

    var answerInput = function (question) {
        var generateSelect = function (question) {

            return QuestionService.options(question).then(function (response) {
                var questionOptions = response.data,
                    initialValue = '<select><option>Choose One</option>',
                    closingTag = '</select>';

                return questionOptions.reduce(function (prev, curr) {
                        return prev + '<option>' + curr.fields.text + '</option>'
                    }, initialValue)
                    + closingTag;
            });
        };

        var textInput = function (klass) {
            var aklass = klass || '';
            var deferred = $q.defer();
            deferred.resolve('<input type="text" class="' + aklass + '"/>');
            return deferred.promise
        };

        var answerInputMap = {
            number: textInput(),
            text: textInput(),
            date: textInput("datetimepicker"),
            multichoice: generateSelect(question),
            multipleresponse: generateSelect(question)
        };
        return answerInputMap[question.fields.answer_type.toLowerCase()]
    };

    var renderDirective = function (newVal, elem) {
                newVal && newVal.fields && answerInput(newVal).then(function (inputField) {
                    elem.replaceWith(inputField);
                    (newVal.fields.answer_type.toLowerCase() == 'date') && $('.datetimepicker').datepicker({
                        pickTime: false,
                        autoclose: false
                    });
                });
        };

    return {render: renderDirective};

});