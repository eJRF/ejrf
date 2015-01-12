$(document).ready(function () {
    $('#id_organization').on('change', function () {
        getRegionsFor($(this), '#id_region');
    });
    $("#cancel_button").on('click', function(){
        window.history.go(-1);
    });
});

$(document).on('change', '#organization', function () {
    getRegionsFor(this, '#region');
});

function getRegionsFor(organization, region) {
    var organization_id = $(organization).val(),
        url = "/locations/organization/" + organization_id + "/region/",
        region_select = $(region);
    $.get(url, function (data) {
        region_select.html(' ');
        region_select.html('<option value=" ">Choose a Region </option>');
        for (var i = 0; i < data.length; i++) {
            region_select.append('<option value=' + data[i].id + '>' + data[i].name + '</option>')
        }
    })
}

var template = $("#organization-template").html(),
    country_template = $('#country-template').html(),
    region_template = $('#region-template').html();

function loadCountryOrRegionTemplate(template) {
    $(this).parents('ul').after(template);
}

function hideElements(elements) {
    for (var  index = 0; index < elements.length; ++index) {
        $(elements[index]).hide();
    }
}

function showElements(elements) {
    for (var  index = 0; index < elements.length; ++index) {
        $(elements[index]).show();
    }
}

function resetElementValue(elements) {
    for (var  index = 0; index < elements.length; ++index) {
        $(elements[index]).val('');
    }
}

function addRequiredValidationRule(elements) {
    for (var index = 0; index < elements.length; ++index) {
        if ($(elements[index]).length <= 0)
            continue;

        $(elements[index]).rules("add", {required: true});
    }
}

function disableFields(selector) {
    $('body').find(selector).prop('disabled', true);
}

function groupRolesBootstrap() {
    var $organization_element = $('#create-user-form #id_organization'),
        $region_element = $('#create-user-form #id_region'),
        $country_element = $('#create-user-form #id_country');


    $('#id-reset-password-form').validate();
    $('#create-user-form').validate();
    $region_element.html('<option value>Choose a Region</option>');

    hideElements([$organization_element.parent(), $region_element.parent(),
        $country_element.parent()]);

    addRequiredValidationRule([$('#id_username'), $('#id_password1'),
        $('#id_password2'), $('#id_email'), $('input[name="groups"]')]);

    $('.radio-roles').on('change', function () {
        var $selected_role = $.trim($(this).parents('label').text());
        if ($selected_role === "Global Admin") {
            disableFields('#create-user-form #id_region');
            disableFields('#create-user-form #id_country');
            hideElements([$region_element.parent(), $country_element.parent()]);
            resetElementValue([$region_element, $country_element]);
            showElements([$organization_element.parent()]);
            addRequiredValidationRule($organization_element);
        } else if ($selected_role == "Regional Admin") {
            showElements([$organization_element.parent(), $region_element.parent()]);
            resetElementValue([$organization_element, $region_element]);
            hideElements([$country_element.parent()]);
            addRequiredValidationRule([$organization_element, $region_element]);
        } else if ($selected_role == "Country Admin" || $selected_role == "Data Submitter") {
            disableFields('#create-user-form #id_region');
            showElements([$country_element.parent()]);
            hideElements([$organization_element.parent(), $region_element.parent()]);
            resetElementValue([$organization_element, $region_element]);
            addRequiredValidationRule($country_element);
        }
    });

    $('.radio-roles:checked').each(function () {
        $(this).trigger("change")
    });
}