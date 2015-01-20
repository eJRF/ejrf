import json

from django.test import Client

from questionnaire.tests.base_test import BaseTest
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.question_option_factory import QuestionOptionFactory


class ThemesAPITest(BaseTest):
    def setUp(self):
        self.client = Client()
        # self.user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        # self.assign('can_edit_questionnaire', self.user)
        # self.client.login(username=self.user.username, password='pass')

        self.question = QuestionFactory()
        self.question_option1 = QuestionOptionFactory(question=self.question)
        self.question_option2 = QuestionOptionFactory(question=self.question)
        self.question_option3 = QuestionOptionFactory(question=self.question)
        self.url = '/api/v1/question/%s/options/' % self.question.id

    def test_list_themes(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        self.assertEqual(3, len(json_response))

        pks = [item['pk'] for item in json_response]
        self.assertIn(self.question_option1.id, pks)
        self.assertIn(self.question_option2.id, pks)
        self.assertIn(self.question_option3.id, pks)