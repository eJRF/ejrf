from questionnaire.models import SkipQuestion
import factory
from questionnaire.tests.factory.question_factory import QuestionFactory
from questionnaire.tests.factory.question_option_factory import QuestionOptionFactory
from questionnaire.tests.factory.sub_section_factory import SubSectionFactory


class SkipQuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = SkipQuestion

    root_question = factory.SubFactory(QuestionFactory)
    response = factory.SubFactory(QuestionOptionFactory)
    skip_question = factory.SubFactory(QuestionFactory)
    subsection = factory.SubFactory(SubSectionFactory)