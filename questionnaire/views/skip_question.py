import json
from django.http import HttpResponse
from django.views.generic import View

class SkipQuestion(View):
    def post(self, request, *args, **kwargs):
        data = {}
        data['result'] = 'success'
        return HttpResponse(json.dumps(data), content_type = "application/json", status=201)
