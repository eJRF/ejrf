from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Max
from questionnaire.models import Questionnaire, QuestionGroupOrder
from questionnaire.models.base import BaseModel
from questionnaire.utils.answer_type import AnswerTypes
from questionnaire.utils.model_utils import profiles_that_can_edit


class Section(BaseModel):
    name = models.CharField(max_length=100, blank=False, null=True)
    title = models.CharField(max_length=256, blank=False, null=False)
    order = models.IntegerField(blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    questionnaire = models.ForeignKey(Questionnaire, blank=False, null=False, related_name="sections")
    region = models.ForeignKey("Region", blank=False, null=True, related_name="sections")
    is_core = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def ordered_questions(self):
        question_orders = QuestionGroupOrder.objects.filter(question_group__subsection__in=self.sub_sections.all())
        orders = question_orders.order_by('question_group__subsection__order', 'question_group__order', 'order')
        return [group_question_order.question for group_question_order in orders]

    def mapped_question_orders(self):
        subsections = self.sub_sections.order_by('order')
        _orders = {type_[0]: [] for type_ in AnswerTypes.answer_types()}
        for subsection in subsections:
            for group in subsection.question_group.order_by('order'):
                group.map_orders_with_answer_type(_orders)
        return _orders

    class Meta:
        ordering = ('order',)
        app_label = 'questionnaire'

    def has_at_least_two_subsections(self):
        return self.sub_sections.count() > 1

    def get_absolute_url(self):
        args = self.questionnaire.id, self.id
        return reverse('questionnaire_entry_page', args=args)

    def is_last_in(self, questionnaire):
        return self.order == Section.get_next_order(questionnaire) - 1


    def profiles_with_edit_permission(self):
        return profiles_that_can_edit(self)

    @classmethod
    def get_next_order(cls, questionnaire):
        max_order = cls.objects.filter(questionnaire=questionnaire).aggregate(Max('order')).get('order__max')
        return max_order + 1 if max_order else 1


class SubSection(BaseModel):
    title = models.CharField(max_length=256, blank=True, null=True)
    order = models.IntegerField(blank=False, null=False)
    section = models.ForeignKey(Section, blank=False, null=False, related_name="sub_sections")
    description = models.TextField(blank=True, null=True)
    region = models.ForeignKey("Region", blank=False, null=True, related_name="sub_sections")
    is_core = models.BooleanField(default=False)

    class Meta:
        ordering = ('order',)
        app_label = 'questionnaire'

    def move_groups_down_from(self, group):
        groups_to_move = self.question_group.filter(parent__isnull=True, order__gte=group.order).exclude(id=group.id)
        for g in groups_to_move:
            g.order += 1
            g.save()

    def get_absolute_url(self):
        return self.section.get_absolute_url()

    def all_question_groups(self):
        return self.question_group.all()

    def all_questions(self):
        all_questions = []
        for question_group in self.all_question_groups():
            all_questions.extend(question_group.all_questions())
        return all_questions

    def to_dict(self):
        return {'title': self.title or 'Un-titled subsection %s' % self.order,
            'id': self.id,
            'order': self.order}

    def parent_question_groups(self):
        return self.question_group.filter(parent=None).exclude(question=None)

    def has_at_least_two_groups(self):
        return self.parent_question_groups().count() > 1

    def next_group_order(self):
        max_group_order = self.question_group.aggregate(Max('order')).get('order__max')
        return max_group_order + 1 if max_group_order else 0

    def profiles_with_edit_permission(self):
        return profiles_that_can_edit(self)

    @classmethod
    def get_next_order(cls, section_id):
        max_order = cls.objects.filter(section__id=section_id).aggregate(Max('order')).get('order__max')
        return max_order + 1 if max_order else 0

    def __unicode__(self):
        return "%s ,%s" % (str(self.order), self.title)