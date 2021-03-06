from datetime import date

from questionnaire.forms.questionnaires import QuestionnaireFilterForm, PublishQuestionnaireForm, EditQuestionnaireForm
from questionnaire.models import Questionnaire, Region, Organization
from questionnaire.tests.base_test import BaseTest
from questionnaire.tests.factories.questionnaire_factory import QuestionnaireFactory
from questionnaire.tests.factories.region_factory import RegionFactory
from questionnaire.tests.factories.organization_factory import OrganizationFactory
from questionnaire.tests.factories.answer_factory import NumericalAnswerFactory


class QuestionnaireFilterFormTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.FINALIZED,
                                                          year=2013)
        self.start_year = 2014
        self.form_data = {
            'questionnaire': self.questionnaire.id,
            'year': self.start_year,
            'name': 'New JRF'
        }

    def test_valid(self):
        questionnaire_filter = QuestionnaireFilterForm(self.form_data)
        self.assertTrue(questionnaire_filter.is_valid())

    def test_valid_with_published_questionnaire(self):
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.PUBLISHED,
                                                     year=2013)
        form_data = {
            'questionnaire': questionnaire.id,
            'year': self.start_year,
            'name': 'New JRF'
        }
        questionnaire_filter = QuestionnaireFilterForm(form_data)
        self.assertTrue(questionnaire_filter.is_valid())

    def test_has_years_of_existing_questionnaires(self):
        questionnaire_filter = QuestionnaireFilterForm(self.form_data)
        self.assertIn(('', 'Choose a year'), questionnaire_filter.fields['year'].choices)
        for count in range(0, 20):
            year_option = self.start_year + count
            self.assertIn((year_option, year_option), questionnaire_filter.fields['year'].choices)

    def test_invalid_when_questionniare_is_blank(self):
        form_data = self.form_data.copy()
        form_data['questionnaire'] = ''
        questionnaire_filter = QuestionnaireFilterForm(form_data)
        self.assertFalse(questionnaire_filter.is_valid())
        self.assertIn("This field is required.", questionnaire_filter.errors['questionnaire'])

    def test_invalid_when_year_is_blank(self):
        form_data = self.form_data.copy()
        form_data['year'] = ''
        questionnaire_filter = QuestionnaireFilterForm(form_data)
        self.assertFalse(questionnaire_filter.is_valid())
        self.assertIn("This field is required.", questionnaire_filter.errors['year'])

    def test_valid_when_name_is_blank(self):
        form_data = self.form_data.copy()
        form_data['name'] = ''
        questionnaire_filter = QuestionnaireFilterForm(form_data)
        self.assertFalse(questionnaire_filter.is_valid())
        self.assertIn("This field is required.", questionnaire_filter.errors['name'])

    def test_clean_year(self):
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.PUBLISHED,
                                                     year=date.today().year + 1)
        child_questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.PUBLISHED,
                                                           year=date.today().year + 1,
                                                           parent=questionnaire,
                                                           region=RegionFactory(name='AFR'))
        NumericalAnswerFactory(questionnaire=child_questionnaire)

        form_data = self.form_data.copy()
        form_data['year'] = child_questionnaire.year
        questionnaire_filter = QuestionnaireFilterForm(form_data)
        valid = questionnaire_filter.is_valid()
        self.assertFalse(valid)
        message = "Select a valid choice. %d is not one of the available choices." % questionnaire.year
        self.assertIn(message, questionnaire_filter.errors['year'])

    def test_has_years_choices_exclude_existing_questionnaires_years(self):
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.PUBLISHED,
                                                     year=date.today().year + 1)
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.PUBLISHED,
                                                     year=date.today().year + 1,
                                                     parent=questionnaire,
                                                     region=RegionFactory(name='AFR'))
        NumericalAnswerFactory(questionnaire=questionnaire)

        questionnaire_filter = QuestionnaireFilterForm(self.form_data)
        self.assertIn(('', 'Choose a year'), questionnaire_filter.fields['year'].choices)
        self.assertNotIn((date.today().year + 1, date.today().year + 1), questionnaire_filter.fields['year'].choices)


class PublishQuestionnaireFormTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.FINALIZED,
                                                          year=2013)
        self.who = Organization.objects.create(name="WHO")
        self.afro = Region.objects.create(name="The Afro", organization=self.who)
        self.paho = Region.objects.create(name="The Paho", organization=self.who)

        self.form_data = {
            'questionnaire': self.questionnaire.id,
            'regions': [self.paho.id, self.afro.id]}

    def test_valid(self):
        publish_questionnaire_form = PublishQuestionnaireForm(initial={'questionnaire': self.questionnaire},
                                                              data=self.form_data)
        self.assertTrue(publish_questionnaire_form.is_valid())
        self.assertIn((self.paho.id, self.paho.name), publish_questionnaire_form.fields['regions'].choices)
        self.assertIn((self.afro.id, self.afro.name), publish_questionnaire_form.fields['regions'].choices)

    def test_choices_only_has_regions_that_do_not_have_published_questionnaires(self):
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.PUBLISHED,
                                                     year=2013, region=self.afro)
        data = {'questionnaire': self.questionnaire, 'regions': [self.paho.id]}
        publish_questionnaire_form = PublishQuestionnaireForm(initial={'questionnaire': self.questionnaire}, data=data)
        self.assertTrue(publish_questionnaire_form.is_valid())
        region_choices = [choice for choice in publish_questionnaire_form.fields['regions'].choices]
        self.assertIn((self.paho.id, self.paho.name), region_choices)
        self.assertNotIn((self.afro.id, self.afro.name), region_choices)

    def test_choices_has_regions_when_questionnaire_is_archived(self):
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.ARCHIVED,
                                                     year=2013, region=self.afro)
        data = {'questionnaire': self.questionnaire, 'regions': [self.paho.id]}
        publish_questionnaire_form = PublishQuestionnaireForm(initial={'questionnaire': self.questionnaire}, data=data)
        self.assertTrue(publish_questionnaire_form.is_valid())
        region_choices = [choice for choice in publish_questionnaire_form.fields['regions'].choices]
        self.assertIn((self.paho.id, self.paho.name), region_choices)
        self.assertIn((self.afro.id, self.afro.name), region_choices)

    def test_creates_copies_for_regions_on_save(self):
        Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.PUBLISHED, year=2013,
                                     region=self.afro)
        pacific = Region.objects.create(name="haha", organization=self.who)
        asia = Region.objects.create(name="hehe", organization=self.who)

        data = {'questionnaire': self.questionnaire, 'regions': [self.paho.id, pacific.id, asia.id]}

        publish_questionnaire_form = PublishQuestionnaireForm(initial={'questionnaire': self.questionnaire}, data=data)
        self.assertTrue(publish_questionnaire_form.is_valid())
        publish_questionnaire_form.save()
        questionnaires = Questionnaire.objects.filter(year=self.questionnaire.year)
        self.assertEqual(5, questionnaires.count())
        [self.assertEqual(1, region.questionnaire.all().count()) for region in [self.paho, pacific, asia]]
        self.assertEqual(1, self.afro.questionnaire.all().count())
        questionnaire = Questionnaire.objects.filter(id=self.questionnaire.id)[0]
        self.assertEqual(questionnaire.status, Questionnaire.PUBLISHED)


class EditQuestionnaireFormTest(BaseTest):
    def setUp(self):
        self.questionnaire_1 = QuestionnaireFactory(name="JRF 2011 Core English",
                                                    status=Questionnaire.PUBLISHED,
                                                    year=2016)
        self.draft_questionnaire = QuestionnaireFactory(name="JRF 2012 Core English",
                                                        status=Questionnaire.DRAFT,
                                                        year=2017)
        self.who = OrganizationFactory(name="WHO")
        self.afro = RegionFactory(name="The Afro", organization=self.who)
        self.this_year = date.today().year

        self.form_data = {
            'name': self.draft_questionnaire.name,
            'year': self.this_year
        }

    def test_valid(self):
        edit_questionnaire_form = EditQuestionnaireForm(initial={'questionnaire': self.draft_questionnaire},
                                                        data=self.form_data)

        self.assertTrue(edit_questionnaire_form.is_valid())
        for i in range(self.this_year, self.this_year + 10):
            self.assertIn((i, i), edit_questionnaire_form.fields['year'].choices)

    def test_year_for_published_questionnaire_without_answers_is_valid(self):
        three_years_from_now = self.this_year + 3
        form_data = self.form_data.copy()
        form_data['year'] = three_years_from_now

        QuestionnaireFactory(name="JRF 2011 Core English",
                             status=Questionnaire.PUBLISHED,
                             year=three_years_from_now,
                             parent=self.questionnaire_1,
                             region=RegionFactory(name='AFRO'))

        edit_questionnaire_form = EditQuestionnaireForm(instance=self.questionnaire_1, data=form_data)

        self.assertTrue(edit_questionnaire_form.is_valid())
        self.assertIn((three_years_from_now, three_years_from_now), edit_questionnaire_form.fields['year'].choices)

    def test_save_archives_regional_adapttions_from_the_revision_s_year(self):
        three_years_from_now = self.this_year + 3
        form_data = self.form_data.copy()
        form_data['year'] = 2016

        QuestionnaireFactory(name="JRF 2011 Core English",
                             status=Questionnaire.PUBLISHED,
                             year=three_years_from_now,
                             parent=self.questionnaire_1,
                             region=self.afro)
        edit_questionnaire_form = EditQuestionnaireForm(instance=self.draft_questionnaire, data=form_data)

        self.assertTrue(edit_questionnaire_form.is_valid())
        edit_questionnaire_form.save()
        self.assertTrue(Questionnaire.objects.get(id=self.questionnaire_1.id).is_archived())
        self.assertEqual(Questionnaire.objects.get(id=self.draft_questionnaire.id).year, 2016)

    def test_year_for_published_questionnaire_with_answers_is_invalid(self):
        three_years_from_now = self.this_year + 3
        form_data = self.form_data.copy()
        form_data['year'] = three_years_from_now

        questionnaire_1 = QuestionnaireFactory(name="JRF 2011 Core English",
                                               status=Questionnaire.PUBLISHED,
                                               year=three_years_from_now)
        child_questionnaire = QuestionnaireFactory(name="JRF 2011 Core English child", parent=questionnaire_1)
        NumericalAnswerFactory(questionnaire=child_questionnaire)
        edit_questionnaire_form = EditQuestionnaireForm(initial={'questionnaire': questionnaire_1},
                                                        data=form_data)

        self.assertFalse(edit_questionnaire_form.is_valid())
        self.assertNotIn((three_years_from_now, three_years_from_now), edit_questionnaire_form.fields['year'].choices)