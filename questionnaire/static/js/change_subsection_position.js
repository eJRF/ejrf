var subsectionPositions = subsectionPositions || {};


subsectionPositions.getSubSections = function (selectedSubsectionOrder) {
    var subSections = $('div .subsection-content');
    $('#modal-subsection-id').html("");
    subSections.map(function (_, element) {
            var name = $(element).attr('data-attribute-subsection-name'),
            order = $(element).attr('data-attribute-subsection-order'),
            id = $(element).attr('data-attribute-subsection-id');
        if (selectedSubsectionOrder == order) {
            $('#subsection').val(id);
            $('#move_modal_label').text('Change Position of subsection: ' + name.replace('None', 'Un-titled subsection ' + order));
            $('#modal-subsection-id').append('<option value=' + order + '>' + order + ' (Current) ' + '</option>');
        } else {
            $('#modal-subsection-id').append('<option value=' + order + '>' + order + '</option>');
        }
    });

};