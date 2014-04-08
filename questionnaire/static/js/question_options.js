;
jQuery(function($){
    var $form = $("#id-new-question-form"),
        template = $("#question-option-template").html(),
        answerTypeSelect = $('#id_answer_type');

    function addQuestionOption($element){
        $element.before(template);
        assignOptionNumbers($form)
    }

    answerTypeSelect.on('change', function(){
        if($(this).val() == 'MultiChoice'){
            $('#option-choices').addClass('show').removeClass('hide')
        }else{
            $('#option-choices').removeClass('show').addClass('hide')
            removeOptions();
        }
    });

    $('input[type=radio]').on('change', function(){
        if($(this).val() == 'custom'){
            addQuestionOption($("div.form-actions"));
            $form.find('input[name=options]').prop('checked', false)
        }else{
            $form.find('input[name=options-custom]').prop('checked', false)
            removeOptions()
        }
    });

    $form.on("click", ".add-option", function(){
        addQuestionOption($("div.form-actions"));
    });

    $form.on("click", ".remove-option", function(){
        $(this).parents("div#option-input-group").remove();
        assignOptionNumbers($form)
    });
});

function assignOptionNumbers($form){
        $form.find("span.number").each(function(i, element){
            $(element).text(++i);
        });
    }

function removeOptions(){
        $("div.input-group").each(function(){
           $(this).remove();
        });
    }
