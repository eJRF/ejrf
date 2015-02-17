import json
from django.core import serializers
from django.http import HttpResponse
from django.views.generic import View
from questionnaire.forms.questions import QuestionOptionForm
from questionnaire.models import QuestionOption, Question


class QuestionOptionAPIView(View):
    template_name = 'questions/index.html'
    model = QuestionOption

    def get(self, request, question_id, *args, **kwargs):
        data = QuestionOption.objects.filter(question__id=question_id)
        serialized_data = serializers.serialize('json', data)
        return HttpResponse(serialized_data, content_type="application/json")

    def post(self, *args, **kwargs):
        question = Question.objects.get(id=kwargs['question_id'])
        form = QuestionOptionForm(self.request.POST, question=question)
        if form.is_valid():
            form.save()
            message_response = {'message': 'The question options were reordered successfully.'}
            return HttpResponse(json.dumps(message_response), content_type="application/json")

        message = {'message': 'The question options could not be reordered successfully.'}
        return HttpResponse(json.dumps(message), content_type="application/json", status=400)