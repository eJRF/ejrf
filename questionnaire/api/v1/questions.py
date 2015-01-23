from django.http import HttpResponse
from django.core import serializers
from django.views.generic import View

from questionnaire.models import Question, Questionnaire


class QuestionAPIView(View):
    template_name = 'questions/index.html'
    model = Question

    def get(self, *args, **kwargs):
        data = self._query_data()
        serialized_data = serializers.serialize('json', data)
        return HttpResponse(serialized_data, content_type="application/json")

    def _query_data(self):
        excluded_params = self._excluded_params()
        QUESTION_FIELDS_MAPPING = {'answer_type': 'answer_type__iexact'}
        query_params = {value: self.request.GET.get(key) for key, value in QUESTION_FIELDS_MAPPING.items() if self.request.GET.get(key)}
        return Question.objects.filter(region=self.request.user.user_profile.region, **query_params).exclude(**excluded_params)

    def _excluded_params(self):
        questionnaire = Questionnaire.objects.filter(id=self.request.GET.get('questionnaire'))
        if questionnaire.exists() and self.request.GET.get('unused'):
            questionnaire = questionnaire[0]
            excluded_questions_ids = questionnaire.get_all_questions().values_list('id', flat=True)
            return {'id__in': excluded_questions_ids}
        return {}