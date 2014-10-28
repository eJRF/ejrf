import json
from django.http import HttpResponse
from django.views.generic import View
from questionnaire.models import SkipQuestion

class SkipQuestionView(View):
    def post(self, request, *args, **kwargs):
        data = {}
        data['result'] = 'success'
        SkipQuestion.objects.create()
        return HttpResponse(json.dumps(data), content_type = "application/json", status=201)
