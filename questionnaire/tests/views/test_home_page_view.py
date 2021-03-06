from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client

from questionnaire.models import Questionnaire, Section, Country, Region, Question, SubSection, QuestionGroup
from questionnaire.models.answers import NumericalAnswer, Answer
from questionnaire.tests.base_test import BaseTest


class HomePageViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.DATA_SUBMITTER, country="Uganda", region="AFRO")
        self.region = self.user.user_profile.country.regions.all()[0]
        self.country = self.user.user_profile.country
        self.assign('can_submit_responses', self.user)
        self.client.login(username=self.user.username, password='pass')
        self.questionnaire1 = Questionnaire.objects.create(name="JRF 2013 Core 1", year=2013, region=self.region,
                                                           status=Questionnaire.PUBLISHED)
        self.section_1 = Section.objects.create(title="Reported Cases", order=1, questionnaire=self.questionnaire1,
                                                name="Reported Cases")
        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                     section=self.section_1)
        question2 = Question.objects.create(text='C. Number of cases positive', UID='C00005', answer_type='Number')

        self.parent = QuestionGroup.objects.create(subsection=self.sub_section, order=1)
        self.parent.question.add(question2)
        self.answer = NumericalAnswer.objects.create(question=question2, country=self.country,
                                                     status=Answer.DRAFT_STATUS, response=22,
                                                     questionnaire=self.questionnaire1)

        self.questionnaire2 = Questionnaire.objects.create(name="JRF 2013 Core 2", year=2013, region=self.region,
                                                           status=Questionnaire.PUBLISHED)
        self.section_2_1 = Section.objects.create(title="Reported Cases", order=1, questionnaire=self.questionnaire2,
                                                  name="Reported Cases")
        self.sub_section_2_1 = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                         section=self.section_2_1)
        question_2_1 = Question.objects.create(text='C. Number of cases positive', UID='C00006', answer_type='Number')

        self.parent_2_1 = QuestionGroup.objects.create(subsection=self.sub_section_2_1, order=1)
        self.parent_2_1.question.add(question_2_1)

        self.questionnaire3 = Questionnaire.objects.create(name="JRF 2013 Core 3", year=2013, region=self.region,
                                                           status=Questionnaire.PUBLISHED)
        self.section_3_1 = Section.objects.create(title="Reported Cases", order=1, questionnaire=self.questionnaire3,
                                                  name="Reported Cases")
        self.question_3_1 = Question.objects.create(text='C. Number of cases positive', UID='C00007',
                                                    answer_type='Number')
        self.sub_section_3_1 = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                         section=self.section_3_1)
        self.parent_3_1 = QuestionGroup.objects.create(subsection=self.sub_section_3_1, order=1)
        self.parent_3_1.question.add(self.question_3_1)
        self.answer_3_1 = NumericalAnswer.objects.create(question=self.question_3_1, country=self.country,
                                                         status=Answer.SUBMITTED_STATUS, response=22,
                                                         questionnaire=self.questionnaire3)

    def test_get(self):
        self.questionnaire3.submissions.create(country=self.country, version=1)
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('home/submitter/index.html', templates)
        self.assertEqual({self.questionnaire1}, response.context['drafts'])
        self.assertEqual({self.questionnaire2: []}, response.context['new'])
        self.assertEqual({self.questionnaire3: [self.answer_3_1.version]}, response.context['submitted'])

    def test_new_questionnaire_with_same_question_on_submit_changes_status(self):
        questionnaire3_2 = Questionnaire.objects.create(name="JRF 2014 Core 3", year=2014, region=self.region,
                                                        status=Questionnaire.PUBLISHED)
        section_3_2 = Section.objects.create(title="Reported Cases", order=1, questionnaire=questionnaire3_2,
                                             name="Reported Cases")
        sub_section_3_2 = SubSection.objects.create(title="Reported cases for the year 2014", order=1,
                                                    section=section_3_2)
        parent_3_2 = QuestionGroup.objects.create(subsection=sub_section_3_2, order=1)
        parent_3_2.question.add(self.question_3_1)
        answer_3_2 = NumericalAnswer.objects.create(question=self.question_3_1, country=self.country,
                                                    status=Answer.DRAFT_STATUS, response=22,
                                                    questionnaire=questionnaire3_2)
        self.questionnaire3.submissions.create(country=self.country, version=1)
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('home/submitter/index.html', templates)
        self.assertIn(self.questionnaire3, response.context['submitted'])
        self.assertNotIn(self.questionnaire3, response.context['drafts'])
        self.assertIn(questionnaire3_2, response.context['drafts'])
        self.assertNotIn(questionnaire3_2, response.context['submitted'])

        questionnaire3_2.submissions.create(country=self.country, version=1)
        answer_3_2.status = Answer.SUBMITTED_STATUS
        answer_3_2.save()
        response = self.client.get("/")
        self.assertNotIn(questionnaire3_2, response.context['drafts'])
        self.assertIn(questionnaire3_2, response.context['submitted'])

    def test_login_required_for_home_get(self):
        self.assert_login_required('/')

    def test_homepage_redirects_to_manage_regional_jrf_when_logged_in_as_regional_admin(self):
        User.objects.all().delete()
        self.client.logout()
        user = self.create_user(group=self.REGIONAL_ADMIN, region="AFRO", org="WHO")
        region = user.user_profile.region
        self.assign('can_edit_questionnaire', user)
        self.client.login(username=user.username, password='pass')
        response = self.client.get("/")
        self.assertRedirects(response, expected_url=reverse('manage_regional_jrf_page', args=(region.id,)))


class GlobalAdminHomePageViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.assign('can_view_users', self.user)
        self.assign('can_edit_users', self.user)
        self.client.login(username=self.user.username, password='pass')
        self.afro = Region.objects.create(name="Afro")
        self.uganda = Country.objects.create(name="Uganda", code="UGX")
        self.rwanda = Country.objects.create(name="Rwanda", code="RWA")
        self.afro.countries.add(self.uganda, self.rwanda)

    def test_get(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('home/index.html', templates)
        self.assertIn(self.uganda, response.context['region_country_status_map'][self.afro])
        self.assertIn(self.rwanda, response.context['region_country_status_map'][self.afro])

    def test_login_required_for_home_get(self):
        self.assert_login_required('/')