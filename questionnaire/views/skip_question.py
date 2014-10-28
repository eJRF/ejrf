import json
from django.http import HttpResponse
from django.views.generic import View
from questionnaire.models import SkipQuestion, Question, QuestionOption, SubSection
import logging

class SkipQuestionView(View):
	def error_response(self, error_message):
		return HttpResponse(json.dumps({'result': error_message}), content_type= "application/json", status=400)

	def post(self, request, *args, **kwargs):
		# print(request)

		root_question_id = 	request.POST['root-question']
		response_id = 	request.POST['responses']	
		skip_question_id = 	request.POST['skip-question']

		try:
			root_question = Question.objects.get(pk=root_question_id)
			subsection = SubSection.objects.get(pk=kwargs['subsection_id'])   	
			if root_question.question_group.filter(subsection = subsection).count() == 1:
				SkipQuestion.objects.create(root_question=root_question, response=QuestionOption.objects.get(pk=response_id), skip_question=Question.objects.get(pk=skip_question_id))
			else:
				return self.error_response('Question is not part of subsection')
		except Exception as e:
			logging.error(e)
			return self.error_response('Question or response do not exist')

		data = {}
		data['result'] = 'success'
		return HttpResponse(json.dumps(data), content_type = "application/json", status=201)
