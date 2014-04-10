from questionnaire.models import Question, QuestionOption, MultiChoiceAnswer
from questionnaire.tests.base_test import BaseTest
from questionnaire.utils.service_utils import export_id, export_text


class GRIDQuestionsExportTest(BaseTest):
    def setUp(self):
        self.primary_question = Question.objects.create(text='Disease', UID='C00003', answer_type='MultiChoice',
                                                        is_primary=True)
        self.option = QuestionOption.objects.create(text="Measles", question=self.primary_question, UID="QO1")
        self.option_without_uid = QuestionOption.objects.create(text="TB", question=self.primary_question)

    def test_export_id(self):
        primary_answer = MultiChoiceAnswer.objects.filter()
        self.assertEqual('', export_id(primary_answer))

        primary_question_answer = MultiChoiceAnswer.objects.create(question=self.primary_question, response=self.option_without_uid)
        primary_answer = MultiChoiceAnswer.objects.filter(id=primary_question_answer.id)
        self.assertEqual('_None', export_id(primary_answer))

        primary_question_answer = MultiChoiceAnswer.objects.create(question=self.primary_question, response=self.option)
        primary_answer = MultiChoiceAnswer.objects.filter(id=primary_question_answer.id)
        self.assertEqual('_QO1', export_id(primary_answer))

    def test_export_text(self):
        primary_answer = MultiChoiceAnswer.objects.filter()
        self.assertEqual('', export_text(primary_answer))

        primary_question_answer = MultiChoiceAnswer.objects.create(question=self.primary_question, response=self.option_without_uid)
        primary_answer = MultiChoiceAnswer.objects.filter(id=primary_question_answer.id)
        self.assertEqual(' | TB', export_text(primary_answer))

        primary_question_answer = MultiChoiceAnswer.objects.create(question=self.primary_question, response=self.option)
        primary_answer = MultiChoiceAnswer.objects.filter(id=primary_question_answer.id)
        self.assertEqual(' | Measles', export_text(primary_answer))
