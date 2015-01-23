import json
from urllib import quote

from django.test import Client

from questionnaire.tests.base_test import BaseTest
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.question_group_factory import QuestionGroupFactory
from questionnaire.tests.factories.region_factory import RegionFactory
from questionnaire.utils.answer_type import AnswerTypes


class QuestionAPITest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.url = '/api/v1/questions/'

        self.multichoice = QuestionFactory()
        self.numerical = QuestionFactory(answer_type=AnswerTypes.NUMBER)
        self.regional_numerical = QuestionFactory(answer_type=AnswerTypes.NUMBER, region=RegionFactory())

    def test_list_questions(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        self.assertEqual(2, len(json_response))

        pks = [item['pk'] for item in json_response]
        self.assertIn(self.multichoice.id, pks)
        self.assertIn(self.numerical.id, pks)

    def test_list_all_multichoice_questions(self):
        response = self.client.get(self.url + '?answer_type=multichoice')
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        self.assertEqual(1, len(json_response))

        self.assertEqual(self.multichoice.id, json_response[0]['pk'])

    def test_list_all_unused_questions_given_questionnaire(self):
        question_group = QuestionGroupFactory()
        question_in_questionnaire = QuestionFactory()
        question_group.question.add(question_in_questionnaire)
        questionnaire = question_group.subsection.section.questionnaire

        response = self.client.get(self.url + '?questionnaire=%s&unused=true' % questionnaire.id)
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        self.assertEqual(2, len(json_response))

        pks = [item['pk'] for item in json_response]
        self.assertIn(self.multichoice.id, pks)
        self.assertIn(self.numerical.id, pks)
        self.assertNotIn(question_in_questionnaire.id, pks)

    def test_permission_required_for_create_section(self):
        self.assert_permission_required(self.url)