;

jQuery(function($){
    var $form = $('#create_grid_form');
    $('.add-column').on('click', function(){
        var $el = $(this),
            $select = $el.parents('.input-group'),
            newElement = $select.clone(true),
            $columns = $form.find('columns');
        removeSelectedOptions(newElement, $columns)
        $select.after(newElement);
        assignOptionNumbers($form);
    });
    $('.remove-column').on('click', function(){
        var $el = $(this),
            $select = $el.parents('.input-group');
        $select.remove();
        assignOptionNumbers($form);
    });


});

function removeSelectedOptions(newElement, $columns) {
    var  used_options = $columns.find('option:selected');
    used_options.each(function(){
        var val = $(this).val();
        newElement.find('option[value=' + val + ']').remove()
    });
}
