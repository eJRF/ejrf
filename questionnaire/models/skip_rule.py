from django.db import models

from questionnaire.models.base import BaseModel
from questionnaire.models import Question, QuestionOption, SubSection


class SkipRule(BaseModel):
    root_question = models.ForeignKey(Question, blank=False, null=False, related_name="root_skip_rules")
    response = models.ForeignKey(QuestionOption, blank=False, null=False, related_name="skip_rules")
    skip_question = models.ForeignKey(Question, blank=True, null=True, related_name="skip_rules")
    skip_subsection = models.ForeignKey(SubSection, blank=True, null=True)
    subsection = models.ForeignKey(SubSection, blank=False, null=False, related_name="skip_rules")

    def to_dictionary(self):
        if self.skip_question is not None:
            return {'id': self.id,
                    'skip_question': self.skip_question.text,
                    'root_question': self.root_question.text,
                    'response': self.response.text}
        else:
            return {'id': self.id,
                    'skip_subsection': (" %s. %s" % (self.skip_subsection.order, self.skip_subsection.title)),
                    'root_question': self.root_question.text,
                    'response': self.response.text}
