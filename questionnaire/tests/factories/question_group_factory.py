from questionnaire.models import QuestionGroup
from questionnaire.tests.factories.sub_section_factory import SubSectionFactory
import factory


class QuestionGroupFactory(factory.DjangoModelFactory):
    class Meta:
        model = QuestionGroup

    subsection = factory.SubFactory(SubSectionFactory)
    name = factory.Sequence(lambda n: 'Question group {0}'.format(n))
    order = factory.Sequence(lambda n: '0{0}'.format(n))