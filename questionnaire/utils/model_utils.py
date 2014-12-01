import re
from decimal import Decimal, InvalidOperation
from questionnaire.models.users import UserProfile


INITIAL_UID = 1
MAX_UID_LENGTH = 5


def largest_uid(cls):
    uid_numbers = []
    all_question_uids = cls.objects.all().values_list('UID', flat=True)
    for uid in all_question_uids:
        uid_numbers.extend([int(num[0]) for num in re.findall(r'(\d+)|([\+-]?\d+)', uid)])
    return max(uid_numbers) if len(uid_numbers) > 0 else INITIAL_UID


def stringify(uid):
    return "0" * (MAX_UID_LENGTH - len(str(uid))) + str(uid)


def map_question_type_with(orders, mapping, option=''):
    for order in orders:
        order_dict = {'option': option, 'order': order}
        mapping[order.question.answer_type].append(order_dict)


def reindex_orders_in(cls, **kwargs):
    objects = cls.objects.filter(**kwargs).order_by('order')
    for index, object_ in enumerate(objects):
        object_.order = index + 1
        object_.save()


def number_from(chars):
    num = None
    try:
        num = Decimal(chars)
    except InvalidOperation:
        pass
    return num

def profiles_that_can_edit(obj):
    user_profiles = UserProfile.objects.all()
    if obj.is_core and obj.region:
        return []
    elif obj.is_core:
        return user_profiles.filter(region__isnull=True)
    return user_profiles.filter(region=obj.region)

