from django.contrib.auth.models import User

from questionnaire.models import Country
from questionnaire.models.users import UserProfile
from questionnaire.tests.base_test import BaseTest


class UserProfileTest(BaseTest):
    def test_user_fields(self):
        user_profile = UserProfile()
        fields = [str(item.attname) for item in user_profile._meta.fields]
        self.assertEqual(7, len(fields))
        for field in ['id', 'created', 'modified', 'user_id', 'country_id', 'region_id', 'organization_id']:
            self.assertIn(field, fields)

    def test_answer_stores(self):
        user = User.objects.create()
        uganda = Country.objects.create(name="Uganda")
        user_profile = UserProfile.objects.create(user=user, country=uganda)
        self.failUnless(user_profile.id)
        self.assertEqual(user, user_profile.user)