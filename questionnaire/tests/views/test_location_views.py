import json

from django.test import Client

from questionnaire.models import Region, Country
from questionnaire.tests.base_test import BaseTest


class RegionViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.assign('can_edit_questionnaire', self.user)
        self.login_user()

    def test_get_region_list(self):
        region1 = Region.objects.create(name="AFRO")
        region2 = Region.objects.create(name="SEAR")
        response = self.client.get('/locations/region/')
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('locations/region/index.html', templates)
        self.assertEqual(2, len(response.context['region_list']))
        self.assertIn(region1, response.context['region_list'])
        self.assertIn(region2, response.context['region_list'])

    def test_login_required(self):
        self.assert_login_required('/locations/region/')

    def test_perms_required(self):
        self.assert_permission_required('/locations/region/')


class CountryViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.assign('can_edit_questionnaire', self.user)
        self.login_user()

    def test_get_region_list(self):
        region = Region.objects.create(name="AFRO")
        paho = Region.objects.create(name="PAHO")
        uganda = Country.objects.create(name="Uganda")
        uganda.regions.add(region)
        brasil = Country.objects.create(name="Brasil")
        brasil.regions.add(paho)
        response = self.client.get('/locations/region/%d/country/' % region.id)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('locations/country/index.html', templates)
        self.assertEqual(1, len(response.context['country_list']))
        self.assertIn(uganda, response.context['country_list'])
        self.assertNotIn(brasil, response.context['country_list'])

    def test_login_required(self):
        region = Region.objects.create(name="AFRO")
        self.assert_login_required('/locations/region/%d/country/' % region.id)

    def test_get_json_countries_for_regions(self):
        region = Region.objects.create(name="AFRO")
        paho = Region.objects.create(name="PAHO")
        uganda = Country.objects.create(name="Uganda")
        congo = Country.objects.create(name="Congo")
        uganda.regions.add(region)
        brasil = Country.objects.create(name="Brasil")
        brasil.regions.add(paho)
        response = self.client.get('/locations/countries/?regions=%s&regions=%s' % (paho.id, region.id))
        self.assertEqual(200, response.status_code)
        countries = json.loads(response.content)
        self.assertIn(dict(id=uganda.id, name=uganda.name), countries)
        self.assertIn(dict(id=brasil.id, name=brasil.name), countries)
        self.assertNotIn(dict(id=congo.id, name=congo.name), countries)