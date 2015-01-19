from django.http import HttpResponse
from django.core import serializers
from django.views.generic import View

from questionnaire.models import Question


class QuestionAPIView(View):
    template_name = 'questions/index.html'
    model = Question

    def get(self, *args, **kwargs):
        data = Question.objects.all()
        serialized_data = serializers.serialize('json', data)
        return HttpResponse(serialized_data, content_type="application/json")