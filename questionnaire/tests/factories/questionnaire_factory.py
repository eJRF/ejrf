import factory

from questionnaire.models import Questionnaire


class QuestionnaireFactory(factory.DjangoModelFactory):
    class Meta:
        model = Questionnaire

    name = 'New questionnaire 2013'
    description = 'description'
    year = 2014
    status = Questionnaire.DRAFT