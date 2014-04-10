from django.contrib.auth.models import User
from questionnaire.tests.base_test import BaseTest
from django.test.client import RequestFactory
from questionnaire.utils.view_utils import get_country


class ViewUtilTest(BaseTest):
    def setUp(self):
        self.user, self.uganda, self.region = self.create_user_with_no_permissions()
        self.factory = RequestFactory()

    def test_gets_country_from_request(self):
        request = self.factory.get('/')
        request.user = self.user
        self.assertEqual(self.uganda, get_country(request))

    def test_gets_country_from_get_params(self):
        user = User.objects.create(username="some user", email="user2@mail.com")
        request = self.factory.get('/?country=%s' % self.uganda.id)
        request.user = user
        self.assertEqual(self.uganda, get_country(request))