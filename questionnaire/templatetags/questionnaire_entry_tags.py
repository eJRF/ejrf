from django import template

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