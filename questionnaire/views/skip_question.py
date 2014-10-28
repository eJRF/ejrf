import json
from django.http import HttpResponse
from django.views.generic import View
from questionnaire.models import SkipQuestion, Question, QuestionOption

class SkipQuestionView(View):
    def post(self, request, *args, **kwargs):
    	print(request)
    	root_question_id = 	request.POST['root-question']
    	response_id = 	request.POST['responses']	
    	skip_question_id = 	request.POST['skip-question']

        data = {}
        data['result'] = 'success'
        SkipQuestion.objects.create(root_question=Question.objects.get(pk=root_question_id), response=QuestionOption.objects.get(pk=response_id), skip_question=Question.objects.get(pk=skip_question_id))
        return HttpResponse(json.dumps(data), content_type = "application/json", status=201)
