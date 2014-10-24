import json
from django.http import HttpResponse
from django.views.generic import View
from questionnaire.models import SubSection, Questionnaire, Question, QuestionGroup
from django.core import serializers

class SubsectionQuestions(View):
    def get(self, request, *args, **kwargs):
        subsection_id=kwargs['subsection_id']
        question_group = QuestionGroup.objects.select_related('question').get(subsection_id=subsection_id)
        questions = question_group.question.all()
        data = {}
        data['questions'] =  serializers.serialize("json", questions)
        return HttpResponse(json.dumps(data), content_type = "application/json")
