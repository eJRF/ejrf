from model_utils.managers import InheritanceManager
from django.db import models
from django.db.models import Q

from questionnaire.models.questions import Question, QuestionOption
from questionnaire.models.base import BaseModel
from questionnaire.utils.answer_type import AnswerTypes
from questionnaire.utils.model_utils import number_from


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
        response_query = cls._response_query(response)
        return answers.filter(response_query).distinct()

    @classmethod
    def _response_query(cls, response):
        if isinstance(response, QuestionOption):
            return Q(multichoiceanswer__response=response) | Q(multipleresponseanswer__response=response)
        return Q(dateanswer__response=response) | Q(textanswer__response=response) | Q(numericalanswer__response=response)

    def can_be_deleted(self, group, country):
        return group.grid and self.country == country


class NumericalAnswer(Answer):

    response = models.CharField(max_length=20, null=True)

    def __unicode__(self):
        return '%s' % self.format_response()

    def format_response(self):
        if AnswerTypes.is_integer(self.question.answer_sub_type) and number_from(self.response):
            return int(number_from(self.response))
        return ('%s' % self.response).strip()

    def _answer_sub_type_is_integer(self):
        return self.response and self.question.answer_sub_type and self.question.answer_sub_type.lower() == AnswerTypes.INTEGER.lower()


class TextAnswer(Answer):
    response = models.TextField(null=True)

    def __unicode__(self):
        return '%s' % self.format_response()

    def format_response(self):
        return self.response


class DateAnswer(Answer):
    response = models.CharField(null=True, max_length=10)

    def __unicode__(self):
        return '%s' % self.format_response()

    def format_response(self):
        return self.response


class MultiChoiceAnswer(Answer):
    response = models.ForeignKey(QuestionOption, null=True, related_name="answer")

    def __unicode__(self):
        return '%s' % self.format_response()

    def format_response(self):
        return self.response


class MultipleResponseAnswer(Answer):
    response = models.ManyToManyField(QuestionOption, null=True, related_name="answers")

    def __unicode__(self):
        return ', '.join(self.format_response().values_list('text', flat=True))

    def format_response(self):
        return self.response.all()


class AnswerStatus(object):
    options = {
        Answer.SUBMITTED_STATUS: Answer.SUBMITTED_STATUS,
        Answer.DRAFT_STATUS: 'In Progress',
        None: 'Not Started'
    }