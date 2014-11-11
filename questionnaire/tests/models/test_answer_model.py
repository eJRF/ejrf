from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from questionnaire.models import Question, Country, QuestionOption, MultiChoiceAnswer, Questionnaire
from questionnaire.models.answers import Answer, NumericalAnswer, TextAnswer, DateAnswer, MultipleResponseAnswer
from questionnaire.tests.base_test import BaseTest
from questionnaire.tests.factories.answer_factory import NumericalAnswerFactory, TextAnswerFactory, DateAnswerFactory, \
    MultiChoiceAnswerFactory, MultipleResponseAnswerFactory
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.question_option_factory import QuestionOptionFactory
from questionnaire.tests.factories.region_factory import CountryFactory
from questionnaire.utils.answer_type import AnswerTypes


class AnswerTest(TestCase):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan")

    def test_answer_fields(self):
        answer = Answer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(9, len(fields))
        for field in ['id', 'created', 'modified', 'status', 'version', 'question_id', 'country_id', 'code',
                      'questionnaire_id']:
            self.assertIn(field, fields)

    def test_answer_stores(self):
        question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Number')
        country = Country.objects.create(name="Peru")
        answer = Answer.objects.create(question=question, country=country, questionnaire=self.questionnaire)
        self.failUnless(answer.id)
        self.assertEqual(question, answer.question)
        self.assertEqual(country, answer.country)
        self.assertEqual(self.questionnaire, answer.questionnaire)
        self.assertEqual(None, answer.code)

    def test_knows_is_draft(self):
        question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Number')
        country = Country.objects.create(name="Peru")
        draft_answer = Answer.objects.create(question=question, country=country, status=Answer.DRAFT_STATUS,
                                             questionnaire=self.questionnaire)
        submitted_answer = Answer.objects.create(question=question, country=country, status=Answer.SUBMITTED_STATUS,
                                                 questionnaire=self.questionnaire)
        self.failUnless(draft_answer.id)
        self.failUnless(submitted_answer.id)
        self.assertTrue(draft_answer.is_draft())
        self.assertFalse(submitted_answer.is_draft())

    def test_knows_corresponding_answer_given_response(self):
        data = {
            'questionnaire': self.questionnaire,
            'question': Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123',
                                                answer_type='Number'),
            'country': Country.objects.create(name="Peru"),
            'version': 1}

        textanswer = TextAnswer.objects.create(response="text", **data)
        dateanswer = DateAnswer.objects.create(response="2014-04-08", **data)
        numberanswer = NumericalAnswer.objects.create(response=1, **data)
        option = QuestionOption.objects.create(text="haha", question=data['question'])
        multichoiceanswer = MultiChoiceAnswer.objects.create(response=option, **data)

        text_answers = Answer.from_response("text", **data)
        self.assertEqual(1, text_answers.count())
        self.assertIn(textanswer, text_answers)

        numerical_answers = Answer.from_response(1, **data)
        self.assertEqual(1, numerical_answers.count())
        self.assertIn(numberanswer, numerical_answers)

        multichoice_answers = Answer.from_response(option, **data)
        self.assertEqual(1, multichoice_answers.count())
        self.assertIn(multichoiceanswer, multichoice_answers)

        date_answers = Answer.from_response("2014-04-08", **data)
        self.assertEqual(1, date_answers.count())
        self.assertIn(dateanswer, date_answers)


class NumericalAnswerTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan")
        self.question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123',
                                                answer_type='Date', answer_sub_type=AnswerTypes.INTEGER)
        self.country = Country.objects.create(name="Peru")

    def test_numerical_answer_fields(self):
        answer = NumericalAnswer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(11, len(fields))
        for field in ['id', 'created', 'modified', 'question_id', 'country_id', 'response', 'code', 'questionnaire_id']:
            self.assertIn(field, fields)

    def test_numerical_answer_store(self):
        answer = NumericalAnswer.objects.create(question=self.question, country=self.country, response=11.2,
                                                questionnaire=self.questionnaire)
        self.failUnless(answer.id)
        self.assertEqual(self.question, answer.question)
        self.assertEqual(self.country, answer.country)
        self.assertEqual(self.questionnaire, answer.questionnaire)
        self.assertEqual(11, answer.format_response())
        int_answer = NumericalAnswer.objects.create(question=self.question, country=self.country, response=11.00,
                                                    questionnaire=self.questionnaire)
        self.assertEqual(11, int_answer.format_response())

    def test_numerical_answer_cannot_be_text(self):
        answer = NumericalAnswer(question=self.question, country=self.country, response='not a decimal number',
                                 questionnaire=self.questionnaire)
        self.assertRaises(ValidationError, answer.save)

    def test_format_response_returns_decimal_when_question_answer_sub_type_is_decimal(self):
        question = QuestionFactory(answer_type=AnswerTypes.NUMBER, answer_sub_type=AnswerTypes.DECIMAL)
        answer_one = NumericalAnswerFactory(question=question, response=44.6)
        answer_two = NumericalAnswerFactory(question=question, response=44)
        self.assertEqual(44.6, answer_one.format_response())
        self.assertEqual(44.0, answer_two.format_response())

    def test_format_response_returns_integer_when_question_answer_sub_type_is_integer(self):
        question = QuestionFactory(answer_type=AnswerTypes.NUMBER, answer_sub_type=AnswerTypes.INTEGER)
        answer_one = NumericalAnswerFactory(question=question, response=44.6)
        answer_two = NumericalAnswerFactory(question=question, response=44)
        self.assertEqual(44, answer_one.format_response())
        self.assertEqual(44, answer_two.format_response())

    def test_unicode(self):
        answer = NumericalAnswerFactory(response=1)
        self.assertEqual("1", str(answer))


class TextAnswerTest(TestCase):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan")

    def test_text_answer_fields(self):
        answer = TextAnswer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(11, len(fields))
        for field in ['id', 'created', 'modified', 'question_id', 'country_id', 'response', 'code', 'questionnaire_id']:
            self.assertIn(field, fields)

    def test_text_answer_store(self):
        question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        country = Country.objects.create(name="Peru")
        answer = TextAnswer.objects.create(question=question, country=country, response="this is a text response",
                                           questionnaire=self.questionnaire)
        self.failUnless(answer.id)
        self.assertEqual(question, answer.question)
        self.assertEqual(country, answer.country)
        self.assertEqual(self.questionnaire, answer.questionnaire)
        self.assertEqual("this is a text response", answer.response)

    def test_format_returns_response_text(self):
        question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        country = Country.objects.create(name="Peru")
        answer = TextAnswer.objects.create(question=question, country=country, response="this is a text response",
                                           questionnaire=self.questionnaire)
        self.assertEqual("this is a text response", answer.format_response())

    def test_unicode(self):
        answer = TextAnswerFactory(response='Haha')
        self.assertEqual('Haha', str(answer))


class DateAnswerTest(TestCase):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan")
        self.question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123',
                                                answer_type='Date')
        self.country = Country.objects.create(name="Peru")

    def test_date_answer_fields(self):
        answer = DateAnswer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(11, len(fields))
        for field in ['id', 'created', 'modified', 'question_id', 'country_id', 'response', 'code', 'questionnaire_id']:
            self.assertIn(field, fields)

    def test_date_answer_store(self):
        some_date = date.today()
        answer = DateAnswer.objects.create(question=self.question, country=self.country, response=some_date,
                                           questionnaire=self.questionnaire)
        self.failUnless(answer.id)
        self.assertEqual(self.question, answer.question)
        self.assertEqual(self.country, answer.country)
        self.assertEqual(self.questionnaire, answer.questionnaire)
        self.assertEqual(some_date, answer.response)
        self.assertEqual(some_date, answer.format_response())

    def test_unicode_dd_mm_yyyy(self):
        date_as_str = '01/02/2014'
        answer = DateAnswerFactory(response=date_as_str)
        self.assertEqual(date_as_str, str(answer))


class MultiChoiceAnswerTest(TestCase):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan")

    def test_mulitchoice_answer_fields(self):
        answer = MultiChoiceAnswer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(11, len(fields))
        for field in ['id', 'created', 'modified', 'question_id', 'country_id', 'response_id', 'code',
                      'questionnaire_id']:
            self.assertIn(field, fields)

    def test_mulitchoice_answer_store(self):
        question = Question.objects.create(text='what do you drink?', UID='abc123', answer_type='MultiChoice')
        country = Country.objects.create(name="Peru")
        option = QuestionOption.objects.create(text="whisky", question=question)
        some_date = date.today()
        answer = MultiChoiceAnswer.objects.create(question=question, country=country, response=option,
                                                  questionnaire=self.questionnaire)
        self.failUnless(answer.id)
        self.assertEqual(question, answer.question)
        self.assertEqual(country, answer.country)
        self.assertEqual(self.questionnaire, answer.questionnaire)
        self.assertEqual(option, answer.response)
        self.assertEqual(option, answer.format_response())

    def test_unicode(self):
        option_text = 'Yes'
        option = QuestionOptionFactory(text=option_text)
        answer = MultiChoiceAnswerFactory(response=option)

        self.assertEqual(option_text, str(answer))


class MultipleResponseAnswerTest(TestCase):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan")

    def test_multipleresponseanswer_fields(self):
        answer = MultipleResponseAnswer()

        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(10, len(fields))

        for field in ['id', 'created', 'modified', 'question_id', 'country_id', 'code',
                      'questionnaire_id']:
            self.assertIn(field, fields)

    def test_multi_response_answer_store(self):
        question = QuestionFactory()
        country = CountryFactory()
        option_1 = QuestionOptionFactory(question=question, text='No')
        option_2 = QuestionOptionFactory(question=question, text='Yes')
        answer = MultipleResponseAnswer.objects.create(question=question, country=country,
                                                       questionnaire=self.questionnaire)
        answer.response.add(option_1)
        answer.response.add(option_2)
        self.failUnless(answer.id)

        all_options = answer.response.all()
        [self.assertIn(option, [option_1, option_2]) for option in all_options]

    def test_unicode(self):
        yes_option_text = 'Yes'
        no_option_text = 'No'
        option_1 = QuestionOptionFactory(text=no_option_text)
        option_2 = QuestionOptionFactory(text=yes_option_text)
        answer = MultipleResponseAnswerFactory()

        answer.response.add(option_1)
        answer.response.add(option_2)

        self.assertEqual('%s, %s' % (no_option_text, yes_option_text), str(answer))
