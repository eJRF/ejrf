from questionnaire.forms.skip_question_form import SkipQuestionRuleForm
from questionnaire.models import SkipQuestion, QuestionGroupOrder
from questionnaire.tests.base_test import BaseTest
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.question_group_factory import QuestionGroupFactory
from questionnaire.tests.factories.question_option_factory import QuestionOptionFactory
from questionnaire.tests.factories.sub_section_factory import SubSectionFactory


class SkipQuestionRuleFormTest(BaseTest):
    def setUp(self):
        self.root_question = QuestionFactory()
        self.question_to_skip = QuestionFactory()
        self.response = QuestionOptionFactory(question=self.root_question)
        self.subsection = SubSectionFactory()
        self.question_group = QuestionGroupFactory()

        self.root_question.question_group.add(self.question_group)
        self.question_to_skip.question_group.add(self.question_group)
        self.subsection.question_group.add(self.question_group)

        self.form_data = {'root_question': self.root_question.id,
                          'response': self.response.id,
                          'skip_question': self.question_to_skip.id,
                          'subsection': self.subsection.id}
        QuestionGroupOrder.objects.create(question=self.root_question, question_group=self.question_group, order=1)
        QuestionGroupOrder.objects.create(question=self.question_to_skip, question_group=self.question_group, order=2)


    def test_save(self):
        skip_question_form = SkipQuestionRuleForm(data=self.form_data)

        skip_question_form.save()
        skip_question_rules = SkipQuestion.objects.filter(**self.form_data)
        self.assertEqual(skip_question_rules.count(), 1)

    def test_invalid_if_skip_question_is_same_as_root_question(self):
        data = {'root_question': self.root_question.id,
                'response': self.response.id,
                'skip_question': self.root_question.id,
                'subsection': self.subsection.id}

        skip_question_form = SkipQuestionRuleForm(data=data)
        self.assertFalse(skip_question_form.is_valid())

    def test_invalid_if_root_question_and_root_question_does_not_belong_to_subsection(self):
        root_question1 = QuestionFactory()
        question_another_group = QuestionGroupFactory()
        subsection = SubSectionFactory()

        root_question1.question_group.add(question_another_group)
        subsection.question_group.add(question_another_group)

        data = {'root_question': root_question1.id,
                'response': self.response.id,
                'skip_question': self.question_to_skip.id,
                'subsection': self.subsection.id}
        skip_question_rule_form = SkipQuestionRuleForm(data=data)
        self.assertFalse(skip_question_rule_form.is_valid())

    def test_is_invalid_if_question_option_is_not_valid_option(self):
        invalid_option = QuestionOptionFactory()

        data = {'root_question': self.root_question.id,
                'response': invalid_option.id,
                'skip_question': self.question_to_skip.id,
                'subsection': self.subsection.id}

        skip_question_rule_form = SkipQuestionRuleForm(data=data)
        self.assertFalse(skip_question_rule_form.is_valid())

    def test_is_invalid_if_root_question_order_is_greater_than_skip_question(self):
        root_question = QuestionFactory()
        self.question_group.question.add(root_question)

        QuestionGroupOrder.objects.create(question=root_question, question_group=self.question_group, order=3)

        data = {'root_question': root_question.id,
                'response': self.response.id,
                'skip_question': self.question_to_skip.id,
                'subsection': self.subsection.id}

        skip_question_rule_form = SkipQuestionRuleForm(data=data)
        self.assertFalse(skip_question_rule_form.is_valid())