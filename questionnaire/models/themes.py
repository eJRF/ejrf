from django.db import models

from questionnaire.models.base import BaseModel


class Theme(BaseModel):
    name = models.CharField("Name", max_length=100, blank=False, null=False)
    description = models.TextField("Description", max_length=500, blank=True, null=True)
    region = models.ForeignKey("Region", blank=True, null=True, related_name="themes")

    def __unicode__(self):
        return "%s" % self.name

    def de_associate_questions(self):
        self.questions.clear()