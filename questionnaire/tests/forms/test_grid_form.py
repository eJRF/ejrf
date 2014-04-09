from questionnaire.forms.grid import GridForm
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionOption
from questionnaire.tests.base_test import BaseTest


class GridFormTest(BaseTest):

    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English")

        self.section1 = Section.objects.create(title="Reported Cases of Selected Vaccine", order=1,
                                               questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="subsection 1", order=1, section=self.section1)
        self.sub_section2 = SubSection.objects.create(title="subsection 2", order=2, section=self.section1)

        self.question1 = Question.objects.create(text='Favorite beer 1', UID='C00001', answer_type='MultiChoice',
                                                 is_primary=True)
        self.option1 = QuestionOption.objects.create(text='tusker lager', question=self.question1)
        self.option2 = QuestionOption.objects.create(text='tusker lager1', question=self.question1)
        self.option3 = QuestionOption.objects.create(text='tusker lager2', question=self.question1)

        self.question2 = Question.objects.create(text='question 2', instructions="instruction 2",
                                                 UID='C00002', answer_type='Text')

        self.question3 = Question.objects.create(text='question 3', instructions="instruction 3",
                                                 UID='C00003', answer_type='Number')

        self.question4 = Question.objects.create(text='question 4', instructions="instruction 2",
                                                 UID='C00005', answer_type='Date')

        self.form_data ={
            'type': 'display_all',
            'primary_question': str(self.question1.id),
            'columns': [str(self.question2.id), str(self.question3.id)]
        }

    def test_valid(self):
        grid_form = GridForm(self.form_data)
        grid_form.is_valid()
        print grid_form.errors
        self.assertTrue(grid_form.is_valid())

    def test_invalid_primary_question(self):
        data = self.form_data.copy()
        not_a_primary_question = self.question2
        data['primary_question'] = not_a_primary_question.id
        grid_form = GridForm(data)
        self.assertFalse(grid_form.is_valid())
        error_message = 'Select a valid choice. That choice is not one of the available choices.'
        self.assertEqual([error_message], grid_form.errors['primary_question'])

    def test_primary_question_can_only_be_multichoice(self):
        data = self.form_data.copy()
        non_multichoice_primary_question = Question.objects.create(text="haha", answer_type="Text", is_primary=True)
        data['primary_question'] = non_multichoice_primary_question.id
        grid_form = GridForm(data)
        self.assertFalse(grid_form.is_valid())
        error_message = 'Select a valid choice. That choice is not one of the available choices.'
        self.assertEqual([error_message], grid_form.errors['primary_question'])

    def test_invalid_column_question(self):
        data = self.form_data.copy()
        primary_question = self.question1
        data['columns'] = [self.question2.id, primary_question.id]
        grid_form = GridForm(data)
        self.assertFalse(grid_form.is_valid())
        error_message = 'Select a valid choice. %d is not one of the available choices.' % primary_question.id
        print grid_form.errors
        self.assertEqual([error_message], grid_form.errors['columns'])

    def test_save_grid_creates_grid(self):
        grid_form = GridForm(self.form_data, subsection=self.sub_section)

        self.failIf(self.question1.question_group.all())
        self.failIf(self.question2.question_group.all())
        self.failIf(self.question3.question_group.all())
        self.failIf(self.question4.question_group.all())

        grid_form.is_valid()
        grid_form.save()

        grid_group = self.question1.question_group.filter()
        self.failUnless(grid_group)
        self.assertEqual(1, grid_group.count())
        self.assertEqual(self.sub_section, grid_group[0].subsection)
        self.assertEqual(0, grid_group[0].order)
        self.assertTrue(grid_group[0].grid)
        self.assertTrue(grid_group[0].display_all)
        group_questions = grid_group[0].question.all()
        self.assertEqual(3, group_questions.count())
        self.assertIn(self.question2, group_questions)
        self.assertIn(self.question3, group_questions)

    def test_save_grid_creates_group_orders(self):
        grid_form = GridForm(self.form_data, subsection=self.sub_section)

        grid_form.is_valid()
        grid_form.save()

        grid_group = self.question1.question_group.get(subsection=self.sub_section)
        group_orders = grid_group.orders.all()
        self.failUnless(group_orders)
        self.assertEqual(3, group_orders.count())
        self.assertEqual(1, group_orders.filter(question=self.question1, order=0).count())
        self.assertEqual(1, group_orders.filter(question=self.question2, order=1).count())
        self.assertEqual(1, group_orders.filter(question=self.question3, order=2).count())
