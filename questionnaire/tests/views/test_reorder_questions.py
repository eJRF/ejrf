from django.test import Client

from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionOption, \
    QuestionGroupOrder
from questionnaire.tests.base_test import BaseTest


class ReorderSubsectionQuestionsViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.region = None
        self.user = self.assign('can_view_users', self.user)
        self.user = self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.PUBLISHED,
                                                          description="From dropbox as given by Rouslan",
                                                          region=self.region)

        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                                order=1,
                                                questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                     section=self.section_1)

        self.question1 = Question.objects.create(text='Disease', UID='C00001', answer_type='MultiChoice')
        self.question2 = Question.objects.create(text='B. Number of cases tested',
                                                 instructions="Enter the total number of cases for which specimens were collected, and tested in laboratory",
                                                 UID='C00003', answer_type='Number')

        self.question3 = Question.objects.create(text='C. Number of cases positive',
                                                 instructions="Include only those cases found positive for the infectious agent.",
                                                 UID='C00004', answer_type='Number')

        self.option1 = QuestionOption.objects.create(text='tusker lager', question=self.question1)
        self.option2 = QuestionOption.objects.create(text='tusker lager1', question=self.question1)
        self.option3 = QuestionOption.objects.create(text='tusker lager2', question=self.question1)

        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1)
        self.question_group.question.add(self.question1, self.question3, self.question2)

        self.order1 = QuestionGroupOrder.objects.create(question_group=self.question_group, question=self.question1,
                                                        order=1)
        self.order2 = QuestionGroupOrder.objects.create(question_group=self.question_group, question=self.question2,
                                                        order=2)
        self.order3 = QuestionGroupOrder.objects.create(question_group=self.question_group, question=self.question3,
                                                        order=3)
        self.url = '/subsection/%d/reorder/' % self.sub_section.id

    def test_reorder_questions_in_group(self):
        data = {'Number-0-response-order': [u"%d,%d, 0" % (self.question_group.id, self.order3.id)],
                'Text-1-response-order': [u"%d,%d, 1" % (self.question_group.id, self.order2.id)],
                'Text-0-response-order': [u"%d,%d, 2" % (self.question_group.id, self.order1.id)]}
        response = self.client.post(self.url, data=data)
        self.assertRedirects(response, expected_url=self.sub_section.get_absolute_url())
        updated_orders = self.question_group.question_orders()
        self.assertEqual(3, updated_orders.count())
        self.assertEqual(self.order1, updated_orders.get(order=3))
        self.assertEqual(self.order2, updated_orders.get(order=2))
        self.assertEqual(self.order3, updated_orders.get(order=1))

    def test_permissions_required(self):
        self.assert_login_required(self.url)
        self.assert_permission_required(self.url)


class RegionalAdminReorderSubsectionQuestionsViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.REGIONAL_ADMIN, org="WHO", region="AFRO")
        self.region = self.user.user_profile.region
        self.user = self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.PUBLISHED,
                                                          description="From dropbox as given by Rouslan",
                                                          region=self.region)

        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                                order=1,
                                                questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                     section=self.section_1)

        self.question1 = Question.objects.create(text='Disease', UID='C00001', answer_type='MultiChoice')
        self.question2 = Question.objects.create(text='B. Number of cases tested',
                                                 instructions="Enter the total number of cases for which specimens were collected, and tested in laboratory",
                                                 UID='C00003', answer_type='Number')

        self.question3 = Question.objects.create(text='C. Number of cases positive',
                                                 instructions="Include only those cases found positive for the infectious agent.",
                                                 UID='C00004', answer_type='Number')

        self.option1 = QuestionOption.objects.create(text='tusker lager', question=self.question1)
        self.option2 = QuestionOption.objects.create(text='tusker lager1', question=self.question1)
        self.option3 = QuestionOption.objects.create(text='tusker lager2', question=self.question1)

        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1)
        self.question_group.question.add(self.question1, self.question3, self.question2)

        self.order1 = QuestionGroupOrder.objects.create(question_group=self.question_group, question=self.question1,
                                                        order=1)
        self.order2 = QuestionGroupOrder.objects.create(question_group=self.question_group, question=self.question2,
                                                        order=2)
        self.order3 = QuestionGroupOrder.objects.create(question_group=self.question_group, question=self.question3,
                                                        order=3)

    def test_reorder_questions_in_group(self):
        data = {'Number-0-response-order': [u"%d,%d, 0" % (self.question_group.id, self.order3.id)],
                'Text-1-response-order': [u"%d,%d, 1" % (self.question_group.id, self.order2.id)],
                'Text-0-response-order': [u"%d,%d, 2" % (self.question_group.id, self.order1.id)]}
        response = self.client.post('/subsection/%d/reorder/' % self.sub_section.id, data=data)
        self.assertRedirects(response, expected_url=self.sub_section.get_absolute_url())
        updated_orders = self.question_group.question_orders()
        self.assertEqual(3, updated_orders.count())
        self.assertEqual(self.order1, updated_orders.get(order=3))
        self.assertEqual(self.order2, updated_orders.get(order=2))
        self.assertEqual(self.order3, updated_orders.get(order=1))
