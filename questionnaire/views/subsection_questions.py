import json

from django.http import HttpResponse
from django.views.generic import View
from django.core import serializers
from braces.views import PermissionRequiredMixin

from questionnaire.models import QuestionGroup


class SubsectionQuestions(PermissionRequiredMixin, View):
    permission_required = 'auth.can_view_questionnaire'

    def get(self, request, *args, **kwargs):
        subsection_id = kwargs['subsection_id']
        question_group = QuestionGroup.objects.select_related('question').filter(subsection_id=subsection_id)
        not_in_grid_question_groups = filter(lambda qg: qg.is_in_hybrid_grid() or not qg.is_in_grid(), list(question_group))
        questions = []
        for qg in not_in_grid_question_groups:
            for q in qg.question.all():
                question_json = serializers.serialize("json", [q])
                options_json = serializers.serialize("json", q.options.all())
                question_dict = json.loads(question_json)[0]
                question_dict['options'] = json.loads(options_json)
                question_dict['parentQuestionGroup'] = qg.parent_group_id()
                questions.append(question_dict)

        data = {}
        data['questions'] = questions

        return HttpResponse(json.dumps(data), content_type="application/json")