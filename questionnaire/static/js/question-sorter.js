$(function () {
    $.extend($.tablesorter.themes.bootstrap, {
        table: 'table table-bordered table-striped',
        caption: 'caption',
        header: 'bootstrap-header',
        sortNone: 'glyphicon glyphicon-sort-by-alphabet',
        sortAsc: 'glyphicon glyphicon-chevron-up',
        sortDesc: 'glyphicon glyphicon-chevron-down'
    });

    $("#tbl-question-list").tablesorter({
        headers: {
            0: {sorter: 'UID'},
            1: {sorter: 'Export Label (Detail)'},
            2: {sorter: 'Theme'},
            3: {sorter: 'Response Type'},
            4: {sorter: false}
        },
        theme: "bootstrap",
        widthFixed: true,
        headerTemplate: '{content} {icon}',
        widgets: [ "uitheme", "zebra" ],
        widgetOptions: {
            zebra: ["even", "odd"],
            filter_reset: ".reset"
        }
    })
});