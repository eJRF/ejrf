from questionnaire.models.base import BaseModel
from questionnaire.models import Question, QuestionOption, SubSection
from django.db import models
from django.core.exceptions import ValidationError


class SkipQuestion(BaseModel):
    root_question = models.ForeignKey(Question, blank=False, null=False, related_name="root_question")
    response = models.ForeignKey(QuestionOption, blank=False, null=False, related_name="response_option")
    skip_question = models.ForeignKey(Question, blank=False, null=False, related_name="skip_question")
    subsection = models.ForeignKey(SubSection, blank=False, null=False, related_name="subsection")

    @classmethod
    def create(cls, root_question_id, response_id, skip_question_id, subsection_id):
        if root_question_id == skip_question_id:
            raise ValidationError("root question cannot be the same as skip question")

        if not Question.objects.filter(pk=root_question_id).exists():
            raise ValidationError('root-question does not exist')
        root_question = Question.objects.get(pk=root_question_id)

        if not QuestionOption.objects.filter(pk=response_id).exists():
            raise ValidationError('response does not exist')
        response = QuestionOption.objects.get(pk=response_id)

        if not Question.objects.filter(pk=skip_question_id).exists():
            raise ValidationError('skip-question does not exist')

        subsection = SubSection.objects.get(pk=subsection_id)
        if root_question.question_group.filter(subsection=subsection).count() == 0:
            raise ValidationError('root-question is not part of subsection')

        skip_question = Question.objects.get(pk=skip_question_id)
        if skip_question.question_group.filter(subsection=subsection).count() == 0:
            raise ValidationError('skip-question is not part of subsection')

        if response.question != root_question:
            print response.question
            raise ValidationError('root question\'s options does not contain the provided response')

        SkipQuestion.objects.create(root_question=root_question,
                                    response=response,
                                    skip_question=skip_question,
                                    subsection=subsection)