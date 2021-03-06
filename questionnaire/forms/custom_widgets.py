from itertools import chain

from django import forms
from django.forms import ModelMultipleChoiceField
from django.forms.widgets import RadioFieldRenderer
from django.utils.encoding import force_text
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

from questionnaire.models import Question, SkipRule
from questionnaire.models.skip_rule import SkipQuestion, SkipSubsection
from questionnaire.utils.questionnaire_entry_helpers import is_in_grid


def get_rules(option_id, subsection):
    all_rules = SkipRule.objects.filter(response_id=option_id, subsection=subsection)
    question_rules = ''
    subsection_rules = ''
    hybrid_grid_rules = ''
    if all_rules.exists():
        rules_skipping_questions = filter(lambda rule: not rule.is_in_hybrid_grid(),
                                          SkipQuestion.objects.filter(subsection=subsection, response_id=option_id))
        rules_skipping_questions_in_hybrid_grids = filter(lambda rule: rule.is_in_hybrid_grid(),
                                                          SkipQuestion.objects.filter(subsection=subsection,
                                                                                      response_id=option_id))
        rules_skipping_subsections = SkipSubsection.objects.filter(subsection=subsection, response_id=option_id)
        question_rules = ",".join(map(lambda rule: str(rule.skip_question.id), rules_skipping_questions))
        hybrid_grid_rules = ",".join(
            map(lambda rule: str(rule.skip_question.id), rules_skipping_questions_in_hybrid_grids))
        subsection_rules = ",".join(map(lambda rule: str(rule.skip_subsection.id), rules_skipping_subsections))

    return question_rules, subsection_rules, hybrid_grid_rules


class MultiChoiceAnswerSelectWidget(forms.Select):
    def __init__(self, subsection, attrs=None, choices=(), question_options=None):
        super(MultiChoiceAnswerSelectWidget, self).__init__(attrs, choices)
        self.question_options = question_options
        self.subsection = subsection

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_text(option_value)
        data_instruction = ''
        data_skip_rule = ''
        data_subsection_skip_rule = ''
        data_hybrid_grid_rules = ''

        if option_value:
            question_option = self.question_options.get(id=int(option_value))
            data_instruction = mark_safe(' data-instructions="%s"' % question_option.instructions)

            (question_rules, subsection_rules, hybrid_grid_rules) = get_rules(question_option, self.subsection)
            if question_rules != "":
                data_skip_rule = mark_safe(' data-skip-rules="%s"' % question_rules)
            if subsection_rules != "":
                data_subsection_skip_rule = mark_safe(' data-skip-subsection="%s"' % subsection_rules)
            if hybrid_grid_rules != "":
                data_hybrid_grid_rules = mark_safe(' data-skip-hybrid-grid-rules="%s"' % hybrid_grid_rules)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
        else:
            selected_html = ''

        return format_html('<option value="{0}"{1}{2}{3}{4}{5}>{6}</option>',
                           option_value,
                           selected_html,
                           data_instruction,
                           data_skip_rule,
                           data_subsection_skip_rule,
                           data_hybrid_grid_rules,
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
    def __init__(self, name, value, attrs, choices, subsection=None):
        super(DataRuleRadioFieldRenderer, self).__init__(name, value, attrs, choices)
        self.subsection = subsection

    def render(self):
        inputs = map(lambda option: self._add_attr(option), self)
        return format_html('<ul>\n{0}\n</ul>',
                           format_html_join("", '<li>{0}</li>', [(force_text(w),) for w in inputs]))

    def _add_attr(self, option):
        (question_rules, subsection_rules, hybrid_grid_rules) = self._get_rules(option.choice_value)
        if question_rules != "":
            option.attrs.update({'data-skip-rules': question_rules})
        if subsection_rules != "":
            option.attrs.update({'data-skip-subsection': subsection_rules})
        if hybrid_grid_rules != "":
            option.attrs.update({'data-skip-hybrid-grid-rules': hybrid_grid_rules})
        return option

    def _get_rules(self, option):
        return get_rules(option, self.subsection)


class SkipRuleRadioWidget(forms.RadioSelect):
    renderer = DataRuleRadioFieldRenderer

    def __init__(self, subsection, *args, **kwargs):
        super(SkipRuleRadioWidget, self).__init__(*args, **kwargs)
        self.subsection = subsection

    def get_renderer(self, name, value, attrs=None, choices=()):
        """Returns an instance of the renderer."""
        if value is None: value = ''
        str_value = force_text(value)  # Normalize to string.
        final_attrs = self.build_attrs(attrs)
        choices = list(chain(self.choices, choices))
        return self.renderer(name, str_value, final_attrs, choices, self.subsection)


class MultipleResponseChoiceField(ModelMultipleChoiceField):
    def clean(self, value):
        return super(MultipleResponseChoiceField, self).clean(self._remove_group_data(value))

    def _remove_group_data(self, value):
        if value and is_in_grid(value[0]):
            return value[1:]
        return value