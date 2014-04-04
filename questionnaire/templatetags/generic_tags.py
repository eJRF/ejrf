from django import template
from django.core.urlresolvers import reverse
from questionnaire.forms.questions import QuestionForm
from questionnaire.forms.theme import ThemeForm
from questionnaire.models import Questionnaire

ASSIGN_QUESTION_PAGINATION_SIZE = 30

register = template.Library()


@register.filter
def display_list(_list):
    new_list = [str(item) for item in _list]
    return ', '.join(new_list)


@register.filter
def bootstrap_message(django_message):
    if django_message == 'error':
        return 'danger'
    return django_message


@register.filter
def get_url_with_ids(args, url_name):
    if not str(args).isdigit():
        arg_list = [int(arg) for arg in args.split(',')]
        return reverse(url_name, args=arg_list)
    return reverse(url_name, args=(args,))


@register.filter
def divide_to_paginate(questions):
    size_of_paginated = 1 + len(questions)/ASSIGN_QUESTION_PAGINATION_SIZE
    paginated = [questions[i * ASSIGN_QUESTION_PAGINATION_SIZE:(i+1) * ASSIGN_QUESTION_PAGINATION_SIZE] for i in range(size_of_paginated)]
    return paginated


@register.filter
def add_string(int_1, int_2):
    return "%s, %s" % (str(int_1), str(int_2))


@register.assignment_tag
def get_questionnaire_from(region, **kwargs):
    region_questionnaire_map = kwargs['regions_questionnaire_map']
    return region_questionnaire_map[region][kwargs['status']]


@register.filter
def bootstrap_class(status):
    css_class_status_map = {'Submitted': 'text-success', 'In Progress': 'text-warning', 'Not Started': 'text-danger'}
    return css_class_status_map[status]

@register.filter
def packaged_options(question, packaged_opts):
    question_options = question.options.values_list('text', flat=True)
    if packaged_opts == ", ".join(question_options):
        return 'checked'

@register.filter
def custom_options(question):
    question_options = question.options.values_list('text', flat=True)
    options_string = ", ".join(question_options)
    if not options_string in QuestionForm.KNOWN_OPTIONS:
        return 'checked'


@register.filter
def get_theme_form_with_instance(theme):
    return ThemeForm(instance=theme)

@register.filter
def get_reverse_sort_key(key, default):
    if key:
        if key.startswith('-'):
            reverse_key = key.replace('-', '', 1)

            if reverse_key <> default:
                return default

            return reverse_key
        else:
            if key == default:
                return '-' + key

    return default

@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()