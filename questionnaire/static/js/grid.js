;

jQuery(function($){
    $('.create-grid').on('show.bs.modal', function(){
        var subsection_id = $(this).attr('subsection-id'),
            create_grid_url = "/subsection/" + subsection_id +"/grid/new/";
        $.get(create_grid_url, function( data ) {
            var $holder = $('<div></div>').append(String(data));
            var content =  $holder.find("#create-grid-form-content").html()
            $( "#create-grid-ajax-content-"+subsection_id ).html(content);

        });
    });

    $.validator.addMethod("column_required", function(value, element) {
        var ret = true;
        $("select[name='columns']:has(option[value='']:selected)").each(function(){
            ret = false;
        });
        return ret;
    }, "This field is required.");

    $('.create-grid-form').validate({
        rules: {
            'type': 'required',
            'primary_question': 'required',
            'columns': {required:true, "column_required": true}
        },
        errorPlacement: function(error, element) {
            if (element.attr("name") == "columns") {
                $("select[name='columns']:has(option[value='']:selected)").each(function(){
                    var $error_clone = error.clone(true);
                    $error_clone.insertAfter($(this).siblings(':last'));
                });
            } else {
              error.insertAfter(element);
            }
        }
    });

    $('body').on('click', '.add-column', function(){
        var $el = $(this),
            $select = $el.parents('.input-group'),
            newElement = $select.clone(true),
            $form = $el.parents('form'),
            $columns = $form.find('#columns');
        $select.after(newElement);
        removeSelectedOptions(newElement, $columns);
        assignOptionNumbers($form);
        newElement.rules('add', {required: true});
    });

    $('body').on('click','.remove-column', function(){
        var $el = $(this),
            $select = $el.parents('.input-group'),
            $form = $el.parents('form'),
            $columns = $form.find('#columns');
        if ($columns.find('p').length>1){
            $select.remove();
            assignOptionNumbers($form);
        }
    });

    $('body').on('change', '#id_type', function(){
        var $el = $(this),
            $parent_form = $el.parents('.create-grid-form'),
            $primary_question = $parent_form.find('#id_primary_question'),
            all_primary_questions = $('#all-primary-template').html(),
            $all_primary_questions = $(all_primary_questions),
            $first_columns = $parent_form.find('#columns');
        if ($el.val() === 'display_all'){
            removeNonMultiChoiceOptions($all_primary_questions);
            addTemplate('#addmore-displayall-template', $first_columns);
        }
        else if ($el.val() ==='hybrid'){
            addTemplate('#hybrid-template', $first_columns);
        }
        else if ($el.val() ==='allow_multiples'){
            addTemplate('#addmore-displayall-template', $first_columns);
        }
        else{
            $first_columns.html('');
        }
        $primary_question.html($all_primary_questions.html());

    });

   $('body').on('change', '#id_primary_question', function(){
        var $el = $(this),
            theme_id = $el.find('option:selected').attr('theme'),
            $parent_form = $el.parents('.create-grid-form'),
            $columns = $parent_form.find('#columns');
        removeQuestionsWithOtherThemes($columns, theme_id);
    });

    $('body').on('change', '.mid-row-add-hybrid-grid select[name=columns]', function(){
        var $el = $(this);
        $el.next('input[type=hidden][name=subgroup]').val($el.val());
    });

    $('.delete-grid').hover(function(){
       $(this).parents('.grid-group').addClass('show-border');
    }, function(){
        $(this).parents('.grid-group').removeClass('show-border');
    });


});

function removeQuestionsWithOtherThemes($columns, theme_id) {
    $columns.find('option[theme!="'+ theme_id +'"]').each(function(){
        $(this).remove();
    });
}

function removeSelectedOptions(newElement, $columns) {
    var  used_options = $columns.find('option:selected');
    used_options.each(function(){
        var val = $(this).val();
        newElement.find('option[value=' + val + ']').remove();
    });
}

function removeNonMultiChoiceOptions($all_primary_questions){
    $all_primary_questions.find('option[multichoice!="true"]').each(function(){
        $(this).remove();
    });
}
function addTemplate(template_selector, $first_columns) {
    var template = $(template_selector).html();
    $first_columns.html(template);
}