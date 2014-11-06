import factory

from questionnaire.models import Questionnaire
from questionnaire.tests.factories.region_factory import RegionFactory


class QuestionnaireFactory(factory.DjangoModelFactory):
    class Meta:
        model = Questionnaire

    name = 'New questionnaire 2013'
    description = 'description'
    year = 2014
    status = Questionnaire.DRAFT
    region = factory.SubFactory(RegionFactory)