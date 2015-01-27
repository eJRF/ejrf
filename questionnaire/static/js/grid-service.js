
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
