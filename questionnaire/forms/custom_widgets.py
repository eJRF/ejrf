from django import forms
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from questionnaire.models import Question


class MultiChoiceAnswerSelectWidget(forms.Select):
    def __init__(self, attrs=None, choices=(), question_options=None):
        super(MultiChoiceAnswerSelectWidget, self).__init__(attrs, choices)
        self.question_options = question_options

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_text(option_value)
        data_instruction = ''
        if option_value:
            data_instruction = mark_safe(' data-instructions="%s"' % self.question_options.get(id=int(option_value)).instructions)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
        else:
            selected_html = ''
        return format_html('<option value="{0}"{1}{2}>{3}</option>',
                           option_value,
                           selected_html,
                           data_instruction,
                           force_text(option_label))


class MultiChoiceQuestionSelectWidget(forms.Select):
    def __init__(self, attrs=None, choices=()):
        super(MultiChoiceQuestionSelectWidget, self).__init__(attrs, choices)

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_text(option_value)
        question = self._question(option_value)
        multichoice = ''
        theme = ''
        if question:
            if question[0].is_multichoice():
                multichoice = mark_safe(' multichoice="true"')
            if question[0].theme:
                theme = mark_safe(' theme="%d"'% question[0].theme.id)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
        else:
            selected_html = ''
        return format_html('<option value="{0}"{1}{2}{3}>{4}</option>',
                           option_value,
                           selected_html,
                           multichoice,
                           theme,
                           force_text(option_label))

    def _question(self, option_value):
        if not option_value.isdigit():
            return None
        return Question.objects.filter(id=option_value)
