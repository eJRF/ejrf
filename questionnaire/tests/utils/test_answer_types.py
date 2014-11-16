from questionnaire.utils.answer_type import AnswerTypes
from questionnaire.tests.base_test import BaseTest


class AnswerSubTypeTest(BaseTest):
    def test_returns_answer_types_as_a_tuple_of_tuples(self):
        expected_answer_types = (
            ('Date', 'Date'),
            ('MultiChoice', 'MultiChoice'),
            ('Text', 'Text'), ('Number', 'Number'),
            ('MultipleResponse', 'MultipleResponse')
        )

        self.assertEqual(expected_answer_types, AnswerTypes.answer_types())

    def test_returns_answer_sub_types_as_a_tuple_of_tuples(self):
        expected_sub_types = (
            ('DD/MM/YYYY', 'DD/MM/YYYY'),
            ('MM/YYYY', 'MM/YYYY'),
            ('Decimal', 'Decimal'),
            ('Integer', 'Integer')
        )
        self.assertEqual(expected_sub_types, AnswerTypes.answer_sub_types())
