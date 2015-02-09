import json

from django.test import Client

from questionnaire.tests.base_test import BaseTest
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.question_group_factory import QuestionGroupFactory
from questionnaire.tests.factories.sub_section_factory import SubSectionFactory
from questionnaire.tests.factories.theme_factory import ThemeFactory
from questionnaire.utils.answer_type import AnswerTypes


class ThemesAPITest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.theme1 = ThemeFactory()
        self.subsection = SubSectionFactory()
        self.grid_question_group = QuestionGroupFactory(grid=True, allow_multiples=True,
                                                        subsection=self.subsection)
        self.url = '/api/v1/subsection/%s/grid/%s/' % (self.subsection.id, self.grid_question_group.id)

        self.primary_question = QuestionFactory(is_primary=True, text='Some primary question',
                                                answer_type=AnswerTypes.MULTI_CHOICE, theme=self.theme1)
        self.column_1_question = QuestionFactory(text='Question 1', answer_type=AnswerTypes.DATE, theme=self.theme1)
        self.column_2_question = QuestionFactory(text='Question 2', answer_type=AnswerTypes.TEXT, theme=self.theme1)
        self.column_3_question = QuestionFactory(text='Question 3', answer_type=AnswerTypes.TEXT, theme=self.theme1)

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