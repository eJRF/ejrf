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
        self.SUCCESS_MESSAGE = 'The %ss were reordered successfully!' % self.obj.__class__.__name__

    def reorder(self):
        all_objects = list(self.klass.objects.filter(**self.kwargs).order_by('order', '-modified'))
        object_to_swap = all_objects.pop(self.obj.order - 1)
        all_objects.insert(self.new_order - 1, object_to_swap)
        for index, obj in enumerate(all_objects):
            obj.order = index + 1
            obj.save()
        return self.SUCCESS_MESSAGE