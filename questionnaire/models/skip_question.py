from questionnaire.models.base import BaseModel
from questionnaire.models import Question
from django.db import models

class SkipQuestion(BaseModel):
	root_question = models.ForeignKey(Question, blank=False, null=False, related_name="root_question")