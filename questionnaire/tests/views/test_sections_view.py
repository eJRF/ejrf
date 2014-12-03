import json
from urllib import quote

from django.core.urlresolvers import reverse
from django.test import Client

from questionnaire.forms.sections import SectionForm, SubSectionForm
from questionnaire.models import Questionnaire, Section, SubSection, Region, QuestionGroupOrder, SkipRule
from questionnaire.tests.base_test import BaseTest
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.question_group_factory import QuestionGroupFactory
from questionnaire.tests.factories.section_factory import SectionFactory
from questionnaire.tests.factories.skip_rule_factory import SkipQuestionRuleFactory, SkipSubsectionRuleFactory
from questionnaire.tests.factories.sub_section_factory import SubSectionFactory


class SectionsViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.region = None

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)
        self.section = SectionFactory(questionnaire=self.questionnaire)
        self.url = '/questionnaire/entry/%s/section/new/' % self.questionnaire.id
        self.form_data = {'name': 'New section',
                          'description': 'funny section',
                          'title': 'some title',
                          'questionnaire': self.questionnaire.id,
                          'order': 1}

    def test_get_create_section(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn("sections/subsections/new.html", templates)
        self.assertIsNotNone(response.context['form'])
        self.assertIsInstance(response.context['form'], SectionForm)
        self.assertEqual("CREATE", response.context['btn_label'])

    def test_post_create_section(self):
        self.failIf(Section.objects.filter(**self.form_data))
        response = self.client.post(self.url, data=self.form_data)
        section = Section.objects.get(**self.form_data)
        self.failUnless(section)
        self.assertEqual(self.region, section.region)
        self.assertRedirects(response,
                             expected_url='/questionnaire/entry/%s/section/%s/' % (self.questionnaire.id, section.id))

    def test_permission_required_for_create_section(self):
        self.assert_permission_required(self.url)

        user_not_in_same_region = self.create_user(username="asian_chic", group=self.REGIONAL_ADMIN, region="ASEAN",
                                                   org="WHO")
        self.assign('can_edit_questionnaire', user_not_in_same_region)

        self.client.logout()
        self.client.login(username='asian_chic', password='pass')
        response = self.client.get(self.url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(self.url),
                             status_code=302, target_status_code=200, msg_prefix='')

    def test_post_invalid(self):
        Section.objects.create(name="Some", order=1, questionnaire=self.questionnaire)
        form_data = self.form_data.copy()
        form_data['name'] = ''
        self.failIf(Section.objects.filter(**form_data))
        response = self.client.post(self.url, data=form_data)
        section = Section.objects.filter(order=2, name=form_data['name'])
        self.failIf(section)
        self.assertIn('Section NOT created. See errors below.', response.content)
        self.assertIsInstance(response.context['form'], SectionForm)
        self.assertEqual("new-section-modal", response.context['id'])
        self.assertEqual("CREATE", response.context['btn_label'])


class EditSectionsViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.region = None

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)

        self.form_data = {'name': 'section',
                          'description': 'funny section',
                          'title': 'some title',
                          'order': 1,
                          'questionnaire': self.questionnaire.id}
        self.create_form_data = self.form_data.copy()
        del self.create_form_data['questionnaire']
        self.section = Section.objects.create(region=self.region, questionnaire=self.questionnaire,
                                              **self.create_form_data)
        self.url = '/section/%d/edit/' % self.section.id

    def test_get_edit_section(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn("sections/subsections/new.html", templates)
        self.assertIsNotNone(response.context['form'])
        self.assertIsInstance(response.context['form'], SectionForm)
        self.assertEqual(self.section, response.context['form'].instance)
        self.assertEqual("SAVE", response.context['btn_label'])

    def test_post_create_section(self):
        data = self.form_data.copy()
        data['name'] = 'Edited section name'
        self.failIf(Section.objects.filter(**data))
        response = self.client.post(self.url, data=data)
        section = Section.objects.get(**data)
        self.failUnless(section)
        self.assertRedirects(response,
                             expected_url='/questionnaire/entry/%s/section/%s/' % (self.questionnaire.id, section.id))
        self.assertIn('Section updated successfully.', response.cookies['messages'].value)

    def test_permission_required_for_create_section(self):
        self.assert_permission_required(self.url)

        user_not_in_same_region = self.create_user(username="asian_chic", group=self.REGIONAL_ADMIN, region="ASEAN",
                                                   org="WHO")
        self.assign('can_edit_questionnaire', user_not_in_same_region)

        self.client.logout()
        self.client.login(username='asian_chic', password='pass')
        response = self.client.post(self.url, data=self.create_form_data)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(self.url),
                             status_code=302, target_status_code=200, msg_prefix='')

    def test_post_invalid(self):
        form_data = self.form_data.copy()
        form_data['name'] = ''
        self.failIf(Section.objects.filter(**form_data))
        response = self.client.post(self.url, data=form_data)
        section = Section.objects.filter(**form_data)
        self.failIf(section)
        self.assertIn('Section NOT updated. See errors below.', response.content)
        self.assertIsInstance(response.context['form'], SectionForm)
        self.assertEqual("SAVE", response.context['btn_label'])

    def test_sections_owned_by_others_cannot_be_edited(self):
        region = Region.objects.create(name="SEAR")
        section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1, region=region)
        url = '/section/%d/edit/' % section.id
        response = self.client.get(url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % url)
        response = self.client.post(url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % url)


    def test_updates_section_with_users_region(self):
        client = Client()
        user = self.create_user(username='new-user', group=self.REGIONAL_ADMIN, org="WHO", region='AFRO')
        region = user.user_profile.region
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=region)
        section = Section.objects.create(name="section", questionnaire=questionnaire, order=1, region=region)

        self.assign('can_edit_questionnaire', user)
        client.login(username=user.username, password='pass')
        form_data = {'name': 'section edited',
                          'description': 'funny section',
                          'title': 'some title',
                          'order': 1,
                          'questionnaire': questionnaire.id}

        url = '/section/%d/edit/' % section.id
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        response = client.post(url, data=form_data)

        edited = Section.objects.get(id=section.id)
        self.assertEqual(edited.region, region)
        self.assertEqual(edited.title, form_data['title'])
        self.assertEqual(edited.name, form_data['name'])


class DeleteSectionsViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.region = None
        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013,
                                                          region=self.region)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1,
                                              region=self.region, is_core=True)
        self.section_1 = Section.objects.create(name="section 2", questionnaire=self.questionnaire, order=2
                                                , region=self.region, is_core=True)
        self.url = '/section/%d/delete/' % self.section.id

    def test_post_deletes_section(self):
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)
        self.client.post(self.url, HTTP_REFERER=referer_url)
        self.assertNotIn(self.section, Section.objects.all())

    def test_successful_post_redirect_to_referer_url_if_not_deleting_self(self):
        delete_url = '/section/%d/delete/' % self.section_1.id
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)
        response = self.client.post(delete_url, data={}, HTTP_REFERER=referer_url)
        self.assertRedirects(response, referer_url)

    def test_successful_post_redirect_to_first_section_if_referer_url_is_self(self):
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)
        response = self.client.post(self.url, data={}, HTTP_REFERER=referer_url)
        self.assertRedirects(response,
                             reverse('questionnaire_entry_page', args=(self.questionnaire.id, self.section_1.id)))

    def test_successful_post_display_success_message(self):
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section_1.id)
        meta = {'HTTP_REFERER': referer_url}
        response = self.client.post(self.url, data={}, **meta)
        message = "Section successfully deleted."
        self.assertIn(message, response.cookies['messages'].value)

    def test_successful_deletion_of_section_reindexes_section_orders(self):
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section_1.id)
        meta = {'HTTP_REFERER': referer_url}
        section_3 = Section.objects.create(name="section", questionnaire=self.questionnaire, order=3,
                                           region=self.region, is_core=True)
        Section.objects.create(name="section 2", questionnaire=self.questionnaire, order=4)
        self.client.post('/section/%d/delete/' % section_3.id, data={}, **meta)
        self.assertEqual([1, 2, 3], list(Section.objects.values_list('order', flat=True)))

    def test_sections_owned_by_others_cannot_be_deleted(self):
        region = Region.objects.create(name="SEAR")
        section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1, region=region)
        url = '/section/%d/delete/' % section.id
        response = self.client.get(url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % url)
        response = self.client.post(url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % url)


class RegionalDeleteSectionTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.REGIONAL_ADMIN, org="WHO", region="AFRO")
        self.region = self.user.user_profile.region
        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013,
                                                          region=self.region)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1,
                                              region=self.region, is_core=True)
        self.section_1 = Section.objects.create(name="section 2", questionnaire=self.questionnaire, order=2
                                                , region=self.region, is_core=True)
        self.url = '/section/%d/delete/' % self.section.id

    def test_sections_that_are_core_cannot_be_deleted(self):
        expected_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)
        meta = {'HTTP_REFERER': expected_url}
        response = self.client.post(self.url, data={}, **meta)

        self.assertRedirects(response, expected_url=expected_url)
        message = 'You are not permitted to delete a core section'
        self.assertIn(message, response.cookies['messages'].value)


class SubSectionsViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.region = None

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1, is_core=True)
        self.url = '/questionnaire/entry/%s/section/%s/subsection/new/' % (self.questionnaire.id, self.section.id)
        self.form_data = {
            'description': 'funny section',
            'title': 'some title',
        }

    def test_get_create_subsection(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn("sections/subsections/new.html", templates)
        self.assertIsNotNone(response.context['form'])
        self.assertIsInstance(response.context['form'], SubSectionForm)
        self.assertEqual("CREATE", response.context['btn_label'])

    def test_post_create_subsection(self):
        self.failIf(SubSection.objects.filter(section=self.section, **self.form_data))
        response = self.client.post(self.url, data=self.form_data)
        subsection = SubSection.objects.filter(section=self.section, **self.form_data)
        self.failUnless(subsection)
        self.assertEqual(1, subsection.count())
        self.assertIn('Subsection successfully created.', response.cookies['messages'].value)
        self.assertRedirects(response, expected_url='/questionnaire/entry/%s/section/%s/' % (
            self.questionnaire.id, self.section.id))

    def test_post_with_form_increments_order_before_saving(self):
        SubSection.objects.create(title="Some", order=1, section=self.section)
        form_data = self.form_data.copy()
        form_data['title'] = 'Another subsection'
        self.failIf(SubSection.objects.filter(section=self.section, **form_data))
        response = self.client.post(self.url, data=form_data)
        subsection = SubSection.objects.filter(order=2, title=form_data['title'])
        self.failUnless(subsection)
        self.assertEqual(1, subsection.count())
        self.assertRedirects(response, expected_url='/questionnaire/entry/%s/section/%s/' % (
            self.questionnaire.id, self.section.id))

    def test_permission_required_for_create_section(self):
        self.assert_permission_required(self.url)

        user_not_in_same_region = self.create_user(username="asian_chic", group=self.REGIONAL_ADMIN, region="ASEAN",
                                                   org="WHO")
        self.assign('can_edit_questionnaire', user_not_in_same_region)

        self.client.logout()
        self.client.login(username='asian_chic', password='pass')
        response = self.client.get(self.url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(self.url),
                             status_code=302, target_status_code=200, msg_prefix='')

    def test_post_invalid(self):
        SubSection.objects.create(title="Some", order=1, section=self.section)
        form_data = self.form_data.copy()
        form_data['title'] = ''
        self.failIf(SubSection.objects.filter(section=self.section, **form_data))
        response = self.client.post(self.url, data=form_data)
        subsection = SubSection.objects.filter(order=2, title=form_data['title'])
        self.failUnless(subsection)
        self.assertEqual('', subsection[0].title)


class EditSubSectionsViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.region = None

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)
        self.section = Section.objects.create(questionnaire=self.questionnaire, name="section", order=1, is_core=True)
        self.form_data = {'description': 'funny section',
                          'title': 'some title',
                          'order': 1,
                          'section': self.section.id}
        self.create_form_data = self.form_data.copy()
        del self.create_form_data['section']
        self.subsection = SubSection.objects.create(section=self.section, region=self.region, is_core=True, **self.create_form_data)
        self.url = '/subsection/%d/edit/' % self.subsection.id

    def test_get_edit_section(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn("sections/subsections/new.html", templates)
        self.assertIsNotNone(response.context['form'])
        self.assertIsInstance(response.context['form'], SubSectionForm)
        self.assertEqual(self.subsection, response.context['form'].instance)
        self.assertEqual("SAVE", response.context['btn_label'])

    def test_post_create_section(self):
        data = self.form_data.copy()
        data['title'] = 'Edited subsection name'
        del data['order']
        self.failIf(SubSection.objects.filter(**data))
        response = self.client.post(self.url, data=data)
        subsection = SubSection.objects.get(**data)
        self.assertRedirects(response, expected_url=self.subsection.get_absolute_url())
        self.failUnless(subsection)
        self.assertIn('SubSection updated successfully.', response.cookies['messages'].value)

    def test_permission_required_for_edit_section(self):
        self.assert_login_required(self.url)
        self.assert_permission_required(self.url)

    def test_subsections_owned_by_others_cannot_be_edited(self):
        region = Region.objects.create(name="SEAN")
        sub_section = SubSection.objects.create(title="Cured Cases of Measles 3", order=3, section=self.section,
                                                region=region)
        url = '/subsection/%d/delete/' % sub_section.id
        response = self.client.get(url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % url)
        response = self.client.post(url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % url)

    def test_post_invalid(self):
        form_data = self.form_data.copy()
        form_data['title'] = ''
        self.failIf(SubSection.objects.filter(**form_data))
        response = self.client.post(self.url, data=form_data)
        section = SubSection.objects.filter(**form_data)
        self.failUnless(section)
        self.assertEqual('', section[0].title)


class MoveSubsectionTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.region = None

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.subsection = SubSectionFactory(order=1)

        self.section = self.subsection.section

        self.subsection2 = SubSectionFactory(order=2, section=self.section)
        self.subsection3 = SubSectionFactory(order=3, section=self.section)

        self.url = '/subsection/move/'

    def test_that_reorder_service_gets_called(self):
        new_order = 2

        response = self.client.post(self.url, data={'subsection': self.subsection.id,
                                                    'modal-subsection-position': new_order})
        self.assertEqual(302, response.status_code)
        self.assertIn("", response.cookies['messages'].value)


class DeleteSubSectionsViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.region = None

        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1,
                                              region=self.region)
        self.form_data = {'description': 'First Section',
                          'title': 'Title for First Section',
                          'order': 1,
                          'section': self.section.id}
        self.create_form_data = self.form_data.copy()
        del self.create_form_data['section']
        self.subsection = SubSection.objects.create(section=self.section, region=self.region, is_core=True, **self.create_form_data)
        self.url = '/subsection/%d/delete/' % self.subsection.id

    def test_post_deletes_subsection(self):
        response = self.client.post(self.url)
        self.assertNotIn(self.subsection, SubSection.objects.all())

    def test_successful_post_redirect_to_referrer_url(self):
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)
        meta = {'HTTP_REFERER': referer_url}
        response = self.client.post(self.url, data={}, HTTP_REFERER=referer_url)
        self.assertRedirects(response, referer_url)

    def test_successful_post_display_success_message(self):
        response = self.client.post(self.url)
        message = "Subsection successfully deleted."
        self.assertIn(message, response.cookies['messages'].value)

    def test_successful_deletion_reindexes_subsections(self):
        sub_section1 = SubSection.objects.create(title="Cured Cases of Measles 3", order=2, section=self.section)
        sub_section2 = SubSection.objects.create(title="Cured Cases of Measles 3", order=3, section=self.section,
                                                 region=self.region, is_core=True)
        sub_section3 = SubSection.objects.create(title="Cured Cases of Measles 3", order=4, section=self.section)
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)
        meta = {'HTTP_REFERER': referer_url}
        self.client.post('/subsection/%d/delete/' % sub_section2.id, data={}, **meta)
        self.assertEqual([1, 2, 3], list(SubSection.objects.values_list('order', flat=True)))

    def test_subsections_owned_by_others_cannot_be_deleted(self):
        region = Region.objects.create(name="SEAN")
        sub_section = SubSection.objects.create(title="Cured Cases of Measles 3", order=3, section=self.section,
                                                region=region)
        url = '/subsection/%d/delete/' % sub_section.id
        response = self.client.get(url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % url)
        response = self.client.post(url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % url)

    def test_post_deletes_subsection_and_rules(self):
        SkipQuestionRuleFactory(subsection=self.subsection)
        SkipSubsectionRuleFactory(subsection=self.subsection)
        self.client.post(self.url)

        self.assertEqual(len(SkipRule.objects.all()), 0)

    def test_post_deletes_subsection_and_rules_where_it_is_subsection_to_skip(self):
        SkipSubsectionRuleFactory(skip_subsection=self.subsection)
        self.client.post(self.url)

        self.assertEqual(len(SkipRule.objects.all()), 0)

class DeleteRegionalSectionsViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.REGIONAL_ADMIN, org="WHO", region="AFRO")
        self.region = self.user.user_profile.region
        self.assign('can_edit_questionnaire', self.user)
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1,
                                              region=self.region)
        self.section1 = Section.objects.create(name="section1", questionnaire=self.questionnaire, order=2,
                                               region=self.region)
        self.subsection = SubSection.objects.create(title="subsection 1", section=self.section, order=1,
                                                    region=self.region)
        self.user = self.assign('can_edit_questionnaire', self.user)

    def test_post_deletes_section_that_belongs_to_your_region(self):
        client = Client()
        client.login(username=self.user.username, password='pass')
        url = '/section/%s/delete/' % self.section.id
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)
        response = client.post(url, HTTP_REFERER=referer_url)
        self.assertRedirects(response, expected_url=self.questionnaire.absolute_url())
        self.assertRaises(Section.DoesNotExist, Section.objects.get, id=self.section.id)

    def test_post_delete_section_spares_section_thats_not_for_your_region(self):
        client = Client()
        user_not_in_same_region = self.create_user(username="asian_chic", group=self.REGIONAL_ADMIN, region="ASEAN",
                                                   org="WHO")
        self.assign('can_edit_questionnaire', user_not_in_same_region)
        client.login(username=user_not_in_same_region.username, password='pass')

        paho = Region.objects.create(name="paho")
        section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1, region=paho)

        url = '/section/%s/delete/' % section.id
        self.assert_permission_required(url)

        response = client.post(url)
        self.failUnless(Section.objects.filter(id=section.id))
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(url))


class DeleteRegionalSubSectionsViewTest(BaseTest):
    def setUp(self):
        self.user = self.create_user(group=self.REGIONAL_ADMIN, org="WHO", region="AFRO")
        self.region = self.user.user_profile.region
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1,
                                              region=self.region)
        self.section1 = Section.objects.create(name="section1", questionnaire=self.questionnaire, order=2,
                                               region=self.region)
        self.subsection = SubSection.objects.create(title="subsection 1", section=self.section, order=1,
                                                    region=self.region)
        self.user = self.assign('can_edit_questionnaire', self.user)

    def test_post_deletes_subsection_that_belongs_to_your_region(self):
        client = Client()
        client.login(username=self.user.username, password='pass')
        url = '/subsection/%s/delete/' % self.subsection.id
        referer_url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section.id)
        response = client.post(url, HTTP_REFERER=referer_url)
        self.assertRaises(SubSection.DoesNotExist, SubSection.objects.get, id=self.section.id)
        self.assertRedirects(response, expected_url=self.questionnaire.absolute_url())

    def test_post_delete_subsection_spares_section_thats_not_for_your_region(self):
        client = Client()
        user_not_in_same_region = self.create_user(username="asian_chic", group=self.REGIONAL_ADMIN, region="ASEAN",
                                                   org="WHO")
        self.assign('can_edit_questionnaire', user_not_in_same_region)
        self.assign('can_edit_questionnaire', self.user)
        client.login(username=user_not_in_same_region.username, password='pass')

        section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1, region=self.region)
        subsection = SubSection.objects.create(title="subsection 1", section=section, order=1, region=self.region)

        url = '/subsection/%s/delete/' % subsection.id
        self.assert_permission_required(url)

        response = client.post(url)
        self.failUnless(SubSection.objects.filter(id=subsection.id))
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(url))

    def test_post_delete_subsection_spares_section_that_are_core(self):
        client = Client()
        regional_admin_user = self.create_user(username="asian_chic", group=self.REGIONAL_ADMIN, region="ASEAN",
                                                   org="WHO")
        region = regional_admin_user.user_profile.region
        self.assign('can_edit_questionnaire', regional_admin_user)
        self.assign('can_edit_questionnaire', self.user)

        client.login(username=regional_admin_user.username, password='pass')

        section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1, region=region,
                                         is_core=True)
        subsection = SubSection.objects.create(title="subsection 1", section=section, order=1, region=region,
                                               is_core=True)

        url = '/subsection/%s/delete/' % subsection.id

        self.assert_permission_required(url)

        response = client.post(url)
        self.failUnless(SubSection.objects.filter(id=subsection.id))

        self.assertRedirects(response, expected_url=section.get_absolute_url(), target_status_code=302)
        message = 'You are not permitted to delete a core subsection'
        self.assertIn(message, response.cookies['messages'].value)


class SectionGetSubSectionsTest(BaseTest):
    def setUp(self):
        self.user = self.create_user(group=self.REGIONAL_ADMIN, org="WHO", region="AFRO")
        self.user = self.assign('can_edit_questionnaire', self.user)

        self.client = Client()
        self.client.login(username=self.user.username, password='pass')

        self.region = self.user.user_profile.region
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=self.region)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1,
                                              region=self.region)
        self.url = '/questionnaire/section/%d/subsections/' % self.section.id

    def test_gets_subsections_for_a_section_with_no_subsections(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual([], json.loads(response.content))

    def test_gets_subsections_for_a_section_with_one_subsection(self):
        subsection = SubSection.objects.create(title="subsection 1", section=self.section, order=1,
                                               region=self.region, is_core=False)

        core_subsection = SubSection.objects.create(title="subsection 1", section=self.section, order=2,
                                               region=self.region, is_core=True)

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual([{'title': 'subsection 1', 'id': subsection.id, 'order': 1}], json.loads(response.content))


class MoveGridViewTest(BaseTest):
    def setUp(self):
        self.user = self.create_user(org="WHO")
        self.user = self.assign('can_edit_questionnaire', self.user)

        self.client = Client()
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1)

        self.url = '/grid/move/'

        self.subsection = SubSectionFactory(section=self.section)
        self.question_group1 = QuestionGroupFactory(subsection=self.subsection, order=1, grid=True)
        self.question_group2 = QuestionGroupFactory(subsection=self.subsection, order=2, grid=True)
        self.question_group3 = QuestionGroupFactory(subsection=self.subsection, order=3)
        self.question_group4 = QuestionGroupFactory(subsection=self.subsection, order=4, grid=True)

        self.question = QuestionFactory()
        self.question_group3.question.add(self.question)
        QuestionGroupOrder.objects.create(question=self.question, question_group=self.question_group3, order=1)

    def test_redirects_with_correct_message_when_its_the_first_in_the_subsection(self):
        form_data = {'move_direction': 'up', 'group_id': self.question_group1.id}

        response = self.client.post(self.url, data=form_data)

        warning_message = 'The Grid was not moved up because its the first in this subsection'
        self.assertRedirects(response, self.section.get_absolute_url())
        self.assertIn(warning_message, response.cookies['messages'].value)

    def test_redirects_with_correct_message_when_its_the_last_in_the_subsection(self):
        form_data = {'move_direction': 'down', 'group_id': self.question_group4.id}

        response = self.client.post(self.url, data=form_data)

        warning_message = 'The Grid was not moved down because its the last in this subsection'
        self.assertRedirects(response, self.section.get_absolute_url())
        self.assertIn(warning_message, response.cookies['messages'].value)

    def test_redirects_with_correct_message_when_its_the_second_group_in_the_subsection_moving_down(self):
        form_data = {'move_direction': 'down', 'group_id': self.question_group1.id}

        response = self.client.post(self.url, data=form_data)

        success_message = 'The Grid was successfully moved down'
        self.assertRedirects(response, self.section.get_absolute_url())
        self.assertIn(success_message, response.cookies['messages'].value)

    def test_redirects_with_correct_message_when_its_the_second_group_in_the_subsection_moving_up(self):
        form_data = {'move_direction': 'up', 'group_id': self.question_group2.id}

        response = self.client.post(self.url, data=form_data)

        success_message = 'The Grid was successfully moved up'
        self.assertRedirects(response, self.section.get_absolute_url())
        self.assertIn(success_message, response.cookies['messages'].value)