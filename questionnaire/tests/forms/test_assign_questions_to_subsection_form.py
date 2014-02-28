from questionnaire.forms.assign_question import AssignQuestionForm
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup
from questionnaire.tests.base_test import BaseTest


class AssignQuestionFormTest(BaseTest):

    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1)
        self.subsection = SubSection.objects.create(title="subsection 1", section=self.section, order=1)
        self.question1 = Question.objects.create(text='Q1', UID='C00003', answer_type='Number')        
        self.question2 = Question.objects.create(text='Q2', UID='C00002', answer_type='Number')        
        self.form_data = {'questions': [self.question1.id, self.question2.id]}

    def test_valid(self):
        assign_question_form = AssignQuestionForm(self.form_data)
        self.assertTrue(assign_question_form.is_valid())

    def test_non_existing_question_is_invalid(self):
        non_existing_question_id = '999'
        data = {'questions': [non_existing_question_id, self.question1.id]}
        assign_question_form = AssignQuestionForm(data)
        self.assertFalse(assign_question_form.is_valid())
        error_message = 'Select a valid choice. 999 is not one of the available choices.'
        self.assertEqual([error_message], assign_question_form.errors['questions'])

    def test_create_groups_on_save_if_subsection_does_not_already_have_one(self):
        assign_question_form = AssignQuestionForm(self.form_data, subsection=self.subsection)
        self.assertTrue(assign_question_form.is_valid())
        assign_question_form.save()
        question_group = self.question1.question_group.all()
        self.assertEqual(1, question_group.count())
        self.assertEqual(question_group[0], self.question2.question_group.all()[0])
        self.assertEqual(self.subsection, question_group[0].subsection)

    def test_does_not_create_groups_on_save_if_subsection_already_have_one(self):
        already_existing_group = QuestionGroup.objects.create(subsection=self.subsection, order=1)
        assign_question_form = AssignQuestionForm(self.form_data, subsection=self.subsection)
        self.assertTrue(assign_question_form.is_valid())
        assign_question_form.save()
        question_group = self.question1.question_group.all()
        self.assertEqual(1, question_group.count())
        self.assertEqual(question_group[0], self.question2.question_group.all()[0])
        self.assertEqual(already_existing_group, question_group[0])

    def test_create_order_incrementally_on_save(self):
        assign_question_form = AssignQuestionForm(self.form_data, subsection=self.subsection)
        self.assertTrue(assign_question_form.is_valid())
        assign_question_form.save()
        question_group = self.question1.question_group.all()
        self.assertEqual(0, self.question1.orders.get(question_group=question_group[0]).order)
        self.assertEqual(1, self.question2.orders.get(question_group=question_group[0]).order)

    def test_create_order_incrementally_on_save(self):
        already_existing_group = QuestionGroup.objects.create(subsection=self.subsection, order=1)
        question_with_order = Question.objects.create(text='Q w/ order', UID='C00023', answer_type='Number')
        some_arbitrary_order = 50
        question_with_order.orders.create(question_group=already_existing_group, order=some_arbitrary_order)

        assign_question_form = AssignQuestionForm(self.form_data, subsection=self.subsection)
        self.assertTrue(assign_question_form.is_valid())
        assign_question_form.save()
        question_group = self.question1.question_group.all()
        self.assertEqual(some_arbitrary_order + 1, self.question1.orders.get(question_group=question_group[0]).order)
        self.assertEqual(some_arbitrary_order + 2, self.question2.orders.get(question_group=question_group[0]).order)
