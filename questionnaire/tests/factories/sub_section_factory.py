from questionnaire.models import SubSection
from questionnaire.tests.factories.section_factory import SectionFactory
import factory


class SubSectionFactory(factory.DjangoModelFactory):
    class Meta:
        model = SubSection

    title = "A title"
    order = 1
    section = factory.SubFactory(SectionFactory)
    description = 'Description'