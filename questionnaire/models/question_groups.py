from django.db import models
from django.db.models import Max

from questionnaire.models.base import BaseModel
from questionnaire.utils.model_utils import map_question_type_with, profiles_that_can_edit


class QuestionGroup(BaseModel):
    question = models.ManyToManyField("Question", blank=False, null=False, related_name="question_group")
    subsection = models.ForeignKey("SubSection", blank=False, null=False, related_name="question_group")
    name = models.CharField(max_length=200, blank=False, null=True)
    instructions = models.TextField(blank=False, null=True)
    parent = models.ForeignKey("QuestionGroup", null=True, related_name="sub_group")
    order = models.PositiveIntegerField(null=True, blank=False)
    allow_multiples = models.BooleanField(default=False)
    grid = models.BooleanField(default=False)
    display_all = models.BooleanField(default=False)
    hybrid = models.BooleanField(default=False)
    is_core = models.BooleanField(default=False)

    @property
    def region(self):
        questions_with_region = self.all_questions().exclude(region=None)
        if questions_with_region.exists():
            return questions_with_region[0].region
        return None

    class Meta:
        ordering = ('order',)
        app_label = 'questionnaire'

    def all_questions(self):
        return self.question.all()

    def swap_order(self, other_group):
        self_order = self.order
        other_order = other_group.order

        self.order = other_order
        other_group.order = self_order
        self.save()
        other_group.save()

    def contains_or_sub_group_contains(self, question):
        return question in self.ordered_questions()

    def sub_groups(self):
        all_groups = list(self.sub_group.all())
        for group in self.sub_group.all():
            all_groups.extend(list(group.sub_groups()))
        return all_groups

    def is_in_grid(self):
        if self.parent is not None:
            return self.grid or self.parent.grid
        return self.grid

    def parent_group(self):
        if self.parent:
            return self.parent
        return self

    def parent_group_id(self):
        return self.parent_group().id

    def is_in_hybrid_grid(self):
        if self.parent:
            return self.hybrid or self.parent.hybrid
        return self.hybrid

    def remove_question(self, question):
        self.orders.filter(question=question).delete()
        if question in self.question.all():
            self.question.remove(question)
        map(lambda sub_group: sub_group.remove_question(question), self.sub_group.all())

    @classmethod
    def next_order_in(cls, subsection):
        first_order = 1
        max_orders = cls.objects.filter(subsection=subsection, parent__isnull=True).aggregate(Max('order')).get('order__max')
        return max_orders + 1 if max_orders else first_order

    @classmethod
    def delete_empty_groups(cls, subsection):
        groups = cls.objects.filter(subsection=subsection)
        for group in groups:
            if not group.question.exists():
                group.delete()

    def add_question(self, question, order):
        self.question.add(question)
        question.orders.create(question_group=self, order=order)

    def remove_question_and_reorder(self, question):
        self.remove_question(question)
        for i, q in enumerate(self.orders.order_by('order')):
            q.order = i + 1
            q.save()

    def is_grid_or_has_less_than_two_question(self):
        return self.grid or (len(self.and_sub_group_questions()) <= 1)

    def and_sub_group_questions(self):
        questions = list(self.all_questions())
        for sub_group in self.sub_groups():
            questions.extend(sub_group.and_sub_group_questions())
        return questions

    def ordered_questions(self):
        return [order.question for order in self.question_orders()]

    def question_orders(self):
        if self.parent:
            return self.parent.orders.order_by('order').filter(question__in=self.all_questions()).select_related()
        return self.orders.order_by('order').select_related()

    def has_at_least_two_questions(self):
        return self.question.count() > 1

    def primary_question(self):
        by_attribute = self.question.filter(is_primary=True)
        if by_attribute.exists():
            return by_attribute[0]
        by_order = self.orders.order_by('order')
        if by_order.exists():
            return by_order[0].question
        return None

    def all_non_primary_questions(self):
        non_primary_questions = self.ordered_questions()
        non_primary_questions.remove(self.primary_question())
        return non_primary_questions

    def has_subgroups(self):
        return self.sub_group.exists()

    def max_questions_order(self):
        group_orders = self.orders.order_by('-order')
        if group_orders.exists():
            return group_orders[0].order
        return 0

    def map_orders_with_answer_type(self, mapped_orders):
        orders = self.orders.order_by('order').select_related()
        if self.primary_question() and self.grid and self.display_all:
            for option in self.primary_question().options.all():
                map_question_type_with(orders, mapped_orders, option)
        else:
            map_question_type_with(orders, mapped_orders)