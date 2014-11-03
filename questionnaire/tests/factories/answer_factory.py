import factory
from questionnaire.models import NumericalAnswer
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.questionnaire_factory import QuestionnaireFactory
from questionnaire.tests.factories.region_factory import CountryFactory


class NumericalAnswerFactory(factory.DjangoModelFactory):
    class Meta:
        model = NumericalAnswer

    question = factory.SubFactory(QuestionFactory)
    country = factory.SubFactory(CountryFactory)
    questionnaire = factory.SubFactory(QuestionnaireFactory)

