from urllib import quote

from django.test import Client
from django.conf import settings

from questionnaire.tests.base_test import BaseTest
from django.test.utils import override_settings

from mock import patch

class ErrorPagesTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.assign('can_edit_questionnaire', self.user)
        self.client.login(username=self.user.username, password='pass')
        self.none_existing_url = '/unknown/resource/3/'

    def test_404(self):
        response = self.client.get(self.none_existing_url)

        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn("errors/404.html", templates)

    def test_permissions_required(self):
        self.assert_login_required(self.none_existing_url)
