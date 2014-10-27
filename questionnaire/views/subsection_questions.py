import json
from django.http import HttpResponse
from django.views.generic import View
from questionnaire.models import SubSection, Questionnaire, Question, QuestionGroup
from django.core import serializers
import logging

class SubsectionQuestions(View):
    def get(self, request, *args, **kwargs):
        subsection_id=kwargs['subsection_id']
        question_group = QuestionGroup.objects.select_related('question').filter(subsection_id=subsection_id)
        question_group_list = map(lambda qg: list(qg.question.all()), list(question_group))
        questions = []
        for qg in question_group_list:
            questions.extend(qg)
        logging.warning(questions)
        data = {}
        data['questions'] =  serializers.serialize("json", questions)
        return HttpResponse(json.dumps(data), content_type = "application/json")
