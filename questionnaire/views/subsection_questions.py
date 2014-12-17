import json

from django.http import HttpResponse
from django.views.generic import View
from django.core import serializers
from django.utils.cache import add_never_cache_headers
from braces.views import PermissionRequiredMixin

from questionnaire.models import QuestionGroup


class SubsectionQuestions(PermissionRequiredMixin, View):
    permission_required = 'auth.can_view_questionnaire'

    def get(self, request, *args, **kwargs):
        subsection_id = kwargs['subsection_id']
        question_group = QuestionGroup.objects.select_related('question').filter(subsection_id=subsection_id)
        questions = []
        user_profile = request.user.user_profile
        for qg in question_group:
            for q in qg.question.all():
                question_json = serializers.serialize("json", [q])
                options_json = serializers.serialize("json", q.options.all())
                question_dict = json.loads(question_json)[0]
                question_dict['options'] = json.loads(options_json)
                question_dict['parentQuestionGroup'] = qg.parent_group_id()
                question_dict['canSkip'] = (user_profile.is_global_admin or user_profile.region == q.region)
                question_dict['inHybrid'] = qg.is_in_hybrid_grid()
                question_dict['inGrid'] = qg.is_in_grid()
                questions.append(question_dict)
        data = {'questions': questions}
        response = HttpResponse(json.dumps(data), content_type="application/json")
        add_never_cache_headers(response)
        return response