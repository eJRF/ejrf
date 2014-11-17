import copy

from questionnaire.models import QuestionGroupOrder, QuestionGroup, SubSection
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


class SubSectionReIndexer:
    SUCCESS_MESSAGE = 'The subsections were reordered successfully!'

    def __init__(self, subsection, new_order):
        self.subsection = subsection
        self.new_order = number_from(new_order)

    def reorder(self):
        sub_sections = list(SubSection.objects.filter(section=self.subsection.section).order_by('order'))
        subsection_to_swap = sub_sections.pop(self.subsection.order - 1)
        sub_sections.insert(self.new_order - 1, subsection_to_swap)
        for index, sub_section in enumerate(sub_sections):
            sub_section.order = index + 1
            sub_section.save()
        return self.SUCCESS_MESSAGE