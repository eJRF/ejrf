import factory

from questionnaire.models import Region, Country
from questionnaire.tests.factories.organization_factory import OrganizationFactory


class RegionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Region

    name = 'AFRO'
    organization = factory.SubFactory(OrganizationFactory)


class CountryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Country

    name = 'Uganda'
    regions = factory.RelatedFactory(RegionFactory)
    code = 'UGX'