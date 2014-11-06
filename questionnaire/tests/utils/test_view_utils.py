from django.contrib.auth.models import User
from django.test.client import RequestFactory

from questionnaire.models import Questionnaire, UserProfile, Organization, Region, Country
from questionnaire.tests.base_test import BaseTest
from questionnaire.utils.view_utils import get_country, get_questionnaire_status, get_regions


class ViewUtilTest(BaseTest):
    def setUp(self):
        self.user = self.create_user(group=self.DATA_SUBMITTER, country="Uganda", region="AFRO")
        self.uganda = self.user.user_profile.country
        self.region = self.user.user_profile.country.regions.all()[0]
        self.factory = RequestFactory()

    def test_gets_country_from_request(self):
        request = self.factory.get('/')
        request.user = self.user
        self.assertEqual(self.uganda, get_country(request))

    def test_gets_country_from_get_params(self):
        organization = Organization.objects.create(name="WHO")
        user = User.objects.create(username="some user", email="user2@mail.com")
        UserProfile.objects.create(user=user, organization=organization)
        request = self.factory.get('/?country=%s' % self.uganda.id)
        request.user = user
        self.assertEqual(self.uganda, get_country(request))

    def test_gets_questionnaire_status_for_global_admin_user(self):
        self.assign('can_edit_questionnaire', self.user)
        request = self.factory.get('/')
        request.user = self.user
        questionnaire_status = get_questionnaire_status(request)
        self.assertEqual(3, len(questionnaire_status))
        [self.assertIn(status, questionnaire_status) for status in
         [Questionnaire.PUBLISHED, Questionnaire.DRAFT, Questionnaire.FINALIZED]]

    def test_gets_questionnaire_status_for_data_submitter_user(self):
        user = self.create_user(username="Ugandauser", group=self.GLOBAL_ADMIN, org="WHO")
        self.assign('can_submit_responses', user)
        request = self.factory.get('/')
        request.user = user
        questionnaire_status = get_questionnaire_status(request)
        self.assertEqual(1, len(questionnaire_status))
        [self.assertIn(status, questionnaire_status) for status in [Questionnaire.PUBLISHED]]

    def test_gets_region_from_get_params(self):
        organization = Organization.objects.create(name="WHO")
        user = User.objects.create(username="some user", email="user2@mail.com")
        UserProfile.objects.create(user=user, organization=organization)
        request = self.factory.get('/')
        request.user = user
        self.assertEqual(None, get_regions(request))

    def test_gets_region_from_get_user_request(self):
        kenya = Country.objects.create(name="Kenya")
        region = Region.objects.create(name="Afro")
        region.countries.add(kenya)

        user = User.objects.create(username="some user", email="user2@mail.com")
        UserProfile.objects.create(user=user, country=kenya)

        request = self.factory.get('/')
        request.user = self.user
        self.assertEqual(1, len(get_regions(request)))
        self.assertIn(self.region, get_regions(request))