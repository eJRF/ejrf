from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import Client
from questionnaire.forms.filter import UserFilterForm
from questionnaire.forms.user_profile import UserProfileForm
from questionnaire.models import Organization, Region, Country, UserProfile
from questionnaire.tests.base_test import BaseTest


class UsersViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user = self.create_user_with_no_permissions()
        self.login_user()
        self.global_admin = Group.objects.create(name='Global Admin')
        auth_content = ContentType.objects.get_for_model(Permission)
        permission, out = Permission.objects.get_or_create(codename='is_global_admin', content_type=auth_content)
        self.global_admin.permissions.add(permission)
        self.global_admin.user_set.add(self.user)
        self.organization = Organization.objects.create(name="haha")
        self.afro = Region.objects.create(name="Afro")
        self.uganda = Country.objects.create(name="Uganda")

        self.form_data = {
            'username': 'rajni',
            'password1': 'kant',
            'password2': 'kant',
            'email': 'raj@ni.kant',
            'groups': self.global_admin.id}

    def test_get_login(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('users/login.html', templates)

    def test_get_list_users(self):
        user2 = User.objects.create(username='user1', email='rajni@kant.com')

        response = self.client.get('/users/')
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('users/index.html', templates)
        self.assertIsInstance(response.context['filter_form'], UserFilterForm)
        self.assertIn(self.user, response.context['users'])
        self.assertIn(user2, response.context['users'])

    def test_get_new(self):
        response = self.client.get('/users/new/')
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('users/new.html', templates)
        self.assertIsInstance(response.context['form'], UserProfileForm)
        self.assertIn('CREATE', response.context['btn_label'])
        self.assertIn('Create new user', response.context['title'])
        self.assertIn(self.organization, response.context['organizations'])
        self.assertIn(self.afro, response.context['regions'])
        self.assertIn(self.uganda, response.context['countries'])

    def test_post_new_user(self):
        response = self.client.post('/users/new/', data=self.form_data)
        self.assertRedirects(response, expected_url='/users/')
        user = User.objects.filter(username=self.form_data['username'])
        self.failUnless(user)
        self.assertIn('%s created successfully.' % self.global_admin.name, response.cookies['messages'].value)

class FilterUsersViewTest(BaseTest):
    def setUp(self):
        self.organization = Organization.objects.create(name="UNICEF")
        self.region = Region.objects.create(name="Afro", organization=self.organization)
        self.paho = Region.objects.create(name="PAHO", organization=self.organization)
        self.uganda = Country.objects.create(name="uganda", code="UGX")
        self.rwanda = Country.objects.create(name="Rwanda", code="RWA")
        self.region.countries.add(self.uganda)
        self.peru = Country.objects.create(name="Peru", code="PRU")
        self.paho.countries.add(self.peru)
        self.jacinta = User.objects.create(username='Jacinta')
        self.tony = User.objects.create(username='Tony')
        UserProfile.objects.create(user=self.jacinta, country=self.uganda, region=self.region, organization=self.organization)
        UserProfile.objects.create(user=self.tony, country=self.rwanda, region=self.region, organization=self.organization)
        self.global_admin = Group.objects.create(name="GROUP")
        self.felix = User.objects.create(username='Felix')
        UserProfile.objects.create(user=self.felix, country=self.peru, region=self.paho, organization=self.organization)

    def test_post_filter_users_by_region(self):
        post_data = {'region': self.region.id, 'organization': '', 'role': ''}
        response = self.client.post('/users/', data=post_data)

        self.assertEqual(2, len(response.context['users']))
        self.assertIn(self.jacinta, response.context['users'])
        self.assertNotIn(self.felix, response.context['users'])

    def test_post_filter_users_by_organisation(self):
        organization = Organization.objects.create(name="WHO")
        who_region = Region.objects.create(name="AFR", organization=organization)
        sudan = Country.objects.create(name="Sudan", code="SDA")
        who_region.countries.add(sudan)
        fatima = User.objects.create(username='Fatima')
        UserProfile.objects.create(user=fatima, country=self.uganda, region=who_region, organization=self.organization)

        faritha = User.objects.create(username='Faritha')
        UserProfile.objects.create(user=faritha, country=sudan, region=who_region, organization=organization)

        post_data = {'organization': organization.id, 'region': '', 'role': ''}

        response = self.client.post('/users/', data=post_data)

        self.assertEqual(1, len(response.context['users']))
        self.assertIn(faritha, response.context['users'])
        self.assertNotIn(self.jacinta, response.context['users'])
        self.assertNotIn(self.felix, response.context['users'])

    def test_post_filter_users_by_role(self):
        self.global_admin.user_set.add(self.tony, self.felix)
        post_data = {'organization': '', 'region': '', 'role': self.global_admin.id}

        response = self.client.post('/users/', data=post_data)
        faritha = User.objects.create(username='Faritha')

        self.assertEqual(2, len(response.context['users']))
        self.assertNotIn(faritha, response.context['users'])
        self.assertIn(self.felix, response.context['users'])
        self.assertIn(self.tony, response.context['users'])

    def test_post_filter_users_by_all(self):
        organization = Organization.objects.create(name="WHO")
        who_region = Region.objects.create(name="AFR", organization=organization)
        sudan = Country.objects.create(name="Sudan", code="SDA")
        who_region.countries.add(sudan)
        fatima = User.objects.create(username='Fatima')
        UserProfile.objects.create(user=fatima, country=self.uganda, region=who_region, organization=self.organization)

        faritha = User.objects.create(username='Faritha')
        UserProfile.objects.create(user=faritha, country=sudan, region=who_region, organization=organization)

        self.global_admin.user_set.add(faritha, self.tony, self.felix)

        post_data = {'organization': self.organization.id, 'region': self.region.id, 'role': self.global_admin.id}

        response = self.client.post('/users/', data=post_data)

        self.assertEqual(1, len(response.context['users']))
        self.assertNotIn(faritha, response.context['users'])
        self.assertNotIn(fatima, response.context['users'])
        self.assertIn(self.tony, response.context['users'])
        self.assertNotIn(self.felix, response.context['users'])

    def test_post_filter_users_by_organisation_and_region(self):
        organization = Organization.objects.create(name="WHO")
        who_region = Region.objects.create(name="AFR", organization=organization)
        sudan = Country.objects.create(name="Sudan", code="SDA")
        who_region.countries.add(sudan)
        fatima = User.objects.create(username='Fatima')
        UserProfile.objects.create(user=fatima, country=self.uganda, region=who_region, organization=self.organization)

        faritha = User.objects.create(username='Faritha')
        UserProfile.objects.create(user=faritha, country=sudan, region=who_region, organization=organization)

        post_data = {'organization': organization.id, 'region': who_region.id, 'role': ''}

        response = self.client.post('/users/', data=post_data)

        self.assertEqual(1, len(response.context['users']))
        self.assertIn(faritha, response.context['users'])
        self.assertNotIn(fatima, response.context['users'])
        self.assertNotIn(self.felix, response.context['users'])

    def test_post_filter_users_by_organisation_and_role(self):
        organization = Organization.objects.create(name="WHO")
        who_region = Region.objects.create(name="AFR", organization=organization)
        sudan = Country.objects.create(name="Sudan", code="SDA")
        who_region.countries.add(sudan)
        fatima = User.objects.create(username='Fatima')
        UserProfile.objects.create(user=fatima, country=self.uganda, region=who_region, organization=self.organization)

        faritha = User.objects.create(username='Faritha')
        UserProfile.objects.create(user=faritha, country=sudan, region=who_region, organization=organization)

        self.global_admin.user_set.add(faritha, self.tony, self.felix)

        post_data = {'organization': self.organization.id, 'region': '', 'role': self.global_admin.id}

        response = self.client.post('/users/', data=post_data)

        self.assertEqual(2, len(response.context['users']))
        self.assertNotIn(faritha, response.context['users'])
        self.assertNotIn(fatima, response.context['users'])
        self.assertIn(self.tony, response.context['users'])
        self.assertIn(self.felix, response.context['users'])

    def test_post_filter_users_by_role_and_region(self):
        organization = Organization.objects.create(name="WHO")
        who_region = Region.objects.create(name="AFR", organization=organization)
        sudan = Country.objects.create(name="Sudan", code="SDA")
        who_region.countries.add(sudan)
        fatima = User.objects.create(username='Fatima')
        UserProfile.objects.create(user=fatima, country=self.uganda, region=who_region, organization=self.organization)

        faritha = User.objects.create(username='Faritha')
        UserProfile.objects.create(user=faritha, country=sudan, region=who_region, organization=organization)

        self.global_admin.user_set.add(faritha, self.tony, self.felix)

        post_data = {'organization': '', 'region': self.region.id, 'role': self.global_admin.id}

        response = self.client.post('/users/', data=post_data)

        self.assertEqual(1, len(response.context['users']))
        self.assertNotIn(faritha, response.context['users'])
        self.assertNotIn(fatima, response.context['users'])
        self.assertIn(self.tony, response.context['users'])
        self.assertNotIn(self.felix, response.context['users'])