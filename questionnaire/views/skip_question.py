import json
from django.http import HttpResponse
from django.views.generic import View
from questionnaire.models import SkipQuestion, Question, QuestionOption, SubSection
import logging
from django.core.exceptions import ValidationError

class SkipQuestionView(View):
	def error_response(self, error_message):
		return HttpResponse(json.dumps({'result': error_message}), content_type= "application/json", status=400)

	def post(self, request, *args, **kwargs):
		# print(request)

		root_question_id = 	request.POST['root-question']
		response_id = 	request.POST['responses']	
		skip_question_id = 	request.POST['skip-question']
		subsection_id = request.POST['subsection-id']

		try: 	
			
			SkipQuestion.create(root_question_id, response_id, skip_question_id, subsection_id)
			# else:
				# return self.error_response('Question is not part of subsection')
		except ValidationError as e:
			msg = '; '.join(e.messages)
			logging.error(msg)
			return self.error_response(msg)

		except Exception as e2:
			logging.error(e2)
			return self.error_response('Unknown error occured')

		data = {}
		data['result'] = 'success'
		return HttpResponse(json.dumps(data), content_type = "application/json", status=201)
