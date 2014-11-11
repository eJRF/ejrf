import factory

from questionnaire.models import NumericalAnswer, TextAnswer, DateAnswer, MultiChoiceAnswer, MultipleResponseAnswer
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.questionnaire_factory import QuestionnaireFactory
from questionnaire.tests.factories.region_factory import CountryFactory


class NumericalAnswerFactory(factory.DjangoModelFactory):
    class Meta:
        model = NumericalAnswer

    question = factory.SubFactory(QuestionFactory)
    country = factory.SubFactory(CountryFactory)
    questionnaire = factory.SubFactory(QuestionnaireFactory)


class TextAnswerFactory(factory.DjangoModelFactory):
    class Meta:
        model = TextAnswer

    question = factory.SubFactory(QuestionFactory)
    country = factory.SubFactory(CountryFactory)
    questionnaire = factory.SubFactory(QuestionnaireFactory)


class DateAnswerFactory(factory.DjangoModelFactory):
    class Meta:
        model = DateAnswer

    question = factory.SubFactory(QuestionFactory)
    country = factory.SubFactory(CountryFactory)
    questionnaire = factory.SubFactory(QuestionnaireFactory)


class MultiChoiceAnswerFactory(factory.DjangoModelFactory):
    class Meta:
        model = MultiChoiceAnswer

    question = factory.SubFactory(QuestionFactory)
    country = factory.SubFactory(CountryFactory)
    questionnaire = factory.SubFactory(QuestionnaireFactory)


class MultipleResponseAnswerFactory(factory.DjangoModelFactory):
    class Meta:
        model = MultipleResponseAnswer

    question = factory.SubFactory(QuestionFactory)
    country = factory.SubFactory(CountryFactory)
    questionnaire = factory.SubFactory(QuestionnaireFactory)
