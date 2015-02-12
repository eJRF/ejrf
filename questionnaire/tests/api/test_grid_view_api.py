import json

from django.test import Client
from questionnaire.models import QuestionGroupOrder, QuestionGroup

from questionnaire.tests.base_test import BaseTest
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.question_group_factory import QuestionGroupFactory
from questionnaire.tests.factories.sub_section_factory import SubSectionFactory
from questionnaire.tests.factories.theme_factory import ThemeFactory
from questionnaire.utils.answer_type import AnswerTypes


class GridAPIViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.theme1 = ThemeFactory()
        self.subsection = SubSectionFactory()
        self.grid_question_group = QuestionGroupFactory(grid=True, allow_multiples=True,
                                                        subsection=self.subsection)
        self.url = '/api/v1/grids/%s/' % self.grid_question_group.id

        self.primary_question = QuestionFactory(is_primary=True, text='Some primary question',
                                                answer_type=AnswerTypes.MULTI_CHOICE, theme=self.theme1)
        self.column_1_question = QuestionFactory(text='Question 1', answer_type=AnswerTypes.DATE, theme=self.theme1)
        self.column_2_question = QuestionFactory(text='Question 2', answer_type=AnswerTypes.TEXT, theme=self.theme1)
        self.column_3_question = QuestionFactory(text='Question 3', answer_type=AnswerTypes.TEXT, theme=self.theme1)
        QuestionGroupOrder.objects.create(question=self.primary_question, order=1,
                                          question_group=self.grid_question_group)
        QuestionGroupOrder.objects.create(question=self.column_1_question, order=2,
                                          question_group=self.grid_question_group)
        QuestionGroupOrder.objects.create(question=self.column_2_question, order=3,
                                          question_group=self.grid_question_group)
        QuestionGroupOrder.objects.create(question=self.column_3_question, order=4,
                                          question_group=self.grid_question_group)

    def test_get_grid(self):
        self.grid_question_group.question.add(self.column_1_question, self.column_2_question, self.column_3_question)

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        json_response = json.loads(response.content)
        self.assertEqual(1, len(json_response))

        response_data = json_response[0]
        self.assertEqual(self.grid_question_group.pk, response_data['pk'])
        self.assertEqual(self.subsection.id, response_data['fields']['subsection'])
        self.assertTrue(response_data['fields']['allow_multiples'])

        self.assertIn(self.column_1_question.pk, response_data['fields']['question'])
        self.assertIn(self.column_2_question.pk, response_data['fields']['question'])
        self.assertIn(self.column_3_question.pk, response_data['fields']['question'])

    def test_get_grid_with_sub_groups(self):
        self.grid_question_group.question.add(self.column_1_question, self.column_2_question, self.column_3_question)

        child_group = QuestionGroupFactory(grid=True,
                                           allow_multiples=False,
                                           subsection=self.subsection,
                                           parent=self.grid_question_group)

        child_2_question = QuestionFactory(text='Question 4',
                                           answer_type=AnswerTypes.TEXT,
                                           theme=self.theme1)

        child_3_question = QuestionFactory(text='Question 5',
                                           answer_type=AnswerTypes.TEXT,
                                           theme=self.theme1)

        child_group.question.add(child_2_question, child_3_question)

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

        json_response = json.loads(response.content)[0]['children']

        children_data = json.loads(json_response)
        self.assertEqual(1, len(children_data))

        self.assertEqual(child_group.pk, children_data[0]['pk'])
        self.assertEqual(self.subsection.id, children_data[0]['fields']['subsection'])

        self.assertIn(child_2_question.pk, children_data[0]['fields']['question'])
        self.assertIn(child_3_question.pk, children_data[0]['fields']['question'])

    def test_permission_required_for_create_section(self):
        self.assert_permission_required(self.url)

    def test_update_grid_details(self):
        column_4_question = QuestionFactory(text='Question 5',
                                            answer_type=AnswerTypes.TEXT,
                                            theme=self.theme1)
        grid_form = {
            'primary_question': self.primary_question.id,
            'columns': [self.column_1_question.id, self.column_3_question.id, self.column_2_question.id,
                        column_4_question.id],
            'type': 'display_all'
        }

        response = self.client.post(self.url, data=grid_form)
        self.assertEqual(200, response.status_code)

        group = QuestionGroup.objects.get(id=self.grid_question_group.id)
        ordered_questions = group.ordered_questions()

        self.assertEqual(5, len(ordered_questions))
        self.assertEqual(self.primary_question, ordered_questions[0])
        self.assertEqual(self.column_1_question, ordered_questions[1])
        self.assertEqual(self.column_3_question, ordered_questions[2])
        self.assertEqual(self.column_2_question, ordered_questions[3])
        self.assertEqual(column_4_question, ordered_questions[4])

        response_data = json.loads(response.content)[0]
        self.assertEqual(response_data['message'], 'The grid was updated successfully.')

    def test_returns_json_errors_with_errors(self):
        non_existing_question = 23
        empty_type = ''
        grid_form = {
            'primary_question': non_existing_question,
            'columns': [self.column_1_question.id, self.column_3_question.id, self.column_2_question.id,
                        non_existing_question],
            'type': empty_type
        }

        response = self.client.post(self.url, data=grid_form)
        self.assertEqual(400, response.status_code)

        group = QuestionGroup.objects.get(id=self.grid_question_group.id)
        ordered_questions = group.ordered_questions()

        self.assertEqual(4, len(ordered_questions))
        self.assertEqual(self.primary_question, ordered_questions[0])
        self.assertEqual(self.column_1_question, ordered_questions[1])
        self.assertEqual(self.column_2_question, ordered_questions[2])
        self.assertEqual(self.column_3_question, ordered_questions[3])

        response_data = json.loads(response.content)[0]

        self.assertEqual(response_data['error'], 'The grid could not be updated.')
        required_error = 'This field is required.'
        primary_invalid_choices = 'Select a valid choice. That choice is not one of the available choices.'
        column_invalid_choices = 'Select a valid choice. %d is not one of the available choices.' % non_existing_question
        self.assertEqual([required_error], response_data['form_errors']['type'])
        self.assertEqual([primary_invalid_choices], response_data['form_errors']['primary_question'])
        self.assertEqual([column_invalid_choices], response_data['form_errors']['columns'])


class GridQuestionOrdersAPIViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.theme1 = ThemeFactory()
        self.subsection = SubSectionFactory()
        self.grid_question_group = QuestionGroupFactory(grid=True, allow_multiples=True,
                                                        subsection=self.subsection)
        self.url = '/api/v1/grids/%s/orders/' % self.grid_question_group.id

        self.primary_question = QuestionFactory(is_primary=True, text='Some primary question',
                                                answer_type=AnswerTypes.MULTI_CHOICE, theme=self.theme1)
        self.column_1_question = QuestionFactory(text='Question 1', answer_type=AnswerTypes.DATE, theme=self.theme1)
        self.column_2_question = QuestionFactory(text='Question 2', answer_type=AnswerTypes.TEXT, theme=self.theme1)
        self.column_3_question = QuestionFactory(text='Question 3', answer_type=AnswerTypes.TEXT, theme=self.theme1)
        self.order_1 = QuestionGroupOrder.objects.create(question=self.primary_question, order=1,
                                                         question_group=self.grid_question_group)
        self.order_2 = QuestionGroupOrder.objects.create(question=self.column_1_question, order=2,
                                                         question_group=self.grid_question_group)
        self.order_3 = QuestionGroupOrder.objects.create(question=self.column_2_question, order=3,
                                                         question_group=self.grid_question_group)

        self.sub_group_1 = QuestionGroupFactory(subsection=self.subsection, parent=self.grid_question_group)
        self.sub_group_1.question.add(self.column_3_question)
        self.order_4 = QuestionGroupOrder.objects.create(question=self.column_3_question, order=4,
                                                         question_group=self.grid_question_group)

    def test_get_orders(self):
        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)

        json_response = json.loads(response.content)
        grid_question_orders = [self.order_1, self.order_2, self.order_3, self.order_4]

        question_orders = map(lambda question_order: question_order['pk'], json_response)
        self.assertEqual(4, len(question_orders))

        for order in grid_question_orders:
            self.assertIn(order.id, question_orders)