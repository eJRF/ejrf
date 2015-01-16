import json
from django.test import Client
from questionnaire.tests.base_test import BaseTest
from questionnaire.models.questionnaires import Questionnaire
from questionnaire.tests.factories.answer_factory import NumericalAnswerFactory

from questionnaire.tests.factories.questionnaire_factory import QuestionnaireFactory


class ValidateQuestionnaireFieldsTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.questionnaire = QuestionnaireFactory(name="Some questionnaire", status=Questionnaire.PUBLISHED, year=2015)
        self.url = '/questionnaire/validate/'

    def test_year_available_when_no_questionnaire_exists_for_that_year(self):
        un_used_year = 2020
        response = self.client.get(self.url + '?year=%s' % un_used_year)
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        expected_response = {'status': '', 'message': ''}
        self.assertEqual(json_response, expected_response)

    def test_year_available_when_questionnaire_has_no_answers(self):
        response = self.client.get(self.url + '?year=2015')
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        expected_response = {'status': 'alert-warning',
                             'message': 'A Revision of the year 2015 already exists. If you go ahead, that revision will be archived.'}
        self.assertEqual(json_response, expected_response)

    def test_year_not_available(self):
        year = 2015
        child_questionnaire = QuestionnaireFactory(name="Some questionnaire",
                                                   status=Questionnaire.PUBLISHED,
                                                   year=year,
                                                   parent=self.questionnaire)

        NumericalAnswerFactory(questionnaire=child_questionnaire)
        expected_response = {'status': 'alert-danger', 'message': 'Questionnaire has responses.'}

        response = self.client.get(self.url + '?year=2015')
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        self.assertEqual(json_response, expected_response)