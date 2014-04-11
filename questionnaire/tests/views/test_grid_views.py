from urllib import quote
from questionnaire.forms.assign_question import AssignQuestionForm
from questionnaire.forms.grid import GridForm
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionOption
from questionnaire.tests.base_test import BaseTest
from django.test import Client


class CreateGridViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", region=self.region)

        self.section1 = Section.objects.create(title="Reported Cases of Selected Vaccine", order=1,
                                               questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="subsection 1", order=1, section=self.section1, region=self.region)
        self.sub_section2 = SubSection.objects.create(title="subsection 2", order=2, section=self.section1)

        self.question1 = Question.objects.create(text='Favorite beer 1', UID='C00001', answer_type='MultiChoice',
                                                 is_primary=True, region=self.region)
        self.option1 = QuestionOption.objects.create(text='tusker lager', question=self.question1)
        self.option2 = QuestionOption.objects.create(text='tusker lager1', question=self.question1)
        self.option3 = QuestionOption.objects.create(text='tusker lager2', question=self.question1)

        self.question2 = Question.objects.create(text='question 2', instructions="instruction 2",
                                                 UID='C00002', answer_type='Text', region=self.region)

        self.question3 = Question.objects.create(text='question 3', instructions="instruction 3",
                                                 UID='C00003', answer_type='Number', region=self.region)

        self.question4 = Question.objects.create(text='question 4', instructions="instruction 2",
                                                 UID='C00005', answer_type='Date', region=self.region)

        self.data ={
            'type': 'display_all',
            'primary_question':self.question1.id,
            'columns': [self.question2.id, self.question3.id]
        }

        self.url = '/subsection/%d/grid/new/' % self.sub_section.id

    def test_get_create_grid_page(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('questionnaires/grid/new.html')

    def test_gets_create_grid_form_and_subsection_in_context(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['grid_form'], GridForm)
        self.assertEqual('Create', response.context['btn_label'])
        self.assertEqual('create_grid_form', response.context['id'])
        self.assertEqual('create-grid-form', response.context['class'])
        self.assertEqual(self.sub_section, response.context['subsection'])
        questions = response.context['non_primary_questions'].values_list('id', flat=True)
        self.assertEqual(3, questions.count())
        self.assertIn(self.question2.id, questions)
        self.assertIn(self.question3.id, questions)
        self.assertIn(self.question4.id, questions)

    def test_post_creates_display_all_grid_group_and_orders_to_subsection(self):
        self.failIf(self.question1.question_group.all())
        self.failIf(self.question2.question_group.all())
        self.failIf(self.question3.question_group.all())

        meta = {'HTTP_REFERER': self.url}
        response = self.client.post(self.url, data=self.data, **meta)

        grid_group = self.question1.question_group.get(subsection=self.sub_section, grid=True, display_all=True, order=0)
        group_questions = grid_group.question.all()
        self.assertEqual(3, group_questions.count())
        self.assertIn(self.question2, group_questions)
        self.assertIn(self.question3, group_questions)

        group_orders = grid_group.orders.all()
        self.failUnless(group_orders)
        self.assertEqual(3, group_orders.count())
        self.assertEqual(1, group_orders.filter(question=self.question1, order=0).count())
        self.assertEqual(1, group_orders.filter(question=self.question2, order=1).count())
        self.assertEqual(1, group_orders.filter(question=self.question3, order=2).count())

    def test_post_creates_add_more_grid_group_and_orders_to_subsection(self):
        self.failIf(self.question1.question_group.all())
        self.failIf(self.question2.question_group.all())
        self.failIf(self.question3.question_group.all())
        self.data ={
            'type': 'allow_multiples',
            'primary_question': str(self.question1.id),
            'columns': [str(self.question2.id), str(self.question3.id)]
        }

        meta = {'HTTP_REFERER': self.url}
        response = self.client.post(self.url, data=self.data, **meta)

        grid_group = self.question1.question_group.get(subsection=self.sub_section, grid=True, allow_multiples=True, order=0)
        group_questions = grid_group.question.all()
        self.assertEqual(3, group_questions.count())
        self.assertIn(self.question2, group_questions)
        self.assertIn(self.question3, group_questions)

        group_orders = grid_group.orders.all()
        self.failUnless(group_orders)
        self.assertEqual(3, group_orders.count())
        self.assertEqual(1, group_orders.filter(question=self.question1, order=0).count())
        self.assertEqual(1, group_orders.filter(question=self.question2, order=1).count())
        self.assertEqual(1, group_orders.filter(question=self.question3, order=2).count())

    def test_post_creates_hybrid_grid_group_and_orders_to_subsection(self):
        self.question5 = Question.objects.create(text='question 5', instructions="instruction 5",
                                                 UID='C00006', answer_type='MultiChoice', region=self.region)

        self.failIf(self.question1.question_group.all())
        self.failIf(self.question2.question_group.all())
        self.failIf(self.question3.question_group.all())
        self.failIf(self.question4.question_group.all())
        self.failIf(self.question5.question_group.all())

        self.data ={
            'type': 'hybrid',
            'primary_question': str(self.question1.id),
            'columns': [str(self.question2.id), str(self.question4.id), str(self.question5.id), str(self.question3.id)],
            'subgroup': [str(self.question4.id), str(self.question5.id)]
        }

        meta = {'HTTP_REFERER': self.url}
        response = self.client.post(self.url, data=self.data, **meta)

        parent_grid_group = self.question1.question_group.get(subsection=self.sub_section, grid=True,
                                                       allow_multiples=True, order=0, hybrid=True)
        group_questions = parent_grid_group.question.all()
        self.assertEqual(3, group_questions.count())
        self.assertIn(self.question2, group_questions)
        self.assertIn(self.question3, group_questions)

        grid_sub_group = self.question4.question_group.get(subsection=self.sub_section, parent=parent_grid_group, grid=True)
        group_questions = grid_sub_group.question.all()
        self.assertEqual(2, group_questions.count())
        self.assertIn(self.question4, group_questions)
        self.assertIn(self.question5, group_questions)

        group_orders = parent_grid_group.orders.all()
        self.failUnless(group_orders)
        self.assertEqual(5, group_orders.count())
        self.assertEqual(1, group_orders.filter(question=self.question1, order=0).count())
        self.assertEqual(1, group_orders.filter(question=self.question2, order=1).count())
        self.assertEqual(1, group_orders.filter(question=self.question4, order=2).count())
        self.assertEqual(1, group_orders.filter(question=self.question5, order=3).count())
        self.assertEqual(1, group_orders.filter(question=self.question3, order=4).count())

    def test_successful_post_redirect_to_referer_url(self):
        meta = {'HTTP_REFERER': self.url}
        response = self.client.post(self.url, data=self.data, **meta)
        self.assertRedirects(response, self.url)

    def test_successful_post_display_success_message(self):
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section1.id)
        meta = {'HTTP_REFERER': referer_url}
        response = self.client.post(self.url, data=self.data, **meta)
        message = "Grid successfully created."
        self.assertIn(message, response.cookies['messages'].value)

    def test_with_errors_returns_the_form_with_error(self):
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section1.id)
        meta = {'HTTP_REFERER': referer_url}
        data = self.data.copy()
        data['type']=''
        response = self.client.post(self.url, data=data, **meta)

        self.assertIsInstance(response.context['grid_form'], GridForm)
        self.assertIn("This field is required.", response.context['grid_form'].errors['type'])
        self.assertEqual('Create', response.context['btn_label'])
        self.assertEqual('create_grid_form', response.context['id'])
        self.assertEqual('create-grid-form', response.context['class'])
        self.assertEqual(self.sub_section, response.context['subsection'])
        questions = response.context['non_primary_questions'].values_list('id', flat=True)
        self.assertEqual(3, questions.count())
        self.assertIn(self.question2.id, questions)
        self.assertIn(self.question3.id, questions)
        self.assertIn(self.question4.id, questions)

    def test_login_required(self):
        self.assert_login_required(self.url)

    def test_permission_required_for_create_section(self):
        self.assert_permission_required(self.url)

        user_not_in_same_region, country, region = self.create_user_with_no_permissions(username="asian_chic",
                                                                                        country_name="China",
                                                                                        region_name="ASEAN")
        self.assign('can_edit_questionnaire', user_not_in_same_region)

        self.client.logout()
        self.client.login(username='asian_chic', password='pass')
        response = self.client.get(self.url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(self.url))
        response = self.client.post(self.url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(self.url))
