from questionnaire.models import QuestionOption
from questionnaire.tests.factories.question_factory import QuestionFactory
import factory


class QuestionOptionFactory(factory.DjangoModelFactory):
    class Meta:
        model = QuestionOption

    text = "Yes"
    question = factory.SubFactory(QuestionFactory)
    instructions = "An instruction"
    UID = factory.Sequence(lambda n: '0{0}'.format(n))