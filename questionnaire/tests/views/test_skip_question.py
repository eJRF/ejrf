from questionnaire.tests.base_test import BaseTest
from django.test import Client
import logging
from questionnaire.models import Question, SkipQuestion

class SkipQuestionTest(BaseTest):

	def setUp(self):
		self.client = Client()
		self.url ="/questionnaire/subsection/1/skiprules/"
		region = None
		question1 = Question.objects.create(text='Q1', UID='C00003', answer_type='Number', region=region)
		self.form_data = {'root-question': question1.pk,
						  'responses': '1',
						  'skip-question': '2'}
		


	def test_post_skip_question(self):
		self.assertEqual(SkipQuestion.objects.all().count(), 0)
		response = self.client.post(self.url, data=self.form_data)
		self.assertEqual(201, response.status_code)
		self.assertEqual(SkipQuestion.objects.all().count(), 1)
