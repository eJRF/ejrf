from questionnaire.tests.base_test import BaseTest
from django.test import Client
import logging
from questionnaire.models import Question, SkipQuestion, QuestionOption, Questionnaire, Section, SubSection, QuestionGroup
import json

class SkipQuestionTest(BaseTest):

	def setUp(self):
		self.client = Client()
		self.url = "/questionnaire/subsection/%d/skiprules/"
		region = None

		questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=region)

		section = Section.objects.create(name="section", questionnaire=questionnaire, order=1)

		subsection = SubSection.objects.create(title="subsection 1", section=section, order=1)
		subsection2 = SubSection.objects.create(title="subsection 2", section=section, order=1)		
		subsection3 = SubSection.objects.create(title="subsection 2", section=section, order=1)
		self.subsection_id = subsection.pk
		question_group = QuestionGroup.objects.create(subsection_id=subsection.id)	

		root_question = Question.objects.create(text='Q1', UID='C00003', answer_type='MultiChoice', region=region)
		skip_question = Question.objects.create(text='Q2', UID='C00004', answer_type='Number', region=region)
		self.random_question = Question.objects.create(text='Q3', UID='C00005', answer_type='Number', region=region)
		
		question_group.question.add(root_question)
		question_group.question.add(skip_question)
		question_group.question.add(self.random_question)

		self.subsection_with_only_root_question = subsection3.pk
		question_group2 = QuestionGroup.objects.create(subsection_id=self.subsection_with_only_root_question)
		question_group2.question.add(root_question)

		self.subsection_with_only_skip_question = subsection2.pk
		question_group3 = QuestionGroup.objects.create(subsection_id=self.subsection_with_only_skip_question)	
		question_group3.question.add(skip_question)

		response = QuestionOption.objects.create(text = "Some response", question=root_question, UID = "U0003")
		self.form_data = {'root-question': root_question.pk,
						  'responses': response.pk,
						  'skip-question': skip_question.pk}

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
		self.assertEqual(json.loads(response.content)['result'], 'root-question does not exist')

	def test_post_skip_question_for_response_not_existing(self):
		data = self.form_data
		data['responses'] = 341543
		response = self.client.post(self.url % self.subsection_id, data=data)
		self.assertEqual(400, response.status_code)
		self.assertEqual(json.loads(response.content)['result'], 'response does not exist')

	def test_post_skip_question_for_skip_question_not_existing(self):
		data = self.form_data
		data['skip-question'] = 341543
		response = self.client.post(self.url % self.subsection_id, data=data)
		self.assertEqual(400, response.status_code)
		self.assertEqual(json.loads(response.content)['result'], 'skip-question does not exist')

	def test_post_skip_question_for_root_question_not_being_part_of_subsection(self):
		response = self.client.post(self.url % self.subsection_with_only_skip_question, data=self.form_data)
		self.assertEqual(400, response.status_code)
		self.assertEqual(json.loads(response.content)['result'], 'root-question is not part of subsection')

	def test_post_skip_question_for_skip_question_not_being_part_of_subsection(self):
		response = self.client.post(self.url % self.subsection_with_only_root_question, data=self.form_data)
		self.assertEqual(400, response.status_code)
		self.assertEqual(json.loads(response.content)['result'], 'skip-question is not part of subsection')

	def test_post_skip_question_for_response_option_not_being_related_to_root_question(self):
		data = self.form_data
		data['root-question'] = self.random_question.pk
		response = self.client.post(self.url % self.subsection_id, data=data)
		self.assertEqual(400, response.status_code)
		self.assertEqual(json.loads(response.content)['result'], "root question's options does not contain the provided response")


	# def test_post_response_for_root_question(self):
	# 	question3 = Question.objects.create(text='Q3', UID='C00005', answer_type='MultiChoice', region=region)
	# 	