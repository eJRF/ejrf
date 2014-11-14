var subsectionPositions = subsectionPositions || {};


subsectionPositions.getSubSections = function () {
    var subSections = $('div .subsection-content');

    subSections.map(function (_, element) {
            name = $(element).attr('data-attribute-subsection-name');
            order = $(element).attr('data-attribute-subsection-order');

            $('#modal-subsection-id').append('<option value=order>' + order + ': ' + name + '</option>');
        });

};