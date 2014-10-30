from questionnaire.models import Section
from questionnaire.tests.factory.questionnaire_factory import QuestionnaireFactory
import factory


class SectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Section

    name = "A nice name"
    title = "A title"
    order = 1
    description = "A description"
    questionnaire = factory.SubFactory(QuestionnaireFactory)