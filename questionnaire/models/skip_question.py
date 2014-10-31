from questionnaire.models.base import BaseModel
from questionnaire.models import Question, QuestionOption, SubSection
from django.db import models


class SkipQuestion(BaseModel):
    root_question = models.ForeignKey(Question, blank=False, null=False, related_name="root_question")
    response = models.ForeignKey(QuestionOption, blank=False, null=False, related_name="response_option")
    skip_question = models.ForeignKey(Question, blank=False, null=False, related_name="skip_question")
    subsection = models.ForeignKey(SubSection, blank=False, null=False, related_name="subsection")