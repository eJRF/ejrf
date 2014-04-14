import csv
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.http.request import QueryDict
from django.test import TestCase
from urllib import quote
from questionnaire.models import Country, UserProfile, Region, Organization


class BaseTest(TestCase):

    DATA_SUBMITTER = 'DATA_SUBMITTER'
    REGIONAL_ADMIN = 'REGIONAL_ADMIN'
    GLOBAL_ADMIN = 'GLOBAL_ADMIN'

    ROLE_BASED_ATTRIBUTES = {GLOBAL_ADMIN: '_global_admin_attributes',
                             REGIONAL_ADMIN: '_regional_admin_attributes',
                             DATA_SUBMITTER: '_data_submitter_attributes'}

    def write_to_csv(self, mode, data, csvfilename='test.csv'):
        with open(csvfilename, mode) as fp:
            _file = csv.writer(fp, delimiter=',')
            _file.writerows(data)
            fp.close()

    def create_user(self, username=None, group=GLOBAL_ADMIN, **kwargs):
        username = username if username else "user"
        user = User.objects.create(username=username, email="user@mail.com")
        attributes_creator_method = getattr(self, self.ROLE_BASED_ATTRIBUTES[group])
        UserProfile.objects.create(user=user, **attributes_creator_method(**kwargs))
        user.set_password("pass")
        user.save()
        return user

    def _data_submitter_attributes(self, country, region):
        region = Region.objects.create(name=region)
        country = Country.objects.create(name=country)
        region.countries.add(country)
        return {'country': country}

    def _global_admin_attributes(self, org):
        organization = Organization.objects.create(name=org)
        return {'organization': organization}

    def _regional_admin_attributes(self, region, org):
        organization = Organization.objects.create(name=org)
        region = Region.objects.create(name=region)
        return {'organization': organization, 'region': region}

    def login_user(self):
        self.client.login(username='user', password='pass')

    def assert_login_required(self, url):
        self.client.logout()
        response = self.client.get(url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(url),
                             status_code=302, target_status_code=200, msg_prefix='')

    def assign(self, permissions, user):
        auth_content = ContentType.objects.get_for_model(Permission)
        group = Group.objects.get_or_create(name="Group with %s permissions" % permissions)[0]
        permission, out = Permission.objects.get_or_create(codename=permissions, content_type=auth_content)
        group.permissions.add(permission)
        group.user_set.add(user)
        return user

    def assert_permission_required(self, url):
        self.client.logout()
        self.client.login(username='user_with_no_perms', password='pass')
        response = self.client.get(url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(url),
                             status_code=302, target_status_code=200, msg_prefix='')

    def cast_to_queryDict(self, original_dict):
        data_query_dict = QueryDict('', mutable=True)
        for key, val in original_dict.items():
            data_query_dict.setlist(key, val)
        return data_query_dict