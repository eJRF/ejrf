from questionnaire.forms.questions import QuestionForm
from questionnaire.models import Question, QuestionOption, Questionnaire, Section, SubSection, QuestionGroup, Region, \
    Theme
from questionnaire.tests.base_test import BaseTest
from questionnaire.utils.answer_type import AnswerTypes
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.question_option_factory import QuestionOptionFactory


class QuestionFormTest(BaseTest):
    def setUp(self):
        self.theme = Theme.objects.create(name="Another theme")
        self.form_data = {'text': 'How many kids were immunised this year?',
                          'instructions': 'Some instructions',
                          'short_instruction': 'short version',
                          'answer_type': 'Text',
                          'export_label': 'Some export text',
                          'options': ['', ],
                          'theme': self.theme.id}

    def test_valid(self):
        section_form = QuestionForm(data=self.form_data)
        self.assertTrue(section_form.is_valid())

    def test_increments_uid_of_existing_question_by_one_upon_save_given_instance(self):
        Question.objects.create(text='B. Number of cases tested',
                                instructions="Enter the total number of cases", UID='00001', answer_type='Number',
                                answer_sub_type="Integer")
        question_form = QuestionForm(data=self.form_data)
        question = question_form.save(commit=True)
        self.assertEqual('00002', question.UID)

    def test_invalid_if_question_text_is_blank(self):
        data = self.form_data.copy()
        data['text'] = ''
        question_form = QuestionForm(data=data)
        self.assertFalse(question_form.is_valid())
        self.assertIn("This field is required.", question_form.errors['text'])

    def test_clean_answer_type(self):
        data = self.form_data.copy()
        data['answer_type'] = ''
        question_form = QuestionForm(data=data)
        self.assertFalse(question_form.is_valid())
        self.assertIn("This field is required.", question_form.errors['answer_type'])

    def test_clean_answer_number_sub_type(self):
        data = self.form_data.copy()
        data['answer_type'] = AnswerTypes.NUMBER
        question_form = QuestionForm(data=data)
        self.assertFalse(question_form.is_valid())
        self.assertIn("This field is required if you select '%s'" % AnswerTypes.NUMBER, question_form.errors['answer_sub_type'])

    def test_clean_answer_number_sub_type_valid(self):
        data = self.form_data.copy()
        data['answer_type'] = AnswerTypes.NUMBER
        data['answer_sub_type'] = AnswerTypes.DECIMAL
        question_form = QuestionForm(data=data)
        self.assertTrue(question_form.is_valid())
        self.assertTrue(len(question_form.errors) == 0)

    def test_clean_answer_date_sub_type(self):
        data = self.form_data.copy()
        data['answer_type'] = AnswerTypes.DATE
        question_form = QuestionForm(data=data)
        self.assertFalse(question_form.is_valid())
        self.assertIn("This field is required if you select '%s'" % AnswerTypes.DATE, question_form.errors['answer_sub_type'])

    def test_clean_export_label(self):
        data = self.form_data.copy()
        data['export_label'] = ''
        question_form = QuestionForm(data=data)
        self.assertFalse(question_form.is_valid())
        self.assertIn("All questions must have export label.", question_form.errors['export_label'])

    def test_answer_type_choices_has_empty_label(self):
        question_form = QuestionForm()
        self.assertIn(('', 'Response type'), question_form.fields['answer_type'].choices)

    def test_answer_sub_type_choices(self):
        question_form = QuestionForm()
        self.assertIn(('', 'Select a Sub-Type'), question_form.fields['answer_sub_type'].choices)
        self.assertIn(('DD/MM/YYYY', 'DD/MM/YYYY'), question_form.fields['answer_sub_type'].choices)
        self.assertIn(('MM/YYYY', 'MM/YYYY'), question_form.fields['answer_sub_type'].choices)
        self.assertIn(('Integer', 'Integer'), question_form.fields['answer_sub_type'].choices)
        self.assertIn(('Decimal', 'Decimal'), question_form.fields['answer_sub_type'].choices)

    def test_save_multichoice_question_saves_packaged_options(self):
        options = ['', 'Yes, No', 'Maybe']
        form = {'text': 'How many kids were immunised this year?',
                'instructions': 'Some instructions',
                'short_instruction': 'short version',
                'export_label': 'blah',
                'answer_type': 'MultiChoice',
                'options': options,
                'theme': self.theme.id}

        question_form = QuestionForm(data=form)
        question = question_form.save(commit=True)
        question_options = QuestionOption.objects.filter(question=question)

        self.assertEqual(2, question_options.count())
        [self.assertIn(question_option.text, ['Yes, No', 'Maybe']) for question_option in question_options]

    def test_save_multichoice_question_saves_listed_options(self):
        options = ['', 'Yes', 'No', 'Maybe']
        form = {'text': 'How many kids were immunised this year?',
                'instructions': 'Some instructions',
                'short_instruction': 'short version',
                'export_label': 'blah',
                'answer_type': 'MultiChoice',
                'options': options,
                'theme': self.theme.id}

        question_form = QuestionForm(data=form)
        question = question_form.save(commit=True)
        question_options = QuestionOption.objects.filter(question=question)

        self.assertEqual(3, question_options.count())
        [self.assertIn(question_option.text, ['Yes', 'No', 'Maybe']) for question_option in question_options]

    def test_assigns_region_on_save_if_region_is_given(self):
        region = Region.objects.create(name="ASEAN")
        form = {'text': 'How many kids were immunised this year?',
                'instructions': 'Some instructions',
                'short_instruction': 'short version',
                'export_label': 'blah',
                'answer_type': 'Text',
                'theme': self.theme.id}
        question_form = QuestionForm(region=region, data=form)
        question = question_form.save(commit=True)
        self.assertEqual(region, question.region)

    def test_form_invalid_if_multichoice_question_and_no_options_in_data_options(self):
        form = {'text': 'How many kids were immunised this year?',
                'instructions': 'Some instructions',
                'short_instruction': 'short version',
                'export_label': 'blah',
                'answer_type': 'MultiChoice',
                'options': ['', ''],
                'theme': self.theme.id}
        question_form = QuestionForm(data=form)

        self.assertFalse(question_form.is_valid())
        message = "MultiChoice questions must have at least one option"
        self.assertIn(message, question_form.errors['answer_type'][0])

    def test_form_invalid_if_multipleresponse_question_and_no_options_in_data_options(self):
        form = {'text': 'How many kids were immunised this year?',
                'instructions': 'Some instructions',
                'short_instruction': 'short version',
                'export_label': 'blah',
                'answer_type': AnswerTypes.MULTIPLE_RESPONSE,
                'options': ['', ''],
                'theme': self.theme.id}
        question_form = QuestionForm(data=form)

        self.assertFalse(question_form.is_valid())
        message = "%s questions must have at least one option" % AnswerTypes.MULTIPLE_RESPONSE
        self.assertIn(message, question_form.errors['answer_type'][0])

    def test_form_invalid_if_multipleresponse_question_is_primary(self):
        options = ['', 'Yes', 'No', 'Maybe']
        form = {'text': 'How many kids were immunised this year?',
                'instructions': 'Some instructions',
                'short_instruction': 'short version',
                'export_label': 'blah',
                'answer_type': AnswerTypes.MULTIPLE_RESPONSE,
                'is_primary': 'true',
                'options': options,
                'theme': self.theme.id}
        question_form = QuestionForm(data=form)

        self.assertFalse(question_form.is_valid())
        message = "%s questions cannot be primary" % AnswerTypes.MULTIPLE_RESPONSE
        self.assertIn(message, question_form.errors['is_primary'][0])

    def test_save__multipleresponse_question_saves_listed_options(self):
        options = ['', 'Yes', 'No', 'Maybe']
        form = {'text': 'How many kids were immunised this year?',
                'instructions': 'Some instructions',
                'short_instruction': 'short version',
                'export_label': 'blah',
                'answer_type': AnswerTypes.MULTIPLE_RESPONSE,
                'options': options,
                'theme': self.theme.id}

        question_form = QuestionForm(data=form)
        question = question_form.save(commit=True)
        question_options = QuestionOption.objects.filter(question=question)

        self.assertEqual(3, question_options.count())
        [self.assertIn(question_option.text, ['Yes', 'No', 'Maybe']) for question_option in question_options]


class QuestionHistoryTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="2014", description="some description")
        self.section = Section.objects.create(title="section", order=1, questionnaire=self.questionnaire)
        self.sub_section = SubSection.objects.create(title="subsection", order=1, section=self.section)
        self.question1 = Question.objects.create(text='q1', UID='C00003', answer_type='Text')
        self.parent_group = QuestionGroup.objects.create(subsection=self.sub_section, name="group1")
        self.theme = Theme.objects.create(name="Theme1")
        self.parent_group.question.add(self.question1)

        self.form_data = {'text': 'q1 edited.',
                          'answer_type': 'Text',
                          'export_label': 'Some export text',
                          'theme': self.theme.id}

    def test_editing_question_used_in_an_unpublished_questionnaire_updates_question(self):
        data = self.form_data.copy()
        history_form = QuestionForm(data=data, instance=self.question1)
        history_form.is_valid()

        history_form.save()

        questions = Question.objects.filter(UID=self.question1.UID)

        self.assertEqual(1, questions.count())
        self.failUnless(self.question1.id, questions[0].id)

    def test_editing_question_used_in_a_published_questionnaire_creates_a_duplicate_question(self):
        self.questionnaire.status = Questionnaire.PUBLISHED
        self.questionnaire.save()
        data = self.form_data.copy()
        history_form = QuestionForm(data=data, instance=self.question1)

        self.assertTrue(history_form.is_valid())

        history_form.save()

        questions = Question.objects.filter(UID=self.question1.UID)

        self.assertEqual(2, questions.count())
        self.failUnless(questions.filter(**data))

    def test_duplicate_question_maintains_region(self):
        self.questionnaire.status = Questionnaire.PUBLISHED
        self.questionnaire.save()
        region = Region.objects.create(name="AFR")
        self.question1.region = region
        self.question1.save()
        data = self.form_data.copy()
        history_form = QuestionForm(data=data, instance=self.question1)

        self.assertTrue(history_form.is_valid())
        duplicate_question = history_form.save()

        self.assertEqual(region, duplicate_question.region)

    def test_editing_question_used_in_a_published_questionnaire_assigns_the_duplicate_question_in_all_draft_questionnaires(
            self):
        self.questionnaire.status = Questionnaire.PUBLISHED
        self.questionnaire.save()
        self.question1.orders.create(order=1, question_group=self.parent_group)

        draft_questionnaire = Questionnaire.objects.create(name="draft qnaire", description="haha",
                                                           status=Questionnaire.DRAFT)
        section_1 = Section.objects.create(title="section 1", order=1, questionnaire=draft_questionnaire, name="ha")
        sub_section_1 = SubSection.objects.create(title="subs1", order=1, section=section_1)
        parent_group_d = QuestionGroup.objects.create(subsection=sub_section_1, name="group")
        parent_group_d.question.add(self.question1)
        self.question1.orders.create(order=2, question_group=parent_group_d)

        finalized_questionnaire = Questionnaire.objects.create(name="finalized qnaire", description="haha",
                                                               status=Questionnaire.FINALIZED)
        section_1_f = Section.objects.create(title="section 1", order=1, questionnaire=finalized_questionnaire,
                                             name="ha")
        sub_section_1_f = SubSection.objects.create(title="subs1", order=1, section=section_1_f)
        parent_group_f = QuestionGroup.objects.create(subsection=sub_section_1_f, name="group")
        parent_group_f.question.add(self.question1)
        self.question1.orders.create(order=3, question_group=parent_group_f)

        data = self.form_data.copy()
        history_form = QuestionForm(data=data, instance=self.question1)

        self.assertTrue(history_form.is_valid())
        duplicate_question = history_form.save()

        parent_group_questions = self.parent_group.question.all()
        self.assertEqual(1, parent_group_questions.count())
        self.assertIn(self.question1, parent_group_questions)

        parent_group_d_questions = parent_group_d.question.all()
        self.assertEqual(1, parent_group_d_questions.count())
        self.assertIn(duplicate_question, parent_group_d_questions)

        parent_group_f_questions = parent_group_f.question.all()
        self.assertEqual(1, parent_group_f_questions.count())
        self.assertIn(duplicate_question, parent_group_f_questions)

    def test_editing_question_used_in_a_published_questionnaire_give_the_duplicate_question_old_question_order(self):
        self.questionnaire.status = Questionnaire.PUBLISHED
        self.questionnaire.save()
        self.question1.orders.create(order=1, question_group=self.parent_group)

        draft_questionnaire = Questionnaire.objects.create(name="draft qnaire", description="haha",
                                                           status=Questionnaire.DRAFT)
        section_1 = Section.objects.create(title="section 1", order=1, questionnaire=draft_questionnaire, name="ha")
        sub_section_1 = SubSection.objects.create(title="subs1", order=1, section=section_1)
        parent_group_d = QuestionGroup.objects.create(subsection=sub_section_1, name="group")
        parent_group_d.question.add(self.question1)
        self.question1.orders.create(order=2, question_group=parent_group_d)

        finalized_questionnaire = Questionnaire.objects.create(name="finalized qnaire", description="haha",
                                                               status=Questionnaire.FINALIZED)
        section_1_f = Section.objects.create(title="section 1", order=1, questionnaire=finalized_questionnaire,
                                             name="ha")
        sub_section_1_f = SubSection.objects.create(title="subs1", order=1, section=section_1_f)
        parent_group_f = QuestionGroup.objects.create(subsection=sub_section_1_f, name="group")
        parent_group_f.question.add(self.question1)
        self.question1.orders.create(order=3, question_group=parent_group_f)

        data = self.form_data.copy()
        history_form = QuestionForm(data=data, instance=self.question1)

        self.assertTrue(history_form.is_valid())
        duplicate_question = history_form.save()

        self.assertEqual(1, self.question1.orders.get(question_group=self.parent_group).order)
        self.assertEqual(0, duplicate_question.orders.filter(question_group=self.parent_group).count())

        self.assertEqual(2, duplicate_question.orders.get(question_group=parent_group_d).order)
        self.assertEqual(0, self.question1.orders.filter(question_group=parent_group_d).count())

        self.assertEqual(3, duplicate_question.orders.get(question_group=parent_group_f).order)
        self.assertEqual(0, self.question1.orders.filter(question_group=parent_group_f).count())

    def test_multichoice_options_are_only_edited_in_the_duplicate_questions(self):
        self.questionnaire.status = Questionnaire.PUBLISHED
        self.questionnaire.save()
        self.question1.orders.create(order=1, question_group=self.parent_group)
        self.question1.answer_type = 'MultiChoice'
        self.question1.save()
        question1_options_texts = ["Yes", "No", "DK"]
        for text in question1_options_texts:
            self.question1.options.create(text=text)

        draft_questionnaire = Questionnaire.objects.create(name="draft qnaire", description="haha",
                                                           status=Questionnaire.DRAFT)
        section_1 = Section.objects.create(title="section 1", order=1, questionnaire=draft_questionnaire, name="ha")
        sub_section_1 = SubSection.objects.create(title="subs1", order=1, section=section_1)
        parent_group_d = QuestionGroup.objects.create(subsection=sub_section_1, name="group")
        parent_group_d.question.add(self.question1)
        self.question1.orders.create(order=2, question_group=parent_group_d)

        finalized_questionnaire = Questionnaire.objects.create(name="finalized qnaire", description="haha",
                                                               status=Questionnaire.FINALIZED)
        section_1_f = Section.objects.create(title="section 1", order=1, questionnaire=finalized_questionnaire,
                                             name="ha")
        sub_section_1_f = SubSection.objects.create(title="subs1", order=1, section=section_1_f)
        parent_group_f = QuestionGroup.objects.create(subsection=sub_section_1_f, name="group")
        parent_group_f.question.add(self.question1)
        self.question1.orders.create(order=3, question_group=parent_group_f)

        changed_options = ['', 'haha', 'hehe', 'hihi']
        data = {'text': 'changed text',
                'instructions': 'Some instructions',
                'export_label': 'blah',
                'answer_type': 'MultiChoice',
                'theme': self.theme.id,
                'options': changed_options}

        history_form = QuestionForm(data=data, instance=self.question1)

        self.assertTrue(history_form.is_valid())
        duplicate_question = history_form.save()

        question1_options = self.question1.options.all()
        self.assertEqual(3, question1_options.count())
        [self.assertIn(question_option.text, question1_options_texts) for question_option in question1_options]

        duplicate_question_options = duplicate_question.options.all()
        self.assertEqual(3, duplicate_question_options.count())
        [self.assertIn(question_option.text, changed_options) for question_option in duplicate_question_options]

    def test_edit_removes_deleted_options_from_the_question(self):
        question = QuestionFactory(text='whats up?', answer_type=AnswerTypes.MULTI_CHOICE)

        option1 = QuestionOptionFactory(question=question, text='Yes', order=1)
        option2 = QuestionOptionFactory(question=question, text='NR', order=2)
        option3 = QuestionOptionFactory(question=question, text='No', order=3)

        changed_options = ['Yes', 'No', 'Maybe']

        data = {'text': 'changed text',
                'instructions': 'Some instructions',
                'export_label': 'blah',
                'answer_type': 'MultiChoice',
                'theme': self.theme.id,
                'options': changed_options}

        history_form = QuestionForm(data=data, instance=question)

        self.assertTrue(history_form.is_valid())
        edited_question = history_form.save()

        question1_options = edited_question.options.all()

        self.assertEqual(3, question1_options.count())
        [self.assertIn(question_option.text, changed_options) for question_option in question1_options]

