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
                    $error_clone.insertAfter($(this).next().next());
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
        removeSelectedOptions(newElement, $columns)
        $select.after(newElement);
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
            $parent = $el.parents('.create-grid-form'),
            $primary_question = $parent.find('#id_primary_question'),
            all_primary_questions = $('#all-primary-template').html(),
            $all_primary_questions = $(all_primary_questions);
        if ($el.val()!='allow_multiples'){
            $all_primary_questions.find('option[multichoice!="true"]').each(function(){
                $(this).remove();
            });
        }
        $primary_question.html($all_primary_questions.html());
    });


});

function removeSelectedOptions(newElement, $columns) {
    var  used_options = $columns.find('option:selected[value!=""]');
    used_options.each(function(){
        var val = $(this).val();
        newElement.find('option[value=' + val + ']').remove()
    });
}
