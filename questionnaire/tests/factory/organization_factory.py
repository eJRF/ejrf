from questionnaire.models import Organization
import factory

class OrganizationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Organization

    name = 'WHO'