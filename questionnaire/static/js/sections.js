$(function(){
    $('#new-section-modal-form').validate({
        rules: { 'name': 'required', 'title': 'required'}
    });

    $('.edit_section').find('form').each(function() {
        $(this).validate({rules: { 'name': 'required', 'title': 'required'}});
    });

    $('.edit_subsection').on('show.bs.modal', function(){
        var id = $(this).attr('object-id'),
            url = "/subsection/" + id +"/edit/";
        loadAjaxEditModal(id, url, "subsection");
    });

    $('.edit_section').on('show.bs.modal', function(){
        var section_id = $(this).attr('object-id'),
            url = "/section/" + section_id +"/edit/";
        loadAjaxEditModal(section_id, url, "section");
    });
});

function loadAjaxEditModal(objectId, url, objectToEdit){
        $.get(url, function(data) {
            var $holder = $('<div></div>').append(String(data));
            var content =  $holder.find("#form-content").html();
            $( "#edit_"+ objectToEdit +"_"+objectId+"_ajax_content").html(content);

            $('textarea').autosize();
            var btnsGrps = jQuery.trumbowyg.btnsGrps;

            $("#edit_"+ objectToEdit +"_"+objectId+"_ajax_content textarea").trumbowyg({
                lang: 'en',
                semantic: true,
                resetCss: true,
                autoAjustHeight: true,
                fullscreenable: false,
                autogrow: true,
                btns: [
                   'formatting',
                   '|', btnsGrps.design,
                   '|', 'link',
                   '|', btnsGrps.justify,
                   '|', 'insertHorizontalRule']
            });

        });
}

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
            $('#modal-subsection-id').append('<option value=' + order + ' selected>' + order + ' (Current) ' + '</option>');
        } else {
            $('#modal-subsection-id').append('<option value=' + order + '>' + order + '</option>');
        }
    });

};