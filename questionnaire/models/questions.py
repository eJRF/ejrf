from questionnaire.models.base import BaseModel
from django.db import models


class Question(BaseModel):

    ANSWER_TYPES = (
        ("Date","Date"),
        ("MultiChoice","MultiChoice"),
        ("Number","Number"),
        ("Text","Text"),
    )

    text = models.TextField(blank=False, null=False)
    instructions = models.TextField(blank=False, null=True)
    UID = models.CharField(blank=False, null=False, max_length=6, unique=True)
    answer_type = models.CharField(blank=False, null=False, max_length=20, choices=ANSWER_TYPES)

class QuestionOption(BaseModel):
    text = models.CharField(max_length=100, blank=False, null=False)
    question = models.ForeignKey(Question)
