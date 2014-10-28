from questionnaire.tests.base_test import BaseTest
from django.test import Client
import logging

class SkipQuestionTest(BaseTest):

	def setUp(self):
		self.client = Client()
		self.url ="/questionnaire/subsection/1/skiprules/"
		self.form_data = {'root-question': '1',
						  'responses': '1',
						  'skip-question': '2'}


	def test_post_skip_question(self):
		response = self.client.post(self.url, data=self.form_data)
		logging.warning(response)
		self.assertEqual(200, response.status_code)