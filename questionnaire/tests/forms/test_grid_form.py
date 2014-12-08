from questionnaire.forms.grid import GridForm
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionOption, Region, Theme
from questionnaire.tests.base_test import BaseTest
from questionnaire.tests.factories.question_factory import QuestionFactory


class GridFormTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English")

        self.section1 = Section.objects.create(title="Reported Cases of Selected Vaccine", order=1,
                                               questionnaire=self.questionnaire, name="Reported Cases")

        self.region = Region.objects.create(name="AFR")
        self.sub_section = SubSection.objects.create(title="subsection 1", order=1, section=self.section1,
                                                     region=self.region)
        self.sub_section2 = SubSection.objects.create(title="subsection 2", order=2, section=self.section1)
        self.theme = Theme.objects.create(name="Theme1", description="Our theme.")

        self.question1 = Question.objects.create(text='Favorite beer 1', UID='C00001', answer_type='MultiChoice',
                                                 is_primary=True, region=self.region, theme=self.theme)
        self.option1 = QuestionOption.objects.create(text='tusker lager', question=self.question1)
        self.option2 = QuestionOption.objects.create(text='tusker lager1', question=self.question1)
        self.option3 = QuestionOption.objects.create(text='tusker lager2', question=self.question1)

        self.question2 = Question.objects.create(text='question 2', instructions="instruction 2", theme=self.theme,
                                                 UID='C00002', answer_type='Text', region=self.region)

        self.question3 = Question.objects.create(text='question 3', instructions="instruction 3",
                                                 UID='C00003', answer_type='Number', theme=self.theme)

        self.question4 = Question.objects.create(text='question 4', instructions="instruction 2",
                                                 UID='C00005', answer_type='Date', theme=self.theme)

        self.form_data = {
            'type': 'display_all',
            'primary_question': str(self.question1.id),
            'columns': [str(self.question2.id), str(self.question3.id)]
        }

    def test_only_own_region_questions_are_available(self):
        grid_form = GridForm(subsection=self.sub_section, region=self.region)

        primary_question_queryset = grid_form.fields['primary_question'].queryset
        self.assertEqual(1, primary_question_queryset.count())
        self.assertEqual(self.question1, primary_question_queryset[0])

        columns_queryset = grid_form.fields['columns'].queryset
        self.assertEqual(1, columns_queryset.count())
        self.assertEqual(self.question2, columns_queryset[0])

    def test_only_unused_questions_in_questionnaire_are_available(self):
        primary_question_not_in_self_questionnaire = Question.objects.create(text='primary other Qnaire', UID='C00011',
                                                                             answer_type='MultiChoice', is_primary=True,
                                                                             region=self.region, theme=self.theme)
        question_not_in_self_questionnaire = Question.objects.create(text='non primary  other Qnaire', UID='C00012',
                                                                     answer_type='Text', region=self.region,
                                                                     theme=self.theme)

        section1 = Section.objects.create(title="section 2", order=1, questionnaire=self.questionnaire,
                                          name="section 2", region=self.region)
        sub = SubSection.objects.create(title="subsection 1", order=1, section=section1, region=self.region)
        group = primary_question_not_in_self_questionnaire.question_group.create(subsection=sub)
        group.question.add(question_not_in_self_questionnaire)

        grid_form = GridForm(subsection=self.sub_section, region=self.region)

        primary_question_queryset = grid_form.fields['primary_question'].queryset
        self.assertEqual(1, primary_question_queryset.count())
        self.assertEqual(self.question1, primary_question_queryset[0])

        columns_queryset = grid_form.fields['columns'].queryset
        self.assertEqual(1, columns_queryset.count())
        self.assertEqual(self.question2, columns_queryset[0])

    def test_only_global_stuff_are_available_to_global_admin(self):
        grid_form = GridForm(subsection=self.sub_section, region=None)

        primary_question_queryset = grid_form.fields['primary_question'].queryset
        self.assertEqual(0, primary_question_queryset.count())

        columns_queryset = grid_form.fields['columns'].queryset
        self.assertEqual(2, columns_queryset.count())
        self.assertIn(self.question3, columns_queryset)
        self.assertIn(self.question4, columns_queryset)

    def test_only_questions_from_the_same_theme_are_allowed_for_columns(self):
        question_from_different_theme = Question.objects.create(text='question 2', theme=None,
                                                                UID='C00022', answer_type='Text', region=self.region)
        data = self.form_data.copy()
        data['columns'] = [question_from_different_theme.id, self.question2.id]
        grid_form = GridForm(data, subsection=self.sub_section, region=self.region)

        self.assertFalse(grid_form.is_valid())
        error_message = 'All questions must be with theme %s.' % self.theme.name
        self.assertEqual([error_message], grid_form.errors['columns'])

    def test_only_questions_from_the_same_theme_are_allowed_for_subgroups(self):
        question_from_different_theme = Question.objects.create(text='question 2', theme=None,
                                                                UID='C00022', answer_type='Text', region=self.region)
        data = self.form_data.copy()
        data['subgroup'] = [question_from_different_theme.id]
        grid_form = GridForm(data, subsection=self.sub_section, region=self.region)

        self.assertFalse(grid_form.is_valid())
        error_message = 'All questions must be with theme %s.' % self.theme.name
        self.assertEqual([error_message], grid_form.errors['subgroup'])


class DisplayAllGridFormTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English")

        self.section1 = Section.objects.create(title="Reported Cases of Selected Vaccine", order=1,
                                               questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="subsection 1", order=1, section=self.section1)
        self.sub_section2 = SubSection.objects.create(title="subsection 2", order=2, section=self.section1)
        self.theme = Theme.objects.create(name="Theme1", description="Our theme.")

        self.question1 = Question.objects.create(text='Favorite beer 1', UID='C00001', answer_type='MultiChoice',
                                                 is_primary=True, theme=self.theme)
        self.option1 = QuestionOption.objects.create(text='tusker lager', question=self.question1)
        self.option2 = QuestionOption.objects.create(text='tusker lager1', question=self.question1)
        self.option3 = QuestionOption.objects.create(text='tusker lager2', question=self.question1)

        self.question2 = Question.objects.create(text='question 2', instructions="instruction 2",
                                                 UID='C00002', answer_type='Text', theme=self.theme)

        self.question3 = Question.objects.create(text='question 3', instructions="instruction 3",
                                                 UID='C00003', answer_type='Number', theme=self.theme)

        self.question4 = Question.objects.create(text='question 4', instructions="instruction 2",
                                                 UID='C00005', answer_type='Date', theme=self.theme)

        self.form_data = {
            'type': 'display_all',
            'primary_question': str(self.question1.id),
            'columns': [str(self.question2.id), str(self.question3.id)]
        }

    def test_valid_and_is_core_when_region_is_none(self):
        user =self.create_user(org='WHO', group=self.GLOBAL_ADMIN)
        grid_form = GridForm(self.form_data, subsection=self.sub_section, region=user.user_profile.region)

        self.assertTrue(grid_form.is_valid())
        new_grid = grid_form.save()

        self.assertIsNone(new_grid.region)
        self.assertTrue(new_grid.is_core)

    def test_valid_and_not_is_core_when_region_is_not_none(self):
        user =self.create_user(username='username', org='WHO', group=self.REGIONAL_ADMIN, region='AFR')

        question1 = QuestionFactory(region=user.user_profile.region, text='Some text 1', is_primary=True, answer_type='MultiChoice')
        question2 = QuestionFactory(region=user.user_profile.region, text='Some text 2', answer_type='Text')
        question3 = QuestionFactory(region=user.user_profile.region, text='Some text 3', answer_type='Text')

        form_data = {
            'type': 'display_all',
            'primary_question': question1.id,
            'columns': [question2.id, question3.id]
        }

        grid_form = GridForm(form_data, subsection=self.sub_section, region=user.user_profile.region)
        grid_form.is_valid()
        self.assertTrue(grid_form.is_valid())

        new_grid = grid_form.save()

        self.assertEqual(new_grid.region, user.user_profile.region)
        self.assertFalse(new_grid.is_core)

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
        non_multichoice_primary_question = Question.objects.create(text="haha", answer_type="Text", is_primary=True,
                                                                   theme=self.theme)
        data['primary_question'] = non_multichoice_primary_question.id
        grid_form = GridForm(data)
        self.assertFalse(grid_form.is_valid())
        error_message = 'This type of grid requires a multichoice primary question.'
        self.assertEqual([error_message], grid_form.errors['primary_question'])

    def test_invalid_column_question(self):
        data = self.form_data.copy()
        primary_question = self.question1
        data['columns'] = [self.question2.id, primary_question.id]
        grid_form = GridForm(data)
        self.assertFalse(grid_form.is_valid())
        error_message = 'Select a valid choice. %d is not one of the available choices.' % primary_question.id
        self.assertEqual([error_message], grid_form.errors['columns'])

    def test_save_display_all_grid_creates_display_all_grid(self):
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


class AddMoreGridFormTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English")

        self.section1 = Section.objects.create(title="Reported Cases of Selected Vaccine", order=1,
                                               questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="subsection 1", order=1, section=self.section1)
        self.sub_section2 = SubSection.objects.create(title="subsection 2", order=2, section=self.section1)
        self.theme = Theme.objects.create(name="Theme1", description="Our theme.")

        self.question1 = Question.objects.create(text='Favorite beer 1', UID='C00001', answer_type='Text',
                                                 is_primary=True, theme=self.theme)

        self.question2 = Question.objects.create(text='question 2', instructions="instruction 2",
                                                 UID='C00002', answer_type='Text', theme=self.theme)

        self.question3 = Question.objects.create(text='question 3', instructions="instruction 3",
                                                 UID='C00003', answer_type='Number', theme=self.theme)

        self.question4 = Question.objects.create(text='question 4', instructions="instruction 2",
                                                 UID='C00005', answer_type='Date', theme=self.theme)

        self.form_data = {
            'type': 'allow_multiples',
            'primary_question': str(self.question1.id),
            'columns': [str(self.question2.id), str(self.question3.id)]
        }

    def test_valid(self):
        grid_form = GridForm(self.form_data, subsection=self.sub_section)
        grid_form.is_valid()
        self.assertTrue(grid_form.is_valid())

    def test_invalid_primary_question(self):
        data = self.form_data.copy()
        not_a_primary_question = self.question2
        data['primary_question'] = not_a_primary_question.id
        grid_form = GridForm(data)
        self.assertFalse(grid_form.is_valid())
        error_message = 'Select a valid choice. That choice is not one of the available choices.'
        self.assertEqual([error_message], grid_form.errors['primary_question'])

    def test_save_add_more_grid_creates_add_more_grid(self):
        grid_form = GridForm(self.form_data, subsection=self.sub_section)

        self.failIf(self.question1.question_group.all())
        self.failIf(self.question2.question_group.all())
        self.failIf(self.question3.question_group.all())
        self.failIf(self.question4.question_group.all())

        self.assertTrue(grid_form.is_valid())
        grid_form.save()

        grid_group = self.question1.question_group.filter()
        self.failUnless(grid_group)
        self.assertEqual(1, grid_group.count())
        self.assertEqual(self.sub_section, grid_group[0].subsection)
        self.assertEqual(0, grid_group[0].order)
        self.assertTrue(grid_group[0].grid)
        self.assertTrue(grid_group[0].allow_multiples)
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


class HybridGridFormTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English")

        self.section1 = Section.objects.create(title="Reported Cases of Selected Vaccine", order=1,
                                               questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="subsection 1", order=1, section=self.section1)
        self.sub_section2 = SubSection.objects.create(title="subsection 2", order=2, section=self.section1)
        self.theme = Theme.objects.create(name="Theme1", description="Our theme.")

        self.question1 = Question.objects.create(text='Favorite beer 1', UID='C00001', answer_type='MultiChoice',
                                                 is_primary=True, theme=self.theme)
        self.option1 = QuestionOption.objects.create(text='tusker lager', question=self.question1)
        self.option2 = QuestionOption.objects.create(text='tusker lager1', question=self.question1)
        self.option3 = QuestionOption.objects.create(text='tusker lager2', question=self.question1)

        self.question2 = Question.objects.create(text='question 2', instructions="instruction 2",
                                                 UID='C00002', answer_type='Text', theme=self.theme)

        self.question3 = Question.objects.create(text='question 3', instructions="instruction 3",
                                                 UID='C00003', answer_type='Number', theme=self.theme)

        self.question4 = Question.objects.create(text='question 4', instructions="instruction 2",
                                                 UID='C00005', answer_type='Date', theme=self.theme)
        self.question5 = Question.objects.create(text='question 5', instructions="instruction 5",
                                                 UID='C00006', answer_type='MultiChoice', theme=self.theme)

        self.form_data = {
            'type': 'hybrid',
            'primary_question': str(self.question1.id),
            'columns': [str(self.question2.id), str(self.question4.id), str(self.question5.id), str(self.question3.id)],
            'subgroup': [str(self.question4.id), str(self.question5.id)]
        }

    def test_valid(self):
        grid_form = GridForm(self.form_data)
        self.assertTrue(grid_form.is_valid())

    def test_invalid_primary_question(self):
        data = self.form_data.copy()
        not_a_primary_question = self.question2
        data['primary_question'] = not_a_primary_question.id
        grid_form = GridForm(data)
        self.assertFalse(grid_form.is_valid())
        error_message = 'Select a valid choice. That choice is not one of the available choices.'
        self.assertEqual([error_message], grid_form.errors['primary_question'])

    def test_primary_question_is_not_constrained_to_be_multichoice(self):
        data = self.form_data.copy()
        non_multichoice_primary_question = Question.objects.create(text="haha", answer_type="Text", is_primary=True,
                                                                   theme=self.theme)
        data['primary_question'] = non_multichoice_primary_question.id
        grid_form = GridForm(data)
        self.assertTrue(grid_form.is_valid())

    def test_save_hybrid_grid_creates_hybrid_grid(self):
        grid_form = GridForm(self.form_data, subsection=self.sub_section)

        self.failIf(self.question1.question_group.all())
        self.failIf(self.question2.question_group.all())
        self.failIf(self.question3.question_group.all())
        self.failIf(self.question4.question_group.all())
        self.failIf(self.question5.question_group.all())

        grid_form.is_valid()
        grid_form.save()

        grid_group = self.question1.question_group.filter()
        self.failUnless(grid_group)
        self.assertEqual(1, grid_group.count())
        self.assertEqual(self.sub_section, grid_group[0].subsection)
        self.assertEqual(0, grid_group[0].order)
        self.assertTrue(grid_group[0].grid)
        self.assertTrue(grid_group[0].allow_multiples)
        self.assertTrue(grid_group[0].hybrid)
        group_questions = grid_group[0].question.all()
        self.assertEqual(3, group_questions.count())
        self.assertIn(self.question2, group_questions)
        self.assertIn(self.question3, group_questions)

        grid_sub_group = self.question4.question_group.filter()
        self.failUnless(grid_sub_group)
        self.assertEqual(1, grid_sub_group.count())
        self.assertEqual(self.sub_section, grid_sub_group[0].subsection)
        self.assertEqual(grid_group[0], grid_sub_group[0].parent)
        self.assertTrue(grid_sub_group[0].grid)
        group_questions = grid_sub_group[0].question.all()
        self.assertEqual(2, group_questions.count())
        self.assertIn(self.question4, group_questions)
        self.assertIn(self.question5, group_questions)

    def test_save_grid_creates_group_orders(self):
        grid_form = GridForm(self.form_data, subsection=self.sub_section)

        grid_form.is_valid()
        grid_form.save()

        grid_group = self.question1.question_group.get(subsection=self.sub_section)
        group_orders = grid_group.orders.all()
        self.failUnless(group_orders)
        self.assertEqual(5, group_orders.count())
        self.assertEqual(1, group_orders.filter(question=self.question1, order=0).count())
        self.assertEqual(1, group_orders.filter(question=self.question2, order=1).count())
        self.assertEqual(1, group_orders.filter(question=self.question4, order=2).count())
        self.assertEqual(1, group_orders.filter(question=self.question5, order=3).count())
        self.assertEqual(1, group_orders.filter(question=self.question3, order=4).count())
