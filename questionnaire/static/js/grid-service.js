
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


gridService.factory('hybridGridService', function () {
    var hybridGrid = [
        [
            {}
        ]
    ];

    var addElement = function (rowIndex) {
        hybridGrid[rowIndex].push({});
    };

    var addRow = function (rowIndex) {
        hybridGrid[rowIndex] = [];
        addElement(rowIndex, 0);
    };

    var rows = function () {
        return hybridGrid
    };

    var columns = function (rowIndex) {
        return hybridGrid[rowIndex];
    };

    var removeElement = function (rowIndex, columnIndex) {
        hybridGrid[rowIndex].splice(columnIndex, 1);
    };

    return {
        rows: rows,
        columns: columns,
        addElement: addElement,
        addRow: addRow,
        removeElement: removeElement
    }
});
