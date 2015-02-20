var form_has_changed = false;
var editable = false;

$(document).ready(function () {
    $('.pagination').children('ul').addClass('pagination');
    $('a[data-toggle=popover]').popover();
    $('a[data-toggle=tooltip]').tooltip();
    groupRolesBootstrap();
    $('p:empty').remove();

    $('.datetimepicker').datepicker({pickTime: false, autoclose: true});
    $('textarea').autosize();

    $('.grid-error').hover(function () {
        $(this).popover('show');
    }, function () {
        $(this).popover('hide');
    });

    $('#first_row').find('input[type=hidden]').each(function (index, element) {
        $(element).val(0);
    });

    $('select[name^=MultiChoice]').on('change', function () {
        var selectedText = $(this).find('option:selected').text();
        if (selectedText.toLowerCase() === "other") {
            addSpecifyField($(this));
        }
    });

    $('select[name=answer_type]').on('change', function () {
        var selectedAnswerType = $(this).val(),
            isPrimaryField = $('input[name=is_primary]');
        setDisabled(isPrimaryField, selectedAnswerType);
    });
    var btnsGrps = jQuery.trumbowyg.btnsGrps;

    $('.wysiwyg').trumbowyg({
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

    $("input[type=checkbox][name=regions]").on('click', function () {
        var regions = [];
        $("input[type=checkbox][name=regions]:checked").each(function () {
            regions.push($(this).val());
        });

        getCountriesFor(regions, function (data) {
            $('#extract-countries').html('');
            for (var index = 0; index < data.length; index++) {
                $('#extract-countries').append("<li class='countries-extract'>" +
                '<input type="checkbox" name="countries" value="' + data[index].id + '" id="' + data[index].name + '"/>' +
                '<label for="' + data[index].name + '">' + data[index].name + '</label></li>');
            }
        });
    });

    $('.add-row').on('click', function (event) {
        var $el = $(this);
        var $newRow = addRowOn($el, 'tr', 'table');
        applySkipRules.bindAddMoreSkipRulesOn($newRow, showAddMoreRows)
        event.preventDefault();
    });


    $('.reorder-subsection').on('click', function () {
        var $element = $(this),
            $modal = getModalWithSubSectionQuestions($element);
        removeButtons($modal, ['.add-more', '.btn-group', '.unassign-question']);
        highlightOnHover($modal);
        activateSortable($modal);
        disableInputFields(false);
        $modal.modal('show');
        return false;
    });

    $('#export-section').on('click', function (event) {
        $(this).toggleClass('active');
        var filename = "";
        $.ajax({
            type: "GET",
            async: false,
            url: "/export-section",
            success: function (data) {
                var obj = JSON.parse(data);
                filename = obj['filename']
            }
        });

        setTimeout(function () {
            $('#export-section').toggleClass('active');
            return_file(filename)
        }, 8000);
        event.preventDefault();
    });

    $('#id-older-jrf').on('click', function (event) {
        $('.hide').toggleClass('show');
        $(this).html($(this).html() === "More" ? "Less" : "More");
        event.preventDefault()
    });

    $('input[type=radio]').on('click', function () {
        var $el = $(this),
            name = $el.attr('name'),
            $redundant_hidden_radio = $el.parents('.form-group').find('input[name=' + name + '][exclude=true]');
        $redundant_hidden_radio.remove();
    });

    $('.add-more').on('click', function (event) {
        var $el = $(this);
        var $new_row = addRowOn($el, '.hybrid-group-row', '.question-group');
        showSeparator($new_row);

        //applySkipRules.bindSkipRulesOn is exported by skip-rules.js
        applySkipRules.bindSkipRulesOn($new_row, showHybridRows);
        event.preventDefault();
    });

    $('.unassign-question').hover(function () {
        var parent_question = $(this).parents('div[class^="form-group"]');
        $(parent_question).toggleClass('question-form');
    });

    $('.remove-table-row').on('click', function (evt) {
        var $row = $(this).parents('tr'),
            $table = $row.parents('table'),
            $grid_rows = $table.find('tr.grid_row');
        deleteRow($row, $table, $grid_rows, 1);
        evt.preventDefault();
    });

    $('.remove-hybrid-row').on('click', function (evt) {
        var $row = $(this).parents('.hybrid-group-row'),
            $table = $row.parents('.question-group'),
            $grid_rows = $table.find('.hybrid-group-row');
        deleteRow($row, $table, $grid_rows, 2);
        evt.preventDefault();
    });

    $("a[post=true]").each(function () {
        $(this).on('click', function (e) {
            e.preventDefault();
            makePostRequest(
                $(this).attr('phref'),
                JSON.parse($(this).attr('pdata'))
            );
        });
    });

    $('#new-themes-modal-form,form[id^=edit-theme]').each(function () {
        $(this).validate({rules: {'name': 'required'}});
    });

    $('#duplicate-questionnaire-form').validate({
        rules: {'questionnaire': 'required', 'year': 'required', 'name': 'required'}
    });

    var elementID = '#duplicate-questionnaire-form #id_questionnaire',
        selectQuestionnaireElement = $(elementID),
        questionnaireNameElement = $('#id_name');

    selectQuestionnaireElement.on('change', function () {
        questionnaireNameElement.val($(elementID + ' option:selected').text());
    });

    $('#id_year').on('change', function () {
        $.ajax({
            type: 'get',
            url: '/questionnaire/validate/',
            data: {year: $(this).val()},
            success: function (data) {
                var htmlContent = data.status && '<div class="alert ' + data.status + '">' + data.message + '</div>';
                $('#notification').html(htmlContent);
            }
        });
    });

    $("#cancel_button").on('click', function(){
        window.history.go(-1);
    });
});

function makePostRequest(url, data) {
    var jForm = $('<form></form>');
    jForm.attr('action', url);
    jForm.attr('method', 'post');
    for (name in data) {
        var jInput = $("<input/>");
        jInput.attr({'name': name, 'value': data[name], 'type': 'hidden'});
        jForm.append(jInput);
    }
    var button = $("<input type='submit' style='display: none'/>");
    jForm.append(button);
    $("body").append(jForm);
    button.trigger('click');
}

function getCountriesFor(regions, callback) {
    var url = "/locations/countries/",
        data = $.param({'regions': regions}, true);
    $.get(url, data, callback);
}

function setDisabled(isPrimaryField, selectedAnswerType) {
    if (selectedAnswerType.toLowerCase() === "multipleresponse") {
        isPrimaryField.removeAttr('checked');
        isPrimaryField.attr('disabled', 'disabled');
    } else {
        isPrimaryField.removeAttr('disabled');
    }
}

function replaceAttributes($el, index) {
    return {
        'name': _replace($el, 'name', index),
        'id': _replace($el, 'id', index)
    };
}

function _replace($el, attr, index) {
    return $($el).attr(attr).replace(/-[\d]+-/g, '-' + index.toString() + '-');
}

function reIndexFieldNames() {
    var fieldTypes = ['MultiChoice', 'Date', 'Number', 'Text'];

    for (var i = 0; i < fieldTypes.length; i++) {
        var type = fieldTypes[i];
        var total = -1;
        var previous_name = '';
        $('#questionnaire_entry').find(":input[name^=" + type + "][type!=hidden]").each(function (index, el) {
            var $el = $(el),
                name = $el.attr('name'),
                type = $el.attr('type');
            if (!(previous_name == name && type == 'radio')) {
                total = total + 1;
            }
            var attributeMap = replaceAttributes($el, total);
            $el.attr({'name': attributeMap.name, 'id': attributeMap.id});
            var $hidden = $el.prev("input[name=" + name + "]");
            $hidden.attr({'name': attributeMap.name, 'id': attributeMap.id});
            if (previous_name != name && type == 'radio') {
                var $radio_extra_hidden = $el.prev().prev("input[name=" + name + "]");
                $radio_extra_hidden.attr({'name': attributeMap.name, 'id': attributeMap.id});
            }
            var $label = $el.parents("label");
            $label.attr('for', attributeMap.id);
            previous_name = name;
        });
        $('#id_' + type + '-MAX_NUM_FORMS').val(total + 1);
        $('#id_' + type + '-INITIAL_FORMS').val(total + 1);
        $('#id_' + type + '-TOTAL_FORMS').val(total + 1);
    }
}

function prependHiddenColumnFields(newElement) {
    var previous_name = '';
    newElement.find(':input').each(function () {
        var $el = $(this);
        var name = $el.attr('name'),
            type = $el.attr('type');
        if (!(previous_name == name && type == 'radio')) {
            $el.before('<input type="hidden" name="' + name + '" />')
        }
        if (previous_name != name && type == 'radio') {
            $el.before('<input type="hidden" exclude="true" value="" name="' + name + '" />')
        }
        previous_name = name;
    });
}

function duplicateRow(selector, $table) {
    var $selector = $(selector);
    var newElement = $selector.clone(true);
    newElement.find('input[type=hidden]').each(function () {
        $(this).remove()
    });
    newElement.find('.primary-question').each(function () {
        $(this).removeAttr('data-primary-question')
    });
    resetClonedInputs(newElement);
    prependHiddenColumnFields(newElement);
    $selector.after(newElement);
    assignRowNumbers($table);
    reIndexFieldNames();
    resetDatePicker(newElement);
    return newElement;
}

function assignRowNumbers($table) {
    $table.find("span.number").each(function (i, element) {
        $(element).text(++i);
    });
}

function showSeparator($selector) {
    var separator = $selector.find('.separator');
    separator.removeClass('hide');
    separator.show();
}

function resetDatePicker(newElement) {
    newElement.find('.datetimepicker').each(function () {
        var $this = $(this);
        $this.removeData('datepicker').unbind();
        $this.datepicker({pickTime: false, autoclose: true});
    });
}

function resetClonedInputs(newElement) {
    newElement.find(':input').each(function () {
        if ($(this).attr('type') != 'radio')
            $(this).val('');
        $(this).removeAttr('checked');
        $(this).removeAttr('selected');
    });
}

function addRowAndColumnHiddenInputs($table, group_id, row_selector) {
    $table.find(row_selector).each(function (i, el) {
        var $tr = $(this);
        $tr.find('input[type=hidden][exclude!=true]').each(function (index, element) {
            $(element).val([i, group_id]);
        });
    });
}

function addRowOn($el, row_selector, table_selector) {
    var $grid_row = $el.parents(row_selector).prev();
    var $table = $el.parents(table_selector);
    var $new_row = duplicateRow($grid_row, $table);
    var group_id = $table.attr('data-group-id');
    addRowAndColumnHiddenInputs($table, group_id, row_selector);
    return $new_row;
}

var showHybridRows = function (gridInstance) {
    $(gridInstance).find('div[class^="form-group form-group-question-"]').show();
    $(gridInstance).find('li[class^="form-group-question-"]').show();
};

var showAddMoreRows = function (tableRow) {
    $(tableRow).find('input[class^="input-question-id-"]').prop('disabled', false).removeClass('grayed-out');
    $(tableRow).find('select[class^="input-question-id-"]').prop('disabled', false).removeClass('grayed-out');
};


function return_file(filename) {
    window.location = "/export-section/" + filename;
}
function disableInputFields(status) {
    $(this).find(":input").each(function () {
        $(this).prop('disabled', status);
    });
    $('.add-more').prop('disabled', status);
}

function deleteRow($row, $table, $grid_rows, min_number_of_rows) {
    if ($grid_rows.length > min_number_of_rows) {
        deleteRowFromServer($row, $table);
        $row.remove();
        assignRowNumbers($table);
        reIndexFieldNames();
    }
}

function deleteRowFromServer($row, $table) {
    var group_id = $table.attr('data-group-id');
    var url = window.location.pathname + "delete/" + group_id + "/";
    var $primary_answer = $row.find('.primary-question').attr('data-primary-question'),
        $csrf = $('input[name=csrfmiddlewaretoken]'),
        data = {'primary_answer': $primary_answer, 'csrfmiddlewaretoken': $csrf.val()};
    if ($primary_answer) {
        $.post(url, data, function () {
        });
    }
}

function getTableRow($questionForm, $index) {
    if ($($questionForm).hasClass('group-hr')) {
        return "<tr class='group-tr' " +
            "data-group-id='" + $($questionForm).attr('data-group-id') + "'>" +
            "<td><hr class='group-hr'/></td></tr>";
    } else if ($($questionForm).hasClass('grid-group')) {
        return "<tr><td class='group-tr ' align='center'>" +
            "<div class='well well-large'><h5> Reordering of Grid Question is not supported </h5></div></td></tr>";
    } else if ($($questionForm).hasClass('none-grid-qns')) {
        return "<tr id='question-" + $index + "' class='sortable-tr'><td>" + $($questionForm).html() + "</td></tr>"
    }
    return '';
}

function getModalWithSubSectionQuestions($element) {
    var $modal = $('#reorder_modal_label'),
        action = $element.attr('data-href'),
        questionFormsAsTableRows = "";
    getQuestionsInSubsection($element).map(function (index, $questionForm) {
        questionFormsAsTableRows += getTableRow($questionForm, index)
    });
    $modal.find('#reorder-content-table').html(questionFormsAsTableRows);
    $modal.find('#re-order-questions-form').attr('action', action);
    return $modal;
}

function removeButtons($modal, btnClasses) {
    for (var i = 0; i < btnClasses.length; i++) {
        $modal.find(btnClasses[i]).remove();
    }
}

function highlightOnHover($modal) {
    $modal.find('tr').each(function () {
        $(this).hover(function () {
            $(this).toggleClass('question-form');
        });
    });
}

function callOnDropSuper($item) {
    $item.removeClass("dragged").removeAttr("style");
    $("body").removeClass("dragging");
}

function reIndexOrderFields($item, container) {
    var $table = $item.parents('table');
    var groupTableRows = $table.find('tr.group-tr');
    for (var i = 0; i < groupTableRows.length; i++) {
        var $sameGroupRows = $(groupTableRows[i]).prevUntil('tr.group-tr');
        var totalQuestionRows = $sameGroupRows.length;
        $sameGroupRows.each(function (index, questionTableRow) {
            var reverseIndex = parseInt(totalQuestionRows) - parseInt(index),
                $hiddenOrderField = $(questionTableRow).find('input[type=hidden]'),
                hiddenFieldValue = $hiddenOrderField.val(),
                orderId = hiddenFieldValue && hiddenFieldValue.split(",")[1];
            $hiddenOrderField.val('');
            $hiddenOrderField.val($(groupTableRows[i]).attr('data-group-id') + "," + orderId + "," + reverseIndex);
        });
    }
}

var activateSortable = function($modal) {
    $modal.find('table').each(function () {
        $(this).sortable({
            containerSelector: 'table',
            itemPath: '>tbody',
            itemSelector: '.sortable-tr',
            placeholder: '<tr class="placeholder"/>',
            onDrop: function ($item, container, _super) {
                callOnDropSuper($item);
                reIndexOrderFields($item, container);
            }
        });
    })
};


function getQuestionsInSubsection($element) {
    var $subsectionContainer = $element.parents('div .subsection-content');
    return $subsectionContainer.find('.form-group, .group-hr, .grid-group');
}


function addSpecifyField($element) {
    var parentElementName = $element.attr('name'),
        newElementName = parentElementName.replace('response', 'specified_option'),
        $otherField = "<input type='text' id='specified_response' maxlength='100'" +
            "name='" + newElementName + "' class='form-control input-sm specified_response'" +
            "placeholder='Specify'>";
    $element.after($otherField);
}