import json

from django.test import Client

from questionnaire.tests.base_test import BaseTest
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.utils.answer_type import AnswerTypes


class QuestionAPITest(BaseTest):
    def setUp(self):
        self.client = Client()
        # self.user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        # self.assign('can_edit_questionnaire', self.user)
        # self.client.login(username=self.user.username, password='pass')

        self.url = '/api/v1/questions/'

        self.multichoice = QuestionFactory()
        self.numerical = QuestionFactory(answer_type=AnswerTypes.NUMBER)

    def test_list_questions(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        self.assertEqual(2, len(json_response))

        pks = [item['pk'] for item in json_response]
        self.assertIn(self.multichoice.id, pks)
        self.assertIn(self.numerical.id, pks)
