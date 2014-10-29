import json
from django.http import HttpResponse
from django.views.generic import View
from questionnaire.models import SkipQuestion
import logging
from django.core.exceptions import ValidationError
from braces.views import PermissionRequiredMixin


class SkipQuestionView(PermissionRequiredMixin, View):
    permission_required = 'auth.can_edit_questionnaire'

    def error_response(self, error_message):
        return HttpResponse(json.dumps({'result': error_message}), content_type="application/json", status=400)

    def post(self, request, *args, **kwargs):
        try:
            root_question_id = request.POST['root-question']
            response_id = request.POST['responses']
            skip_question_id = request.POST['skip-question']
            subsection_id = request.POST['subsection-id']
        except Exception as e:
            return self.error_response("You must provide a root question, response, question to skip and subsection")

        try:
            SkipQuestion.create(root_question_id, response_id, skip_question_id, subsection_id)
        except ValidationError as e:
            msg = '; '.join(e.messages)
            logging.error(msg)
            return self.error_response(msg)

        except Exception as e2:
            logging.error(e2)
            return self.error_response('Unknown error occurred')

        data = {}
        data['result'] = 'Skip rule created successfully'
        return HttpResponse(json.dumps(data), content_type="application/json", status=201)
