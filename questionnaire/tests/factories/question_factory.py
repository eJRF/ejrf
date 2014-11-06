import factory

from questionnaire.models import Question
from questionnaire.utils.answer_type import AnswerTypes


class QuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Question

    text = "A nice question"
    export_label = "A nice question"
    instructions = 'some instructions'
    UID = factory.Sequence(lambda n: '0{0}'.format(n))
    answer_type = AnswerTypes.MULTI_CHOICE
    is_primary = False
    is_required = False