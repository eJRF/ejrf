import json
from django.core.urlresolvers import reverse
from django.test import Client
from questionnaire.tests.base_test import BaseTest
from questionnaire.models import Section, SubSection, Questionnaire, Question, QuestionGroup
from django.core import serializers


class SubsectionQuestionsTest(BaseTest):

    def setUp(self):
        self.region = None
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)
        self.questionnaire.save()
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1)
        self.section.save()
        self.subsection = SubSection.objects.create(title="subsection 1", section=self.section, order=1, pk=1)
        self.subsection.save()
        self.question_group = QuestionGroup.objects.create(subsection_id=self.subsection.id)
        self.question1 = Question.objects.create(text='Q1', UID='C00003', answer_type='Number', region=self.region)
        self.question1.save()
        self.question2 = Question.objects.create(text='Q2', UID='C00002', answer_type='Number', region=self.region)
        self.question2.save()
        self.question_group.question.add(self.question1)
        self.question_group.question.add(self.question2)
        self.question_group.save()


    def test_should_get_back_questionnaire_id_from_url(self):
        response = self.client.get('/questionnaire/1/section/1/subsection/1/questions/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(json.loads(response.content)['questions'], serializers.serialize("json", [self.question1, self.question2]))
