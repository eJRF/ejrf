import factory

from questionnaire.models.skip_rule import SkipQuestion, SkipSubsection
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.question_option_factory import QuestionOptionFactory
from questionnaire.tests.factories.region_factory import RegionFactory
from questionnaire.tests.factories.sub_section_factory import SubSectionFactory


class SkipQuestionRuleFactory(factory.DjangoModelFactory):
    class Meta:
        model = SkipQuestion

    root_question = factory.SubFactory(QuestionFactory)
    response = factory.SubFactory(QuestionOptionFactory)
    subsection = factory.SubFactory(SubSectionFactory)
    skip_question = factory.SubFactory(QuestionFactory)
    region = factory.SubFactory(RegionFactory)


class SkipSubsectionRuleFactory(factory.DjangoModelFactory):
    class Meta:
        model = SkipSubsection

    root_question = factory.SubFactory(QuestionFactory)
    response = factory.SubFactory(QuestionOptionFactory)
    subsection = factory.SubFactory(SubSectionFactory)
    skip_subsection = factory.SubFactory(SubSectionFactory)
    region = factory.SubFactory(RegionFactory)
