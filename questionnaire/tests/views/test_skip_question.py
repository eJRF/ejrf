from questionnaire.tests.base_test import BaseTest
from django.test import Client
import logging
from questionnaire.models import Question, SkipQuestion, QuestionOption, Questionnaire, Section, SubSection, QuestionGroup

class SkipQuestionTest(BaseTest):

	def setUp(self):
		self.client = Client()
		self.url = "/questionnaire/subsection/%d/skiprules/"
		region = None

		questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=region)

		section = Section.objects.create(name="section", questionnaire=questionnaire, order=1)

		subsection = SubSection.objects.create(title="subsection 1", section=section, order=1)
		subsection2 = SubSection.objects.create(title="subsection 2", section=section, order=1)
		self.subsection_id = subsection.pk
		self.empty_subsection_id = subsection2.pk
		question_group = QuestionGroup.objects.create(subsection_id=subsection.id)

		question1 = Question.objects.create(text='Q1', UID='C00003', answer_type='MultiChoice', region=region)
		question2 = Question.objects.create(text='Q2', UID='C00004', answer_type='Number', region=region)
		
		question_group.question.add(question1)
		question_group.question.add(question2)

		response = QuestionOption.objects.create(text = "Some response", question=question1, UID = "U0003")
		self.form_data = {'root-question': question1.pk,
						  'responses': response.pk,
						  'skip-question': question2.pk}

	def test_post_skip_question(self):
		self.assertEqual(SkipQuestion.objects.all().count(), 0)
		response = self.client.post(self.url % self.subsection_id, data=self.form_data)
		self.assertEqual(201, response.status_code)
		self.assertEqual(SkipQuestion.objects.all().count(), 1)

	def test_post_skip_question_for_root_question_not_existing(self):
		data = self.form_data
		data['root-question'] = 341543
		response = self.client.post(self.url % self.subsection_id, data=data)
		self.assertEqual(400, response.status_code)

	def test_post_skip_question_for_response_not_existing(self):
		data = self.form_data
		data['responses'] = 341543
		response = self.client.post(self.url % self.subsection_id, data=data)
		self.assertEqual(400, response.status_code)

	def test_post_skip_question_for_skip_question_not_existing(self):
		data = self.form_data
		data['skip-question'] = 341543
		response = self.client.post(self.url % self.subsection_id, data=data)
		self.assertEqual(400, response.status_code)

	def test_post_skip_question_for_questions_not_being_part_of_subsection(self):
		response = self.client.post(self.url % self.empty_subsection_id, data=self.form_data)
		self.assertEqual(400, response.status_code)