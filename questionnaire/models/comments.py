from django.contrib.auth.models import User
from django.db import models

from questionnaire.models.base import BaseModel


class Comment(BaseModel):
    text = models.CharField(max_length=100, blank=False, null=False)
    answer_group = models.ManyToManyField("AnswerGroup", blank=False, null=False, related_name="comments")
    user = models.ForeignKey(User, blank=False, null=False)