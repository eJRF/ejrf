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
    var service = function (grid) {

        var hybridGrid = grid;

        var addElement = function (rowIndex, columnIndex) {
            hybridGrid[rowIndex].splice(columnIndex, 0, {});
        };

        var addRow = function (rowIndex) {
            hybridGrid.splice(rowIndex, 0, [{}]);
            return rowIndex;
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
        };
    };

    return {
        get: function (hybridGrid) {
            return new service(hybridGrid);
        }
    }
});
