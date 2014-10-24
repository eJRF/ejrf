import json
from django.http import HttpResponse
from django.views.generic import View

class SubsectionQuestions(View):
    def get(self, request, *args, **kwargs):
        data = {}
        data['something'] = 'useful'
        return HttpResponse(json.dumps(data), content_type = "application/json")
