from model_utils.managers import InheritanceManager
from django.db import models
from questionnaire.models.questions import Question, QuestionOption
from questionnaire.models.base import BaseModel


class Answer(BaseModel):
    objects = InheritanceManager()
    DRAFT_STATUS = "Draft"
    SUBMITTED_STATUS = 'Submitted'
    STATUS_CHOICES = {
        ("DRAFT", DRAFT_STATUS),
        ("SUBMITTED", SUBMITTED_STATUS),
    }

    question = models.ForeignKey(Question, null=True, related_name="answers")
    country = models.ForeignKey("Country", null=True)
    status = models.CharField(max_length=15, blank=False, null=False, choices=STATUS_CHOICES, default=DRAFT_STATUS)
    version = models.IntegerField(blank=False, null=True, default=1)
    code = models.CharField(blank=False, max_length=20, null=True)
    questionnaire = models.ForeignKey("Questionnaire", blank=False, null=True, related_name="answers")

    def is_draft(self):
        return self.status == self.DRAFT_STATUS

    @classmethod
    def from_response(cls, response, **kwargs):
        answers = cls.objects.filter(**kwargs).select_subclasses()
        answer = filter(lambda ans: ans.response == response or str(ans.response) == response, answers)
        answer_ids = map(lambda ans: ans.id, answer)
        return answers.filter(id__in=answer_ids).distinct()

    def can_be_deleted(self, group, country):
        return group.grid and self.country == country


class NumericalAnswer(Answer):
    response = models.DecimalField(max_digits=9, decimal_places=2, null=True)

    def format_response(self):
        if self.response and float(self.response).is_integer():
            return int(self.response)
        return self.response


class TextAnswer(Answer):
    response = models.CharField(max_length=100, null=True)

    def format_response(self):
        return self.response


class DateAnswer(Answer):
    response = models.CharField(null=True, max_length=10)

    def format_response(self):
        return self.response


class MultiChoiceAnswer(Answer):
    response = models.ForeignKey(QuestionOption, null=True, related_name="answer")

    def format_response(self):
        return self.response


class AnswerStatus(object):
    options = {
        Answer.SUBMITTED_STATUS: Answer.SUBMITTED_STATUS,
        Answer.DRAFT_STATUS: 'In Progress',
        None: 'Not Started'
    }