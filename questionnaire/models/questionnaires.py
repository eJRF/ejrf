from questionnaire.models.base import BaseModel
from django.db import models


class Questionnaire(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):
        return '%s' % self.name

    def sub_sections(self):
        sections = self.sections.all()
        from questionnaire.models import SubSection
        return SubSection.objects.filter(section__in=sections)

    def get_all_questions(self):
        all_questions = []
        for subsection in self.sub_sections():
            all_questions.extend(subsection.all_questions())
        return all_questions

    def all_groups(self):
        all_groups = []
        for subsection in self.sub_sections():
            all_groups.extend(subsection.question_group.all())
        return all_groups