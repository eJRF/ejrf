from django.core import serializers
from django.http import HttpResponse
from django.views.generic import View
from questionnaire.models import QuestionOption


class QuestionOptionAPIView(View):
    template_name = 'questions/index.html'
    model = QuestionOption

    def get(self, request, question_id, *args, **kwargs):
        data = QuestionOption.objects.filter(question__id=question_id)
        serialized_data = serializers.serialize('json', data)
        return HttpResponse(serialized_data, content_type="application/json")