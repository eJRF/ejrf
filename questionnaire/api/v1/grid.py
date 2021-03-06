import json
from braces.views import PermissionRequiredMixin
from django.http import HttpResponse
from django.core import serializers
from django.views.generic import View
from questionnaire.forms.grid import GridForm, EditGridForm

from questionnaire.models import Theme, QuestionGroup, QuestionGroupOrder


class GridAPIView(PermissionRequiredMixin, View):
    permission_required = 'auth.can_edit_questionnaire'
    template_name = 'questions/index.html'
    model = QuestionGroup

    def get(self, request, grid_id, *args, **kwargs):
        question_group = QuestionGroup.objects.get(id=grid_id)
        question_group_json = serializers.serialize("json", [question_group])
        children = serializers.serialize("json", question_group.sub_group.all())

        grid_response = json.loads(question_group_json)[0]
        grid_response['children'] = json.loads(children)
        return HttpResponse(json.dumps(grid_response), content_type="application/json")

    def post(self, request, grid_id, *args, **kwargs):
        grid = QuestionGroup.objects.get(id=grid_id)
        form = EditGridForm(data=request.POST, instance=grid, subsection=grid.subsection)
        if form.is_valid():
            form.save()
            grid_response = {'message': 'The grid was updated successfully.'}
            return HttpResponse(json.dumps(grid_response), content_type="application/json")
        grid_response = {'error': 'The grid could not be updated.', 'form_errors': form.errors}
        return HttpResponse(json.dumps(grid_response), content_type="application/json", status=400)


class GridQuestionOrdersAPIView(PermissionRequiredMixin, View):
    permission_required = 'auth.can_edit_questionnaire'
    template_name = 'questions/index.html'
    model = QuestionGroupOrder

    def get(self, *args, **kwargs):
        question_group = QuestionGroup.objects.get(id=kwargs['grid_id'])
        orders = serializers.serialize("json", question_group.orders.all())
        return HttpResponse(orders, content_type="application/json")