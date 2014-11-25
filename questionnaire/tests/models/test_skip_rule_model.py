from questionnaire.models.skip_rule import SkipQuestion, SkipSubsection
from questionnaire.tests.base_test import BaseTest
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.question_group_factory import QuestionGroupFactory
from questionnaire.tests.factories.skip_rule_factory import SkipQuestionRuleFactory, SkipSubsectionRuleFactory


class SkipQuestionRuleTest(BaseTest):
    def test_skip_rules_fields(self):
        skip_rule = SkipQuestion()
        fields = [str(item.attname) for item in skip_rule._meta.fields]
        self.assertEqual(9, len(fields))
        for field in ['id', 'created', 'modified', 'root_question_id', 'skip_question_id', 'subsection_id',
                      'response_id', 'region_id']:
            self.assertIn(field, fields)

    def test_skip_question_rule_stores(self):
        skip_question = SkipQuestionRuleFactory()
        self.failUnless(skip_question.id)

    def test_should_return_true_if_is_in_hybrid_grid(self):
        root_question = QuestionFactory()
        group = QuestionGroupFactory(grid=True, hybrid=True)
        group.question.add(root_question)
        skip_question = SkipQuestionRuleFactory(root_question=root_question, subsection=group.subsection)
        self.assertTrue(skip_question.is_in_hybrid_grid())


class SkipSubsectionRuleTest(BaseTest):
    def test_skip_rules_fields(self):
        skip_rule = SkipSubsection()
        fields = [str(item.attname) for item in skip_rule._meta.fields]
        self.assertEqual(9, len(fields))
        for field in ['id', 'created', 'modified', 'root_question_id', 'skip_subsection_id', 'subsection_id',
                      'response_id', 'region_id']:
            self.assertIn(field, fields)

    def test_skip_subsection_rule_stores(self):
        skip_subsection = SkipSubsectionRuleFactory()
        self.failUnless(skip_subsection.id)