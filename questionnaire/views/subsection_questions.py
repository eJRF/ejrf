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
        question_group = QuestionGroup.objects.select_related('question').filter(subsection_id=subsection_id,
                                                                                 grid=False)
        question_group_list = map(lambda qg: list(qg.question.all()), list(question_group))
        questions = []
        for qg in question_group_list:
            for q in qg:
                question_json = serializers.serialize("json", [q])
                options_json = serializers.serialize("json", q.options.all())
                question_dict = json.loads(question_json)[0]
                question_dict['options'] = json.loads(options_json)
                questions.append(question_dict)

        data = {}
        data['questions'] = questions

        return HttpResponse(json.dumps(data), content_type="application/json")
