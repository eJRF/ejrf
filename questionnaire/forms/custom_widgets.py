from django import forms
from django.forms.widgets import RadioFieldRenderer
from django.utils.encoding import force_text
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from questionnaire.models import Question, QuestionOption
from django.core import serializers


class MultiChoiceAnswerSelectWidget(forms.Select):
    def __init__(self, attrs=None, choices=(), question_options=None):
        super(MultiChoiceAnswerSelectWidget, self).__init__(attrs, choices)
        self.question_options = question_options

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_text(option_value)
        data_instruction = ''
        data_skip_rule = ''
        if option_value:
            question_option = self.question_options.get(id=int(option_value))
            data_instruction = mark_safe(' data-instructions="%s"' % question_option.instructions)
            data_skip_rule = mark_safe(
                ' data-skip-rule="%s"' % serializers.serialize('json', question_option.skip_rules.all()))
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
        else:
            selected_html = ''
        return format_html('<option value="{0}"{1}{2}{3}>{4}</option>',
                           option_value,
                           selected_html,
                           data_instruction,
                           data_skip_rule,
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
                theme = mark_safe(' theme="%d"' % question[0].theme.id)
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


class DataRuleRadioFieldRenderer(RadioFieldRenderer):
    def __init__(self, name, value, attrs, choices):
        super(DataRuleRadioFieldRenderer, self).__init__(name, value, attrs, choices)

    def render(self):
        return format_html('<ul>\n{0}\n</ul>',
                           format_html_join('\n', '<li data-skip-rules="{0}">{1}</li>',
                                            [(self._get_rules(w.choice_value), force_text(w),) for w in self]))

    def _get_rules(self, option):
        options = QuestionOption.objects.filter(id=option, skip_rules__isnull=False)
        blank = ''
        if options.exists():
            all_rules = options[0].skip_rules.all()
            return all_rules[0].skip_question.id
        return blank


class SkipRuleSelectWidget(forms.RadioSelect):
    renderer = DataRuleRadioFieldRenderer

    def __init__(self, *args, **kwargs):
        super(SkipRuleSelectWidget, self).__init__(*args, **kwargs)