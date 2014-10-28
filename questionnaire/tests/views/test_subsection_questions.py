import json
from django.core.urlresolvers import reverse
from django.test import Client
from questionnaire.tests.base_test import BaseTest
from questionnaire.models import Section, SubSection, Questionnaire, Question, QuestionGroup
from django.core import serializers


class SubsectionQuestionsTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.region = None
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)

        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1)

        self.subsection = SubSection.objects.create(title="subsection 1", section=self.section, order=1, pk=1)

        self.question_group = QuestionGroup.objects.create(subsection_id=self.subsection.id)
        self.question_group2 = QuestionGroup.objects.create(subsection_id=self.subsection.id)

        self.question1 = Question.objects.create(text='Q1', UID='C00003', answer_type='Number', region=self.region)
        self.question2 = Question.objects.create(text='Q2', UID='C00002', answer_type='Number', region=self.region)
        self.question3 = Question.objects.create(text='Q3', UID='C00004', answer_type='Number', region=self.region)

        self.question_group.question.add(self.question1)
        self.question_group.question.add(self.question2)

    def test_should_get_back_questionnaire_id_from_url(self):

        response = self.client.get('/questionnaire/subsection/1/questions/')
        self.assertEqual(200, response.status_code)

        q1 = self.obj_to_dict(self.question1)
        q1['options'] = []
        
        q2 = self.obj_to_dict(self.question2)
        q2['options'] = []

        actualResponse = json.loads(response.content)['questions']
        self.assertTrue(q1 in actualResponse)
        self.assertTrue(q2 in actualResponse)


    def obj_to_dict(self, question):
        return json.loads(serializers.serialize('json', [question]))[0]

    def test_should_get_back_questionnaire_id_from_url_when_there_are_two_question_groups(self):
        self.question_group2.question.add(self.question3)
        response = self.client.get('/questionnaire/subsection/1/questions/')
        self.assertEqual(200, response.status_code)

        q3 = self.obj_to_dict(self.question3)
        q3['options'] = []

        q1 = self.obj_to_dict(self.question1)
        q1['options'] = []
        
        q2 = self.obj_to_dict(self.question2)
        q2['options'] = []

        actualResponse = json.loads(response.content)['questions']
        self.assertTrue(q1 in actualResponse)
        self.assertTrue(q2 in actualResponse)
        self.assertTrue(q3 in actualResponse)      