import copy

from questionnaire.models import QuestionGroupOrder, QuestionGroup, SubSection, Section
from questionnaire.utils.model_utils import number_from


class QuestionReIndexer(object):
    NEW_ORDER_INDEX = 2
    OLD_ORDER_ID_INDEX = 1
    GROUP_ID_INDEX = 0
    EXPECTED_KEYS = ["Number", "Date", "MultiChoice", "Text"]
    ORDER = 'order'

    def __init__(self, data):
        self.data = data
        self.cleaned_data = self.clean_data_posted()

    def reorder_questions(self):
        for order, posted_value in self.get_old_orders().items():
            posted_group_id = int(posted_value[self.GROUP_ID_INDEX])
            posted_order = int(posted_value[self.NEW_ORDER_INDEX]) + 1
            if order.question_group.id is not posted_group_id:
                new_group = QuestionGroup.objects.get(id=posted_group_id)
                old_question_group = QuestionGroup.objects.get(id=order.question_group.id)
                old_question_group.question.remove(order.question)
                new_group.question.add(order.question)
                order.question_group = new_group
                order.order = posted_order
                order.save()
            order.order = posted_order
            order.save()

    def get_old_orders(self):
        orders = {}
        for posted_order_values in dict(self.cleaned_data).values():
            orders.update(
                {QuestionGroupOrder.objects.get(id=posted_order_values[self.OLD_ORDER_ID_INDEX]): posted_order_values})
        return orders

    def clean_data_posted(self):
        data = copy.deepcopy(self.data)
        clean_keys = filter(lambda key: self.is_allowed(key), data.keys())
        cleaned_data = (dict((key, self.clean_values(value)) for key, value in data.iteritems() if key in clean_keys))
        return cleaned_data

    def is_allowed(self, key):
        for name in self.EXPECTED_KEYS:
            if key.startswith(name) and key.endswith(self.ORDER):
                return True
        return False

    def clean_values(self, value):
        value = filter(None, value)
        return value.split(",")


class OrderBasedReIndexer:

    def __init__(self, obj, new_order, **kwargs):
        self.obj = obj
        self.kwargs = kwargs
        self.new_order = number_from(new_order)
        self.klass = eval(self.obj.__class__.__name__)
        self.SUCCESS_MESSAGE = 'The %ss were reordered successfully!' % self.klass

    def _get_old_order(self, all_objects):
        if self.obj.id:
            return all_objects.get(id=self.obj.id).order
        return max(all_objects.values_list('order', flat=True)) + 1

    def reorder(self):
        all_objects = self.klass.objects.filter(**self.kwargs).order_by('order')
        order_to_move_from = self._get_old_order(all_objects)
        objects_to_move = self._get_objects_to_move(all_objects, order_to_move_from)
        for obj in objects_to_move:
            obj.order += self._move_delta(order_to_move_from)
            obj.save()
        self.obj.order = self.new_order
        self.obj.save()
        return self.SUCCESS_MESSAGE

    def _get_objects_to_move(self, all_objects, order_to_move_from):
        if self._moving_up(order_to_move_from):
            return all_objects.filter(order__gte=self.new_order, order__lte=order_to_move_from)
        return all_objects.filter(order__gte=order_to_move_from, order__lte=self.new_order)

    def _moving_up(self, old_order):
        return self.new_order < old_order

    def _move_delta(self, order_to_move_from):
        if self._moving_up(order_to_move_from):
            return 1
        return -1

class GridReorderer:
    ONE_BELOW_CURRENT_GROUP_ORDER = 1

    def __init__(self, group, move_direction):
        self.move_direction = move_direction
        self.group = group
        self.message = {'success': 'The Grid was successfully moved ' + move_direction }

    def _is_not_last_question_group(self):
        return self.group.order < self.group.subsection.question_group.filter(parent__isnull=True).count()

    def _move_and_create_group(self, group_in_move_direction, question_to_move, difference_in_pos):
        new_group = self.group.subsection.question_group.create(order=self.group.order + difference_in_pos)
        self.group.subsection.move_groups_down_from(new_group)
        group_in_move_direction.remove_question_and_reorder(question_to_move)
        new_group.add_question(question_to_move, 1)

    def _move_up(self):
        if self.group.order > 1:
            previous_group_order = self.group.order - 1
            group_above = self.group.subsection.question_group.get(order=previous_group_order)
            if group_above.is_grid_or_has_less_than_two_question():
                self.group.swap_order(group_above)
            else:
                question_to_move = group_above.ordered_questions()[::-1][0]
                self._move_and_create_group(group_above, question_to_move, self.ONE_BELOW_CURRENT_GROUP_ORDER)
        else:
            self.message = {'warning': 'The Grid was not moved up because its the first in this subsection' }

    def _move_down(self):
        if self._is_not_last_question_group():
            next_group_order = self.group.order + 1
            group_below = self.group.subsection.question_group.get(order=next_group_order)
            if group_below.is_grid_or_has_less_than_two_question():
                self.group.swap_order(group_below)
            else:
                question_to_move = group_below.ordered_questions()[0]
                self._move_and_create_group(group_below, question_to_move, 0)
        else:
            self.message = {'warning': 'The Grid was not moved down because its the last in this subsection' }

    def _remove_empty_groups(self):
        groups = self.group.subsection.question_group.all()
        QuestionGroup.delete_empty_groups(groups)

    def reorder_group_in_sub_section(self):
        if self.move_direction == "up":
            self._move_up()
        else:
            self._move_down()
        self._remove_empty_groups()