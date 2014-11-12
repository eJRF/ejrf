from django.forms import Select, CheckboxSelectMultiple

from questionnaire.forms.answers import NumericalAnswerForm, TextAnswerForm, DateAnswerForm, MultiChoiceAnswerForm, \
    MultipleResponseForm
from questionnaire.forms.custom_widgets import MultiChoiceAnswerSelectWidget
from questionnaire.models import Question, Country, QuestionOption, QuestionGroup, Section, Questionnaire, SubSection, \
    MultiChoiceAnswer
from questionnaire.tests.base_test import BaseTest
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.question_group_factory import QuestionGroupFactory
from questionnaire.tests.factories.question_option_factory import QuestionOptionFactory
from questionnaire.tests.factories.questionnaire_factory import QuestionnaireFactory
from questionnaire.tests.factories.region_factory import CountryFactory
from questionnaire.tests.factories.section_factory import SectionFactory
from questionnaire.tests.factories.sub_section_factory import SubSectionFactory
from questionnaire.utils.answer_type import AnswerTypes


class NumericalAnswerFormTest(BaseTest):
    def setUp(self):
        self.country = Country.objects.create(name="Peru")
        self.question = Question.objects.create(text='C. Number of cases positive',
                                                instructions="Include only those cases found ...",
                                                UID='C00001', answer_type='Number', answer_sub_type=AnswerTypes.INTEGER)

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan")

        self.section = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                              order=1,
                                              questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                     section=self.section)
        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1, allow_multiples=True)
        self.question_group.question.add(self.question)

        self.form_data = {
            'response': '100',
        }

        self.initial = {
            'question': self.question,
            'country': self.country.id,
            'status': 'DRAFT',
            'version': 1,
            'code': 'HAHA123',
            'group': self.question_group
        }

    def test_valid(self):
        answer_form = NumericalAnswerForm(self.form_data, initial=self.initial)
        self.assertTrue(answer_form.is_valid())

    def test_text_response_is_valid_if_response_is_nr(self):
        form_data = self.form_data.copy()
        form_data['response'] = 'NR'
        answer_form = NumericalAnswerForm(form_data, initial=self.initial)
        self.assertTrue(answer_form.is_valid())

    def test_text_response_is_invalid_if_response_text_and_not_nr(self):
        form_data = self.form_data.copy()
        form_data['response'] = 'MR'
        answer_form = NumericalAnswerForm(form_data, initial=self.initial)
        self.assertFalse(answer_form.is_valid())
        message = 'Enter a number or Either NR or ND if this question is irrelevant'
        self.assertEqual(message, answer_form.errors['response'])

    def test_text_response_is_valid_if_response_is_nd(self):
        form_data = self.form_data.copy()
        form_data['response'] = 'ND'
        answer_form = NumericalAnswerForm(form_data, initial=self.initial)
        self.assertTrue(answer_form.is_valid())

    def test_decimal_response_is_invalid_if_question_answer_subtype_is_integer(self):
        form_data = self.form_data.copy()
        form_data['response'] = '33.4'
        answer_form = NumericalAnswerForm(form_data, initial=self.initial)
        self.assertFalse(answer_form.is_valid())
        message = 'Response should be a whole number.'

        self.assertEqual(message, answer_form.errors['response'])

    def test_valid_if_response_is_zero(self):
        form_data = self.form_data.copy()
        form_data['response'] = '0'
        answer_form = NumericalAnswerForm(form_data, initial=self.initial)
        self.assertTrue(answer_form.is_valid())

    def test_integer_response_is_valid_if_question_answer_subtype_is_decimal(self):
        question = QuestionFactory(answer_type=AnswerTypes.NUMBER, answer_sub_type=AnswerTypes.DECIMAL)
        form_data = self.form_data.copy()
        form_data['response'] = '33.3'
        initial = self.initial.copy()
        initial['question'] = question
        answer_form = NumericalAnswerForm(form_data, initial=initial)
        self.assertTrue(answer_form.is_valid())

    def test_required_question_shows_field_required_error_when_no_data_is_posted_and_no_initial_passed_in(self):
        self.question.is_required = True
        self.question.save()
        answer_form_without_data = NumericalAnswerForm(initial=self.initial)
        answer_form_without_data.show_is_required_errors()
        self.assertEqual(['This field is required.'], answer_form_without_data.errors['response'])

        answer_form_with_data = NumericalAnswerForm(data={'response': 1}, initial=self.initial)
        answer_form_with_data.show_is_required_errors()
        self.assertEqual({}, answer_form_with_data.errors)

        _initial = self.initial.copy()
        _initial['response'] = '1'
        answer_form_with_initial = NumericalAnswerForm(initial=_initial)
        answer_form_with_initial.show_is_required_errors()
        self.assertEqual({}, answer_form_with_initial.errors)


class TextAnswerFormTest(BaseTest):
    def setUp(self):
        self.country = Country.objects.create(name="Peru")
        self.question = Question.objects.create(text='C. Number of cases positive',
                                                instructions="Include only those cases found positive for the infectious agent.",
                                                UID='C00001', answer_type='Text')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan")

        self.section = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                              order=1,
                                              questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                     section=self.section)
        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1, allow_multiples=True)
        self.question_group.question.add(self.question)

        self.form_data = {
            'response': 'some answer',
        }
        self.initial = {
            'question': self.question,
            'country': self.country.id,
            'status': 'DRAFT',
            'version': 1,
            'code': 'HAHA123',
            'group': self.question_group
        }

    def test_valid(self):
        answer_form = TextAnswerForm(self.form_data, initial=self.initial)
        self.assertTrue(answer_form.is_valid())


class DateAnswerFormTest(BaseTest):
    def setUp(self):
        self.country = Country.objects.create(name="Peru")
        self.question = Question.objects.create(text='C. Number of cases positive',
                                                instructions="Include only those cases found positive for the infectious agent.",
                                                UID='C00001', answer_type='Date')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan")

        self.section = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                              order=1,
                                              questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                     section=self.section)
        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1, allow_multiples=True)
        self.question_group.question.add(self.question)

        self.form_data = {
            'response': '2014-01-01',
        }

        self.initial = {
            'question': self.question,
            'country': self.country.id,
            'status': 'DRAFT',
            'version': 1,
            'code': 'HAHA123',
            'group': self.question_group,
            'questionnaire': self.questionnaire.id
        }

    def test_valid(self):
        answer_form = DateAnswerForm(self.form_data, initial=self.initial)
        self.assertTrue(answer_form.is_valid())


class MultiChoiceAnswerFormTest(BaseTest):
    def setUp(self):
        self.country = Country.objects.create(name="Peru")
        self.question = Question.objects.create(text='C. Number of cases positive',
                                                instructions="Include only those cases found positive for the infectious agent.",
                                                UID='C00001', answer_type='MultiChoice', is_primary=True)
        self.question_option_one = QuestionOption.objects.create(text='Option One', question=self.question)

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan")

        self.section = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                              order=1, questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                     section=self.section)
        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1, allow_multiples=True)
        self.question_group.question.add(self.question)

        self.form_data = {
            'response': self.question_option_one.id,
        }

        self.initial = {
            'question': self.question,
            'country': self.country,
            'status': 'DRAFT',
            'version': 1,
            'code': 'HAHA123',
            'group': self.question_group,
            'questionnaire': self.questionnaire,
            'specified_option': '',
        }

    def test_valid(self):
        answer_form = MultiChoiceAnswerForm(self.form_data, initial=self.initial)
        self.assertTrue(answer_form.is_valid())
        self.assertIsNone(answer_form.fields['response'].empty_label)

    def test_id_of_a_non_option(self):
        form_data = self.form_data.copy()
        form_data['response'] = -1
        answer_form = MultiChoiceAnswerForm(form_data, initial=self.initial)
        self.assertFalse(answer_form.is_valid())
        message = 'Select a valid choice. That choice is not one of the available choices.'
        self.assertEqual([message], answer_form.errors['response'])

    def test_multiple_form_choice_form_adds_data_instruction_attributes_for_question_options(self):
        question_option_two = QuestionOption.objects.create(text='Option 2', question=self.question,
                                                            instructions="Some stuff")
        question_option_3 = QuestionOption.objects.create(text='Option 3', question=self.question,
                                                          instructions="Some stuff")
        question_option_4 = QuestionOption.objects.create(text='Option 4', question=self.question,
                                                          instructions="Some stuff")

        answer_form = MultiChoiceAnswerForm(initial=self.initial)
        query_set = answer_form._get_response_choices(self.initial)
        widget = answer_form._get_response_widget(query_set)
        self.assertIsInstance(widget, MultiChoiceAnswerSelectWidget)
        self.assertEqual(4, widget.question_options.count())
        self.assertIn(self.question_option_one, widget.question_options)
        self.assertIn(question_option_two, widget.question_options)
        self.assertIn(question_option_3, widget.question_options)
        self.assertIn(question_option_4, widget.question_options)

        self.assertEqual("Choose One", answer_form.fields['response'].empty_label)

    def test_new_option_is_created_and_saved_as_response_when_specify_field_is_not_empty(self):
        form_data = self.form_data.copy()
        form_data['specified_option'] = 'specified option'
        answer_form = MultiChoiceAnswerForm(form_data, initial=self.initial)
        self.assertTrue(answer_form.is_valid())
        answer_form.save()
        option = QuestionOption.objects.get(text="specified option", question=self.question)
        self.failUnless(MultiChoiceAnswer.objects.filter(response=option, question=self.question))
        as_text = '<input id="id_response" name="response" type="text" value="%d" />' % option.id
        self.assertEqual(as_text, answer_form.visible_fields()[0].as_text())

    def test_input_readonly_widget_if_primary_question_and_group_is_grid_and_display_all(self):
        initial = self.initial.copy()
        option = QuestionOption.objects.create(question=self.question, text="Option1")
        initial['option'] = option
        answer_form = MultiChoiceAnswerForm(initial=initial)
        self.assertIsInstance(answer_form.fields['response'].widget, Select)
        self.assertEqual(answer_form.fields['response'].widget.attrs, {'class': 'hide'})


class MultipleResponseFormTest(BaseTest):
    def setUp(self):
        self.country = CountryFactory()
        self.question = QuestionFactory()
        self.sub_section = SubSectionFactory()
        self.question_group = QuestionGroupFactory()
        self.question_group.question.add(self.question)
        self.female_option = QuestionOptionFactory(text='Female', question=self.question)
        self.male_option = QuestionOptionFactory(text='Male', question=self.question)

        self.form_data = {
            'response': [self.female_option.id, self.male_option.id],
        }

        self.initial = {
            'question': self.question,
            'country': self.country,
            'status': 'DRAFT',
            'version': 1,
            'code': 'HAHA123',
            'group': self.question_group,
            'questionnaire': self.sub_section.section.questionnaire,
        }

    def test_valid(self):
        answer_form = MultipleResponseForm(self.form_data, initial=self.initial)
        self.assertTrue(answer_form.is_valid())

    def test_save_all_selected_options(self):
        answer_form = MultipleResponseForm(self.form_data, initial=self.initial)

        answer = answer_form.save()
        response_all = answer.response.all()
        self.assertEqual(2, response_all.count())
        [self.assertIn(option, response_all) for option in [self.male_option, self.female_option]]

    def test_renders_multiselect_widget(self):
        data = {'response': []}

        answer_form = MultipleResponseForm(data=data, initial=self.initial)

        expected_widget = answer_form.fields['response'].widget
        self.assertIsInstance(expected_widget, CheckboxSelectMultiple)

    def test_response_options_are_question_otpions(self):

        answer_form = MultipleResponseForm(data=self.form_data, initial=self.initial)

        expected_choices = [(self.female_option.id, '%s' % self.female_option.text),
                            (self.male_option.id, '%s' % self.male_option.text)]

        self.assertEqual(expected_choices, list(answer_form.fields['response'].choices))