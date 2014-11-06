import factory

from questionnaire.models import SkipQuestion
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.question_option_factory import QuestionOptionFactory
from questionnaire.tests.factories.sub_section_factory import SubSectionFactory


class SkipQuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = SkipQuestion

    root_question = factory.SubFactory(QuestionFactory)
    response = factory.SubFactory(QuestionOptionFactory)
    skip_question = factory.SubFactory(QuestionFactory)
    subsection = factory.SubFactory(SubSectionFactory)
