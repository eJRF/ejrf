from django.db import models

from questionnaire.models.base import BaseModel
from questionnaire.models import Question, QuestionOption, SubSection


class SkipRule(BaseModel):
    class Meta:
        unique_together = ("root_question", "response", "skip_question", "skip_subsection", "subsection")
        app_label = 'questionnaire'

    root_question = models.ForeignKey(Question, blank=False, null=False, related_name="root_skip_rules")
    response = models.ForeignKey(QuestionOption, blank=False, null=False, related_name="skip_rules")
    skip_question = models.ForeignKey(Question, blank=True, null=True, related_name="skip_rules")
    skip_subsection = models.ForeignKey(SubSection, blank=True, null=True)
    subsection = models.ForeignKey(SubSection, blank=False, null=False, related_name="skip_rules")

    def to_dictionary(self):
        return {'id': self.id, 'skip_question': self.skip_question.text,
                'root_question': self.root_question.text,
                'response': self.response.text}
