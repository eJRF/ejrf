from questionnaire.tests.base_test import BaseTest
from django.test import Client
import logging
from questionnaire.models import Question, SkipQuestion

class SkipQuestionTest(BaseTest):

	def setUp(self):
		self.client = Client()
		self.url ="/questionnaire/subsection/1/skiprules/"
		self.form_data = {'root-question': '1',
						  'responses': '1',
						  'skip-question': '2'}


	def test_post_skip_question(self):
		self.assertEqual(SkipQuestion.objects.all().count(), 0)
		response = self.client.post(self.url, data=self.form_data)
		self.assertEqual(201, response.status_code)
