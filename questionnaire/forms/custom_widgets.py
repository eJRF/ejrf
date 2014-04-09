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
    def __init__(self, attrs=None, choices=(), question_options=None):
        super(MultiChoiceQuestionSelectWidget, self).__init__(attrs, choices)
        self.question_options = question_options

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_text(option_value)
        multichoice = ''
        if self._is_multichoice(option_value):
            multichoice = mark_safe(' multichoice="true"')
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
        else:
            selected_html = ''
        return format_html('<option value="{0}"{1}{2}>{3}</option>',
                           option_value,
                           selected_html,
                           multichoice,
                           force_text(option_label))

    def _is_multichoice(self, option_value):
        if not option_value.isdigit():
            return False
        question = Question.objects.filter(id=option_value)
        if question.exists():
            return question[0].is_multichoice()
        return False