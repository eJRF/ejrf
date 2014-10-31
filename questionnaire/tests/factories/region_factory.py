from questionnaire.models import Region
from questionnaire.tests.factories.organization_factory import OrganizationFactory
import factory


class RegionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Region
    name = 'AFRO'
    organization = factory.SubFactory(OrganizationFactory)