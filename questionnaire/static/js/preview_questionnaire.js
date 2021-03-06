$(function(){
    $('.toggle-versions').on('click', function(event){
        var SHOW_ICON_AND_TEXT = "<span class=\"glyphicon glyphicon-circle-arrow-down\"></span> Show Versions";
        var HIDE_ICON_AND_TEXT = "<span class=\"glyphicon glyphicon-circle-arrow-up\"></span> Hide Versions";
        var countryClass = $(this).attr('data-version');
        $("." + countryClass + '.hide').toggleClass('show');
        $(this).html($(this).html() === HIDE_ICON_AND_TEXT ? SHOW_ICON_AND_TEXT : HIDE_ICON_AND_TEXT);
        event.preventDefault()
    });

    $('.preview-btn-url').on('click', function(){
        var url = $(this).attr('data-href'),
            modalId = $('#preview_modal');
        showLoadingMessage();
        modalId.modal('show');
        modalId.removeData('bs.modal');
        if (form_has_changed){
            $.post( location.pathname, $( "#questionnaire_entry" ).serialize(), function(data1){
                fillModalWithAjaxContent(url);
            });
        }else{
            fillModalWithAjaxContent(url);
        }
    });

    $('.ds-preview-btn').on('click', function(){
        var url = $(this).attr('data-href'),
            modalId = $('#preview_modal');
                showLoadingMessage();
        modalId.modal('show');
        modalId.removeData('bs.modal');
        fillModalWithAjaxContent(url);
        removeButtons(modalId, ['#cancel_button','.alert', '#submit_button']);
    });

    disable_modal_input_fields(editable);

    $('.preview-section-modal-tab-link').on('click', function(){
        var $el = $(this),
            url = $el.attr('data-href'),
            $li = $el.parents('li'),
            $ul = $el.parents('ul'),
            version = $('body').find('#version-holder').val();
        showLoadingMessage();
        $ul.find('.active').removeClass('active');
        $li.addClass('active');
        if(typeof version != 'undefined'){
            url += "&version=" + version
        }
        fillModalWithAjaxContent(url);
        enableFields();
    });

    $('#edit_questionnaire_link').on('click', function(){
        disableInputFields();
    });

    $('.assign-question').on('show.bs.modal', function(){
        var subsection_id = $(this).attr('subsection-id'),
            assign_to_subsection_url = "/subsection/" + subsection_id +"/assign_questions/";
        $.get(assign_to_subsection_url, function( data ) {
            var $holder = $('<div></div>').append(String(data));
            var content =  $holder.find("#question-list").html()
            $( "#assign-question-ajax-content-"+subsection_id ).html(content);
        });
    });
});

function enableFields() {
    var $body = $('body');
    $body.find('#id_path').prop('disabled', false);
    $body.find('#cancel_button').prop('disabled', false);
    $body.find('#upload-btn').prop('disabled', false);
}


function showLoadingMessage(){
    $("#ajax-section-content").html("<img src=\"/static/img/spinner.gif\"> Loading, please wait...");
}

function fillModalWithAjaxContent(questionnaire_preview_url){
    $.get(questionnaire_preview_url, function( data ) {
        var $holder = $('<div></div>').append(String(data));
        var section_title =  $holder.find("#section-title").html();
        var section_content =  $holder.find("#section-content").html();
        var content = section_title + section_content;
        $("#ajax-section-content").html(content);
        disable_modal_input_fields(!editable);
        enableFields();
    });
    form_has_changed = false;
}

function disable_modal_input_fields(editable){
    $('.tab-content :input').each(function() {
       $(this).prop('disabled', editable);
    });
}

function disableInputFields(status) {
    $('.form-content :input').each(function () {
        $(this).prop('disabled', status);
    });
    $('.add-more').prop('disabled', status);
}