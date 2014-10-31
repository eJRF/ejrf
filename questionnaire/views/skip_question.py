import json
from django.http import HttpResponse
from django.views.generic import View
from questionnaire.forms.skip_question_form import SkipQuestionRuleForm
from questionnaire.models import SkipQuestion
import logging
from django.core.exceptions import ValidationError
from braces.views import PermissionRequiredMixin
from django.core import serializers


class SkipQuestionView(PermissionRequiredMixin, View):
    permission_required = 'auth.can_edit_questionnaire'

    def error_response(self, error_message):
        return HttpResponse(json.dumps({'result': error_message}), content_type="application/json", status=400)

    def post(self, request, *args, **kwargs):
        skip_question_rule_form = SkipQuestionRuleForm(request.POST)
        if skip_question_rule_form.is_valid():
            skip_question_rule_form.save()
            data = {'result':  'Skip rule created successfully'}
            return HttpResponse(json.dumps(data), content_type="application/json", status=201)
        else:
            errors_message = skip_question_rule_form.errors.values()
            error_msgs = [error for errors in errors_message for error in errors]
            return self.error_response(error_msgs)


    def get(self, request, subsection_id, *args, **kwargs):

        data = SkipQuestion.objects.select_related('root_question', 'subsection', 'response', 'skip_question').filter(subsection_id=subsection_id)
        responses = map(lambda q: q.to_dictionary(), data)
        print responses
        return HttpResponse(json.dumps(responses), content_type="application/json", status=200)
