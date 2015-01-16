import json

from django.http import HttpResponse
from django.views.generic import View

from questionnaire.models import Questionnaire


class ValidateQuestionnaireFields(View):
    def get(self, *args, **kwargs):
        year = self.request.GET.get('year')
        questionnaire_in_year = Questionnaire.objects.filter(year=year)

        published_questionnaires = questionnaire_in_year.filter(status=Questionnaire.PUBLISHED,
                                                                children__answers__isnull=False)

        if published_questionnaires.exists():
            response = {'status': 'alert-danger', 'message': 'Questionnaire has responses.'}
            return HttpResponse(json.dumps(response), content_type="application/json")

        if questionnaire_in_year.exists():
            response = {'status': 'alert-warning',
                        'message': 'A Revision of the year %s already exists. '
                                   'If you go ahead, that revision will be archived.' % year}
            return HttpResponse(json.dumps(response), content_type="application/json")

        response = {'status': '', 'message': ''}
        return HttpResponse(json.dumps(response), content_type="application/json")