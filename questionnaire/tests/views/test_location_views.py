from django.test import Client
from questionnaire.models import Region, Country
from questionnaire.tests.base_test import BaseTest


class RegionViewTest(BaseTest):

    def setUp(self):
        self.client = Client()

    def test_get_region_list(self):
        region = Region.objects.create(name="AFRO")
        response = self.client.get('/locations/region/')
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('locations/region/index.html', templates)
        self.assertEqual(1, len(response.context['region_list']))
        self.assertIn(region, response.context['region_list'])


class CountryViewTest(BaseTest):

    def setUp(self):
        self.client = Client()

    def test_get_region_list(self):
        region = Region.objects.create(name="AFRO")
        paho = Region.objects.create(name="PAHO")
        uganda = Country.objects.create(name="Uganda", region=region)
        brasil = Country.objects.create(name="Brasil", region=paho)
        response = self.client.get('/locations/region/%d/country/' % region.id)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('locations/country/index.html', templates)
        self.assertEqual(1, len(response.context['country_list']))
        self.assertIn(uganda, response.context['country_list'])
        self.assertNotIn(brasil, response.context['country_list'])
