from django import template
from questionnaire.models.skip_rule import SkipQuestion

register = template.Library()


@register.filter
def get_form(question, formsets):
    form = formsets.next_ordered_form(question)
    fields_ = form.visible_fields()[0]
    return [fields_]


@register.filter
def get_value(key, a_dict):
    return a_dict.get(key)


@register.filter
def _filename(path):
    return str(path).split('/')[1]

@register.filter
def get_questions_to_skip(option, subsection):
    return SkipQuestion.objects.filter(response=option, subsection=subsection).values_list('skip_question', flat=True)