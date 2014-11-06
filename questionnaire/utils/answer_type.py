import itertools


class AnswerTypes(object):
    NUMBER = "Number"
    INTEGER = "Integer"
    DECIMAL = "Decimal"

    MULTI_CHOICE = "MultiChoice"
    DATE = "Date"

    VALID_TYPES = {
        DATE: (
            "DD/MM/YYYY",
            "MM/YYYY"
        ),
        MULTI_CHOICE: (
            "MultipleResponse",
            "SingleResponse"
        ),
        NUMBER: (
            DECIMAL,
            INTEGER
        ),
        "Text": ()
    }

    @classmethod
    def answer_types(cls):
        return tuple(map(lambda (k, v): (k, k), cls.VALID_TYPES.iteritems()))

    @classmethod
    def answer_sub_types(cls):
        subtypes = filter(None, [v for (k, v) in cls.VALID_TYPES.iteritems()])
        return tuple(map(lambda v: (v, v), itertools.chain(*subtypes)))
