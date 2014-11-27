from django.contrib.auth.models import User

from questionnaire.models import Country
from questionnaire.models.users import UserProfile
from questionnaire.tests.base_test import BaseTest
from questionnaire.tests.factories.section_factory import SectionFactory


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

    def test_returns_true_if_section_is_core_and_user_is_global_admin(self):
        user = self.create_user(org="WHO")
        section = SectionFactory(is_core=True)

        self.assertTrue(user.user_profile.can_delete(section))

    def test_returns_false_when_section_is_core_and_user_is_region_admin(self):
        user = self.create_user(group=self.REGIONAL_ADMIN, org="WHO", region="AFRO")
        section = SectionFactory(is_core=True, region=user.user_profile.region)

        self.assertFalse(user.user_profile.can_delete(section))