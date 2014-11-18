from django.db import models

from questionnaire.models.base import BaseModel
from questionnaire.utils.model_utils import map_question_type_with


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

    def contains_or_sub_group_contains(self, question):
        if question in self.all_questions():
            return True
        else:
            return True in map(lambda group: group.contains_or_sub_group_contains(question), self.sub_groups())

    def sub_groups(self):
        return self.sub_group.all()

    def is_in_grid(self):
        if self.parent is not None:
            return self.grid or self.parent.is_in_grid()
        else:
            return self.grid

    def parent_group_id(self):
        if self.parent is not None:
            return self.parent.parent_group_id()
        else:
            return self.id

    def is_in_hybrid_grid(self):
        if self.parent is not None:
            return self.hybrid or self.parent.is_in_hybrid_grid()
        else:
            return self.hybrid


    def and_sub_group_questions(self):
        questions = list(self.all_questions())
        for sub_group in self.sub_groups():
            questions.extend(sub_group.all_questions())
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