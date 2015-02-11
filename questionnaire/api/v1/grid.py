import json
from braces.views import PermissionRequiredMixin
from django.http import HttpResponse
from django.core import serializers
from django.views.generic import View
from questionnaire.forms.grid import GridForm, EditGridForm

from questionnaire.models import Theme, QuestionGroup


class GridAPIView(PermissionRequiredMixin, View):
    permission_required = 'auth.can_edit_questionnaire'
    template_name = 'questions/index.html'
    model = Theme

    def get(self, request, grid_id, *args, **kwargs):
        question_group = QuestionGroup.objects.get(id=grid_id)
        question_group_json = serializers.serialize("json", [question_group])
        children = serializers.serialize("json", question_group.sub_group.all())
        grid_response = json.loads(question_group_json)
        grid_response[0]['children'] = children
        return HttpResponse(json.dumps(grid_response), content_type="application/json")

    def post(self, request, grid_id, *args, **kwargs):
        grid = QuestionGroup.objects.get(id=grid_id)
        form = EditGridForm(data=request.POST, instance=grid)
        if form.is_valid():
            form.save()
            grid_response = [{'message': 'The grid was updated successfully.'}]
            return HttpResponse(json.dumps(grid_response), content_type="application/json")
        grid_response = [{'error': 'The grid could not be updated.', 'form_errors': form.errors}]
        return HttpResponse(json.dumps(grid_response), content_type="application/json", status=400)