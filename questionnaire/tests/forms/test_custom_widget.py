from django.core import serializers

from questionnaire.forms.custom_widgets import MultiChoiceAnswerSelectWidget, MultiChoiceQuestionSelectWidget, \
    SkipRuleRadioWidget, DataRuleRadioFieldRenderer
from questionnaire.models import Question, QuestionOption, Theme
from questionnaire.tests.base_test import BaseTest
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.question_group_factory import QuestionGroupFactory
from questionnaire.tests.factories.skip_rule_factory import SkipRuleFactory
from questionnaire.tests.factories.sub_section_factory import SubSectionFactory


class MultiChoiceAnswerSelectWidgetTest(BaseTest):
    def test_option_has_data_attributes_on_top_of_normal_attributes(self):
        subsection = SubSectionFactory()
        question_group = QuestionGroupFactory(subsection=subsection)
        question = QuestionFactory(text='what do you drink?', UID='C_2013', answer_type='MultiChoice')
        question_group.question.add(question)
        option1 = QuestionOption.objects.create(text='tusker lager', question=question, instructions="yeah yeah")
        option2 = QuestionOption.objects.create(text='club', question=question, instructions="Are you crazy?")
        choices = ((option1.id, option1.text), (option2.id, option2.text))
        skip_question = QuestionFactory()
        skip_rule = SkipRuleFactory(root_question=question, response=option1, subsection=subsection,
                                        skip_question=skip_question)
        skip_rule2 = SkipRuleFactory(root_question=question, response=option2, subsection=subsection,
                                         skip_subsection=subsection)

        widget = MultiChoiceAnswerSelectWidget(subsection, choices=choices, question_options=question.options.all())

        expected_option_1 = '<option value="%d" selected="selected" data-instructions="%s" data-skip-rules="%s" data-skip-subsection="">%s</option>' % (
            option1.id, option1.instructions, skip_rule.skip_question.id, option1.text)
        expected_option_2 = '<option value="%d" data-instructions="%s" data-skip-rules="" data-skip-subsection="%s">%s</option>' % (
            option2.id, option2.instructions, skip_rule2.skip_subsection.id, option2.text)

        self.assertEqual(expected_option_1,
                         widget.render_option(selected_choices=[str(option1.id)], option_value=option1.id,
                                              option_label=option1.text))
        self.assertEqual(expected_option_2,
                         widget.render_option(selected_choices=[str(option1.id)], option_value=option2.id,
                                              option_label=option2.text))


class MultiChoiceQuestionSelectWidgetTest(BaseTest):
    def test_option_has_multichoice_and_theme_attributes_on_top_of_normal_attributes(self):
        theme1 = Theme.objects.create(name="Theme1", description="Our theme.")
        theme2 = Theme.objects.create(name="Theme2", description="Our theme.")
        question = Question.objects.create(text='what do you drink?', UID='C_2013', answer_type='MultiChoice',
                                           theme=theme1)
        question2 = Question.objects.create(text='what do you what?', UID='C_2014', answer_type='Text', theme=theme2)
        question3 = Question.objects.create(text='what do you when?', UID='C_2015', answer_type='Number', theme=theme1)

        choices = ((question.id, question.text), (question2.id, question2.text), (question3.id, question3.text))

        widget = MultiChoiceQuestionSelectWidget(choices=choices)

        expected_option_1 = '<option value="%d" multichoice="true" theme="%s">%s</option>' % (
            question.id, theme1.id, question.text,)
        expected_option_2 = '<option value="%d" theme="%s">%s</option>' % (question2.id, theme2.id, question2.text, )
        expected_option_3 = '<option value="%d" selected="selected" theme="%s">%s</option>' % (
            question3.id, theme1.id, question3.text,)

        self.assertEqual(expected_option_1,
                         widget.render_option(selected_choices=[str(question3.id)], option_value=question.id,
                                              option_label=question.text))
        self.assertEqual(expected_option_2,
                         widget.render_option(selected_choices=[str(question3.id)], option_value=question2.id,
                                              option_label=question2.text))
        self.assertEqual(expected_option_3,
                         widget.render_option(selected_choices=[str(question3.id)], option_value=question3.id,
                                              option_label=question3.text))


class SkipRuleSelectWidgetTest(BaseTest):
    def test_render(self):
        subsection = SubSectionFactory()
        question_group = QuestionGroupFactory(subsection=subsection)
        question = Question.objects.create(text='what do you drink?', UID='C_2013', answer_type='MultiChoice')
        option1 = QuestionOption.objects.create(text='tusker lager', question=question, instructions="yeah yeah")
        option2 = QuestionOption.objects.create(text='tusker lager 2', question=question, instructions="ok yeah yeah")
        question_group.question.add(question)
        skip_question = QuestionFactory()
        skip_rule = SkipRuleFactory(root_question=question, response=option1, subsection=subsection,
                                        skip_question=skip_question)
        skip_rule2 = SkipRuleFactory(root_question=question, response=option1, subsection=subsection,
                                         skip_subsection=subsection)
        widget = SkipRuleRadioWidget(subsection)


        expected_stuff = '<ul>\n' \
                         '<li><label><input checked="checked" data-skip-rules="%s" data-skip-subsection="%s" name="name" type="radio" value="%s" /> %s</label></li>' \
                         '<li><label><input data-skip-rules="" data-skip-subsection="" name="name" type="radio" value="%s" /> %s</label></li>' \
                         '<li><label><input data-skip-rules="" data-skip-subsection="" name="name" type="radio" value="2" /> Really</label></li>\n' \
                         '</ul>' \
                         % (skip_rule.skip_question.id, skip_rule2.skip_subsection.id, option1.id, option1.text, option2.id, option2.text)
        self.assertEqual(expected_stuff,
                         widget.render('name', option1.id, choices=((option1.id, option1.text), (option2.id, option2.text), ('2', 'Really'))))


class DataRuleRadioFieldRendererTest(BaseTest):
    def test_get_rules_for_option(self):
        question = Question.objects.create(text='what do you drink?', UID='C_2013', answer_type='MultiChoice')
        skip_question = QuestionFactory()

        option1 = QuestionOption.objects.create(text='tusker lager', question=question, instructions="yeah yeah")

        subsection = SubSectionFactory()

        question_group = QuestionGroupFactory(subsection=subsection)

        question_group.question.add(question)

        skip_rule = SkipRuleFactory(root_question=question, response=option1, subsection=subsection,
                                        skip_question=skip_question)

        skip_rule2 = SkipRuleFactory(root_question=question, response=option1, subsection=subsection,
                                         skip_subsection=subsection)

        renderer = DataRuleRadioFieldRenderer('name', 1, attrs={},
                                              choices=((option1.id, option1.text), ('2', 'Really'),),
                                              subsection=subsection)

        rules_for_option_1 = renderer._get_rules(option1.id)
        expected_rule = (str(skip_rule.skip_question.id), str(skip_rule2.skip_subsection.id))

        self.assertEqual(expected_rule, rules_for_option_1)

