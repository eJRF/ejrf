from questionnaire.forms.sections import SectionForm, SubSectionForm
from questionnaire.models import Questionnaire, Section, SubSection
from questionnaire.tests.base_test import BaseTest
from questionnaire.tests.factories.questionnaire_factory import QuestionnaireFactory
from questionnaire.tests.factories.section_factory import SectionFactory
from questionnaire.tests.factories.region_factory import RegionFactory


class CoreSectionFormTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        self.user = self.create_user(username='some user', group=self.GLOBAL_ADMIN, org='WHO')
        self.region = self.user.user_profile.region
        self.section1 = SectionFactory(questionnaire=self.questionnaire, order=1, name='Section 1')
        self.section2 = SectionFactory(questionnaire=self.questionnaire, order=2, name='Section 2')
        self.section3 = SectionFactory(questionnaire=self.questionnaire, order=3, name='Section 3')
        self.form_data = {'name': 'New section',
                          'description': 'funny section',
                          'title': 'some title',
                          'questionnaire': self.questionnaire.id,
                          'order': 1}

    def test_valid(self):
        section_form = SectionForm(initial={'questionnaire': self.questionnaire.id}, data=self.form_data)
        self.assertTrue(section_form.is_valid())

    def test_valid_with_initial(self):
        initial = {'questionnaire': self.questionnaire.id, 'region': self.region, 'user': self.user}
        section_form = SectionForm(data=self.form_data, initial=initial)

        self.assertTrue(section_form.is_valid())
        section = section_form.save()
        self.assertEqual(section.region, self.region)
        self.assertTrue(section.is_core)

    def test_that_sections_are_reordered_after_save(self):
        section_form = SectionForm(instance=self.section3,
                                   data=self.form_data, initial={'questionnaire': self.questionnaire.id})
        section_form.save()
        self.assertEqual(1, self.section3.order)

        self.assertEqual(2, Section.objects.get(id=self.section1.id).order)
        self.assertEqual(3, Section.objects.get(id=self.section2.id).order)

    def test_section_form_order_options_include_only_existing_orders_when_editing(self):
        section_form = SectionForm(instance=self.section3,
                                   data=self.form_data, initial={'questionnaire': self.questionnaire.id})
        expected_choices = [(self.section1.order, self.section1.order),
                            (self.section2.order, self.section2.order),
                            (self.section3.order, self.section3.order)]

        choices = section_form.fields['order'].choices
        [self.assertIn(choice, choices) for choice in expected_choices]

    def test_section_form_order_options_include_existing_orders_and_one_extra_choice_bigger_than_largest_order(self):
        section_form = SectionForm(data=self.form_data, initial={'questionnaire': self.questionnaire.id})

        expected_choices = [(self.section1.order, self.section1.order),
                            (self.section2.order, self.section2.order),
                            (self.section3.order, self.section3.order),
                            (self.section3.order + 1, self.section3.order + 1), ]

        choices = section_form.fields['order'].choices
        [self.assertIn(choice, choices) for choice in expected_choices]

    def test_that_a_new_section_created_get_max_order_plus_one(self):
        questionnaire = QuestionnaireFactory()

        section1 = SectionFactory(order=1, questionnaire=questionnaire)
        section2 = SectionFactory(order=2, questionnaire=questionnaire)
        section3 = SectionFactory(order=3, questionnaire=questionnaire)
        section4 = SectionFactory(order=4, questionnaire=questionnaire)
        section5 = SectionFactory(order=1, title='Not in the same questionnaire')
        form_data = self.form_data
        form_data['order'] = 3
        form_data['questionnaire'] = questionnaire.id
        initial = {'questionnaire': questionnaire.id}

        section_form = SectionForm(data=form_data, initial=initial)

        saved_section = section_form.save()
        self.assertEqual(3, saved_section.order)

        self.assertEqual(1, Section.objects.get(id=section1.id).order)
        self.assertEqual(2, Section.objects.get(id=section2.id).order)

        self.assertEqual(4, Section.objects.get(id=section3.id).order)
        self.assertEqual(5, Section.objects.get(id=section4.id).order)


class PermissionBasedValidationTest(CoreSectionFormTest):
    def test_is_invalid_when_user_is_regional_and_editing_core_section(self):
        questionnaire = QuestionnaireFactory()
        user = self.create_user(username='ra-user', group=self.REGIONAL_ADMIN, org="WHO", region='AFR')
        section1 = SectionFactory(order=1, questionnaire=questionnaire, is_core=True, region=user.user_profile.region)
        initial = {'questionnaire': questionnaire.id, 'user': user}

        section_form = SectionForm(data=self.form_data, initial=initial, instance=section1)
        self.assertFalse(section_form.is_valid())
        self.assertIn('You are not permitted to edit this section', section_form.errors['name'])

    def test_is_valid_when_user_is_regional_and_editing_none_core_section(self):
        questionnaire = QuestionnaireFactory()
        user = self.create_user(username='ra-user', group=self.REGIONAL_ADMIN, org="WHO", region='AFR')
        section1 = SectionFactory(order=1, questionnaire=questionnaire, is_core=False, region=user.user_profile.region)
        initial = {'questionnaire': questionnaire.id, 'user': user}

        section_form = SectionForm(data=self.form_data, initial=initial, instance=section1)
        self.assertTrue(section_form.is_valid())

    def test_is_invalid_when_user_is_global_and_editing_none_core_section(self):
        questionnaire = QuestionnaireFactory()
        region = RegionFactory()
        user = self.create_user(username='ra-user', group=self.GLOBAL_ADMIN, org="WHO")
        section1 = SectionFactory(order=1, questionnaire=questionnaire, is_core=False, region=region)
        initial = {'questionnaire': questionnaire.id, 'user': user}

        section_form = SectionForm(data=self.form_data, initial=initial, instance=section1)

        self.assertFalse(section_form.is_valid())
        self.assertIn('You are not permitted to edit this section', section_form.errors['name'])


class CoreSubSectionFormTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1)
        self.form_data = {'description': 'funny subsection',
                          'title': 'some subsection'}

    def test_valid(self):
        subsection_form = SubSectionForm(initial={'section': self.section.id}, data=self.form_data)
        self.assertTrue(subsection_form.is_valid())

    def test_empty_title_is_valid(self):
        data = self.form_data.copy()
        data['title'] = ''

        subsection_form = SubSectionForm(initial={'section': self.section.id}, data=data)

        self.assertTrue(subsection_form.is_valid())

    def test_empty_description_is_invalid(self):
        data = self.form_data.copy()
        data['description'] = ''

        subsection_form = SubSectionForm(initial={'section': self.section.id}, data=data)

        self.assertTrue(subsection_form.is_valid())

    def test_save_increment_order(self):
        existing_subs = SubSection.objects.create(title="subsection 1", section=self.section, order=1)
        data = self.form_data.copy()

        subsection_form = SubSectionForm(instance=SubSection(section=self.section), data=data)
        subsection_form.save()
        new_subs = SubSection.objects.filter(section=self.section, **data)
        self.failUnless(new_subs)
        self.assertEqual(1, new_subs.count())
        self.assertEqual(existing_subs.order + 1, new_subs[0].order)

    def test_save_does_not_increment_order_if_instance_of_section_is_given_and_it_has_order(self):
        subsection_order = 1
        existing_subs = SubSection.objects.create(title="subsection 1", section=self.section, order=subsection_order)
        data = self.form_data.copy()

        subsection_form = SubSectionForm(instance=existing_subs, data=data)
        subsection_form.save()
        new_subs = SubSection.objects.filter(section=self.section, **data)
        self.failUnless(new_subs)
        self.assertEqual(1, new_subs.count())
        self.assertEqual(subsection_order, new_subs[0].order)