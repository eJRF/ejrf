from questionnaire.forms.custom_widgets import MultiChoiceAnswerSelectWidget, MultiChoiceQuestionSelectWidget
from questionnaire.models import Question, QuestionOption
from questionnaire.tests.base_test import BaseTest

class MultiChoiceAnswerSelectWidgetTest(BaseTest):

    def test_option_has_data_attributes_on_top_of_normal_attributes(self):
        question = Question.objects.create(text='what do you drink?', UID='C_2013', answer_type='MultiChoice')
        option1 = QuestionOption.objects.create(text='tusker lager', question=question, instructions="yeah yeah")
        option2 = QuestionOption.objects.create(text='club', question=question, instructions="Are you crazy?")

        choices = ((option1.id, option1.text), (option2.id, option2.text))

        widget = MultiChoiceAnswerSelectWidget(choices=choices, question_options=question.options.all())

        expected_option_1 = '<option value="%d" selected="selected" data-instructions="%s">%s</option>' % (option1.id, option1.instructions, option1.text)
        expected_option_2 = '<option value="%d" data-instructions="%s">%s</option>' % (option2.id, option2.instructions, option2.text)

        self.assertEqual(expected_option_1,
                         widget.render_option(selected_choices=[str(option1.id)], option_value=option1.id, option_label=option1.text))
        self.assertEqual(expected_option_2,
                         widget.render_option(selected_choices=[str(option1.id)], option_value=option2.id, option_label=option2.text))


class MultiChoiceQuestionSelectWidgetTest(BaseTest):

    def test_option_has_data_attributes_on_top_of_normal_attributes(self):
        question = Question.objects.create(text='what do you drink?', UID='C_2013', answer_type='MultiChoice')
        question2 = Question.objects.create(text='what do you what?', UID='C_2014', answer_type='Text')
        question3 = Question.objects.create(text='what do you when?', UID='C_2015', answer_type='Number')

        choices = ((question.id, question.text), (question2.id, question2.text), (question3.id, question3.text))

        widget = MultiChoiceQuestionSelectWidget(choices=choices)

        expected_option_1 = '<option value="%d" multichoice="true">%s</option>' % (question.id,  question.text)
        expected_option_2 = '<option value="%d">%s</option>' % (question2.id,  question2.text)
        expected_option_3 = '<option value="%d" selected="selected">%s</option>' % (question3.id,  question3.text)

        self.assertEqual(expected_option_1,
                         widget.render_option(selected_choices=[str(question3.id)], option_value=question.id, option_label=question.text))
        self.assertEqual(expected_option_2,
                         widget.render_option(selected_choices=[str(question3.id)], option_value=question2.id, option_label=question2.text))
        self.assertEqual(expected_option_3,
                         widget.render_option(selected_choices=[str(question3.id)], option_value=question3.id, option_label=question3.text))