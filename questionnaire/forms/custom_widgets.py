from django import forms
from django.forms.widgets import RadioFieldRenderer
from django.utils.encoding import force_text
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

from questionnaire.models import Question, QuestionOption


class MultiChoiceAnswerSelectWidget(forms.Select):
    def __init__(self, attrs=None, choices=(), question_options=None):
        super(MultiChoiceAnswerSelectWidget, self).__init__(attrs, choices)
        self.question_options = question_options

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_text(option_value)
        data_instruction = ''
        data_skip_rule = ''
        skip_question = ''

        if option_value:
            question_option = self.question_options.get(id=int(option_value))
            data_instruction = mark_safe(' data-instructions="%s"' % question_option.instructions)
            rules_all = question_option.skip_rules.all()
            if rules_all.exists():
                skip_question = rules_all[0].skip_question.id
            data_skip_rule = mark_safe(' data-skip-rules="%s"' % skip_question)
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

    # self.attrs.update({"data-skip-rule":self._get_rules(w.choice_value)})
    def render(self):
        inputs = map(lambda option: self._add_attr(option), self)
        return format_html('<ul>\n{0}\n</ul>',
                           format_html_join("", '<li>{0}</li>', [(force_text(w),) for w in inputs]))

    def _add_attr(self, option):
        option.attrs.update({'data-skip-rules': self._get_rules(option.choice_value)})
        return option

    def _get_rules(self, option):
        options = QuestionOption.objects.filter(id=option, skip_rules__isnull=False)
        blank = ''
        if options.exists():
            all_rules = options[0].skip_rules.all()
            return all_rules[0].skip_question.id
        return blank


class SkipRuleRadioWidget(forms.RadioSelect):
    renderer = DataRuleRadioFieldRenderer

    def __init__(self, *args, **kwargs):
        super(SkipRuleRadioWidget, self).__init__(*args, **kwargs)


