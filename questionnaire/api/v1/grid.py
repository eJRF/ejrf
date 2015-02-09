import json
from braces.views import PermissionRequiredMixin
from django.http import HttpResponse
from django.core import serializers
from django.views.generic import View

from questionnaire.models import Theme, QuestionGroup


class GridAPIView(PermissionRequiredMixin, View):
    permission_required = 'auth.can_edit_questionnaire'
    template_name = 'questions/index.html'
    model = Theme

    def get(self, request, subsection_id, grid_id, *args, **kwargs):
        question_group = QuestionGroup.objects.get(id=grid_id)
        question_group_json = serializers.serialize("json", [question_group])
        children = serializers.serialize("json", question_group.sub_group.all())
        grid_response = json.loads(question_group_json)
        grid_response[0]['children'] = children
        return HttpResponse(json.dumps(grid_response), content_type="application/json")