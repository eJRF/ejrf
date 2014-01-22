from questionnaire.models.base import BaseModel
from django.db import models


class QuestionGroup(BaseModel):
    question = models.ManyToManyField("Question", blank=False, null=False)
    subsection = models.ForeignKey("SubSection", blank=False, null=False, related_name="question_group")
    name = models.CharField(max_length=200, blank=False, null=True)
    instructions = models.TextField(blank=False, null=True)
    parent = models.ForeignKey("QuestionGroup", null=True, related_name="sub_group")
    order = models.PositiveIntegerField(null=True, blank=False)

    def all_questions(self):
        return self.question.all()

    def sub_groups(self):
        return self.sub_group.all()

    def and_sub_group_questions(self):
        questions = list(self.all_questions())
        for sub_group in self.sub_groups():
            questions.extend(sub_group.all_questions())
        return questions


    class Meta:
        ordering = ('order',)
        app_label = 'questionnaire'