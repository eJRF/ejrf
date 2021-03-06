from model_utils import Choices
from model_utils.fields import StatusField
from django.db import models
from django.core.urlresolvers import reverse

from questionnaire.models.base import BaseModel
from questionnaire.models import Region, Country, QuestionGroup, Answer
from questionnaire.models.questions import Question


class Questionnaire(BaseModel):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    FINALIZED = 'finalized'
    ARCHIVED = 'archived'

    PERMS_STATUS_MAP = {
        'auth.can_edit_questionnaire': [PUBLISHED, DRAFT, FINALIZED, ARCHIVED],
        'auth.can_view_users': [PUBLISHED, DRAFT, FINALIZED, ARCHIVED],
        'auth.can_submit_responses': [PUBLISHED]
    }

    STATUS = Choices(FINALIZED, PUBLISHED, DRAFT, ARCHIVED)
    name = models.CharField(max_length=256, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    status = StatusField(choices_name="STATUS", default=DRAFT)
    region = models.ForeignKey(Region, blank=True, null=True, related_name="questionnaire")
    parent = models.ForeignKey('Questionnaire', blank=True, null=True, related_name="children")

    def __unicode__(self):
        return '%s' % self.name

    def sub_sections(self):
        sections = self.sections.all()
        from questionnaire.models import SubSection

        return SubSection.objects.filter(section__in=sections)

    def get_all_questions(self):
        return Question.objects.filter(question_group__subsection__section__in=self.sections.all())

    def all_groups(self):
        return QuestionGroup.objects.filter(subsection__section__in=self.sections.all())

    def is_finalized(self):
        return self.status == Questionnaire.FINALIZED

    def is_published(self):
        return self.status == Questionnaire.PUBLISHED

    def is_archived(self):
        return self.status == Questionnaire.ARCHIVED

    def absolute_url(self):
        args = self.id, self.first_section().id
        return reverse('questionnaire_entry_page', args=args)

    def first_section(self):
        return self.sections.order_by('order')[0]

    def has_more_than_one_section(self):
        return self.sections.all().count() > 1

    def ordered_sections(self):
        return self.sections.order_by('order')

    def current_answer_version(self):
        answers = self.answers.filter(status='Draft')
        if answers.exists():
            return answers.latest('modified').version

    def _children_answers(self):
        return Answer.objects.filter(questionnaire__in=self.children.all())

    def is_archivable(self):
        return self.status == self.FINALIZED or (self.status == self.PUBLISHED and not self._children_answers().exists())

    def is_deletable(self):
        return not (self._children_answers().exists() or self.answers.exists()) and not self.is_last_questionnaire()

    def is_last_questionnaire(self):
        return Questionnaire.objects.filter(region__isnull=True).count() == 1

    def archive(self):
        self.status = self.ARCHIVED
        self.save()
        self._archive_children()

    def _archive_children(self):
        self.children.filter(region__isnull=False).update(status=self.ARCHIVED)

    def disasociate_and_archive_children(self):
        self._archive_children()
        self.children.clear()


class CountryQuestionnaireSubmission(BaseModel):
    country = models.ForeignKey(Country, blank=False, related_name="submissions")
    questionnaire = models.ForeignKey('Questionnaire', blank=False, related_name="submissions")
    version = models.IntegerField(blank=False, default=1)