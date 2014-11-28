import json

from django.test import Client
from django.core import serializers

from questionnaire.tests.base_test import BaseTest
from questionnaire.models import Section, SubSection, Questionnaire, Question, QuestionGroup
from questionnaire.tests.factories.region_factory import RegionFactory


class SubsectionQuestionsTest(BaseTest):
    def setUp(self):
        self.client = Client()
        user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.regional_admin = self.create_user(group=self.REGIONAL_ADMIN, org="WHO", username="ra",
                                               region=RegionFactory())

        self.assign('can_view_questionnaire', user)
        self.assign('can_view_questionnaire', self.regional_admin)
        self.client.login(username=user.username, password='pass')

        self.region = None
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)

        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1)

        self.subsection = SubSection.objects.create(title="subsection 1", section=self.section, order=1, pk=1)

        self.question_group = QuestionGroup.objects.create(subsection_id=self.subsection.id, grid=False)
        self.question_group2 = QuestionGroup.objects.create(subsection_id=self.subsection.id, grid=False)

        self.question1 = Question.objects.create(text='Q1', UID='C00003', answer_type='Number', region=self.region)
        self.question2 = Question.objects.create(text='Q2', UID='C00002', answer_type='Number', region=self.region)
        self.question3 = Question.objects.create(text='Q3', UID='C00004', answer_type='Number',
                                                 region=self.regional_admin.user_profile.region)

        self.question_group.question.add(self.question1)
        self.question_group.question.add(self.question2)

    def test_should_get_back_questionnaire_id_from_url(self):
        response = self.client.get('/questionnaire/subsection/1/questions/')
        self.assertEqual(200, response.status_code)

        q1 = self.obj_to_dict(self.question1)
        q1['options'] = []
        q1['parentQuestionGroup'] = self.question_group.id
        q1['canSkip'] = True

        q2 = self.obj_to_dict(self.question2)
        q2['options'] = []
        q2['parentQuestionGroup'] = self.question_group.id
        q2['canSkip'] = True

        actual_response = json.loads(response.content)['questions']
        print q1
        print actual_response
        self.assertTrue(q1 in actual_response)
        self.assertTrue(q2 in actual_response)

    def obj_to_dict(self, question):
        return json.loads(serializers.serialize('json', [question]))[0]

    def test_should_get_back_questionnaire_id_from_url_when_there_are_two_question_groups(self):
        self.question_group2.question.add(self.question3)
        response = self.client.get('/questionnaire/subsection/1/questions/')
        self.assertEqual(200, response.status_code)

        q3 = self.obj_to_dict(self.question3)
        q3['options'] = []
        q3['parentQuestionGroup'] = self.question_group2.id
        q3['canSkip'] = True

        q1 = self.obj_to_dict(self.question1)
        q1['options'] = []
        q1['parentQuestionGroup'] = self.question_group.id
        q1['canSkip'] = True

        q2 = self.obj_to_dict(self.question2)
        q2['options'] = []
        q2['parentQuestionGroup'] = self.question_group.id
        q2['canSkip'] = True

        actual_response = json.loads(response.content)['questions']
        self.assertTrue(q1 in actual_response)
        self.assertTrue(q2 in actual_response)
        self.assertTrue(q3 in actual_response)

    def test_should_get_back_questionnaire_id_from_url_when_there_are_two_question_groups_as_regional_admin(self):
        self.client.login(username=self.regional_admin.username, password='pass')
        self.question_group2.question.add(self.question3)
        response = self.client.get('/questionnaire/subsection/1/questions/')
        self.assertEqual(200, response.status_code)

        q3 = self.obj_to_dict(self.question3)
        q3['options'] = []
        q3['parentQuestionGroup'] = self.question_group2.id
        q3['canSkip'] = True

        q1 = self.obj_to_dict(self.question1)
        q1['options'] = []
        q1['parentQuestionGroup'] = self.question_group.id
        q1['canSkip'] = False

        q2 = self.obj_to_dict(self.question2)
        q2['options'] = []
        q2['parentQuestionGroup'] = self.question_group.id
        q2['canSkip'] = False

        actual_response = json.loads(response.content)['questions']
        self.assertTrue(q1 in actual_response)
        self.assertTrue(q2 in actual_response)
        self.assertTrue(q3 in actual_response)