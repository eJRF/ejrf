import json

from django.test import Client

from questionnaire.tests.base_test import BaseTest
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.theme_factory import ThemeFactory
from questionnaire.utils.answer_type import AnswerTypes


class ThemesAPITest(BaseTest):
    def setUp(self):
        self.client = Client()
        # self.user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        # self.assign('can_edit_questionnaire', self.user)
        # self.client.login(username=self.user.username, password='pass')

        self.url = '/api/v1/themes/'
        self.theme1 = ThemeFactory()
        self.theme2 = ThemeFactory()

    def test_list_themes(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        self.assertEqual(2, len(json_response))

        pks = [item['pk'] for item in json_response]
        self.assertIn(self.theme1.id, pks)
        self.assertIn(self.theme2.id, pks)
