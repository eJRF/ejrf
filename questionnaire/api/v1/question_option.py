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
            grid_response = {'message': 'The grid was updated successfully.'}
            return HttpResponse(json.dumps(grid_response), content_type="application/json")

        grid_response = {'error': 'The grid could not be updated.', 'form_errors': form.errors}
        return HttpResponse(json.dumps(grid_response), content_type="application/json", status=400)