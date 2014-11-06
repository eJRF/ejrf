import factory

from questionnaire.models import Organization


class OrganizationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Organization

    name = 'WHO'