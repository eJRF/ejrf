import json

from django.http import HttpResponse
from django.views.generic import View
from braces.views import PermissionRequiredMixin

from questionnaire.forms.skip_rule_form import SkipRuleForm, SkipQuestionForm, SkipSubsectionForm
from questionnaire.models import SkipRule


class SkipRuleView(PermissionRequiredMixin, View):
    permission_required = 'auth.can_edit_questionnaire'

    def error_response(self, error_message):
        return HttpResponse(json.dumps({'result': error_message}), content_type="application/json", status=400)

    def post(self, request, *args, **kwargs):
        if 'skip_question' in request.POST.keys():
            skip_question_rule_form = SkipQuestionForm(request.POST)
        else:
            skip_question_rule_form = SkipSubsectionForm(request.POST)

        if skip_question_rule_form.is_valid():
            skip_question_rule_form.save()
            data = {'result': 'Skip rule created successfully'}
            return HttpResponse(json.dumps(data), content_type="application/json", status=201)
        else:
            errors_message = skip_question_rule_form.errors.values()
            error_msgs = [error for errors in errors_message for error in errors]
            return self.error_response(error_msgs)

    def get(self, request, subsection_id, *args, **kwargs):
        data = SkipRule.objects.filter(subsection_id=subsection_id).select_subclasses()
        responses = map(lambda q: q.to_dictionary(), data)
        return HttpResponse(json.dumps(responses), content_type="application/json", status=200)

    def delete(self, request, rule_id, *args, **kwargs):
        status = 204
        rules = SkipRule.objects.filter(id=rule_id)

        if rules:
            rules[0].delete()
            status = 200

        return HttpResponse(status=status)

