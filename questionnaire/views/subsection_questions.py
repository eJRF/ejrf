import json
from django.http import HttpResponse
from django.views.generic import View
from questionnaire.models import SubSection, Questionnaire, Question, QuestionGroup, QuestionOption
from django.core import serializers
import logging

class SubsectionQuestions(View):
    def get(self, request, *args, **kwargs):
        subsection_id=kwargs['subsection_id']
        question_group = QuestionGroup.objects.select_related('question').filter(subsection_id=subsection_id)
        question_group_list = map(lambda qg: list(qg.question.all()), list(question_group))
        questions = []
        for qg in question_group_list:
            #questions.extend(qg)
            for q in qg:
                question_json = serializers.serialize("json", [q])
                options_json = serializers.serialize("json", q.options.all())
                question_dict = json.loads(question_json)[0]
                question_dict['options'] = json.loads(options_json)
                questions.append(question_dict)
            #     quest = q.__dict__
            #     quest['options'] = q.options.all()
            #     # quest['created'] = None
            #     # quest['m'] = None
            #     questions.append(q)
                logging.warning(q.options.all())

        data = {}
        data['questions'] = questions
        
        return HttpResponse(json.dumps(data), content_type = "application/json")
