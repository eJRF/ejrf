import factory

from questionnaire.models import Section
from questionnaire.tests.factories.questionnaire_factory import QuestionnaireFactory


class SectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Section

    name = "A nice name"
    title = "A title"
    order = 1
    description = "A description"
    questionnaire = factory.SubFactory(QuestionnaireFactory)