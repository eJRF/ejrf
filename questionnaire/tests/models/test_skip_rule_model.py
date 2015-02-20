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

    def test_skip_question_rule_to_dictionary(self):
        root_question = QuestionFactory()
        group = QuestionGroupFactory(grid=True, hybrid=True)
        group.question.add(root_question)
        skip_question = SkipQuestionRuleFactory(root_question=root_question, subsection=group.subsection)

        user = self.create_user(username='global_user', org='WHO')
        group_id = skip_question.subsection.question_group.all()[0].id
        expected_dictionary = {'id': skip_question.id,
                               'skip_question': skip_question.skip_question.text,
                               'root_question': skip_question.root_question.text,
                               'response': skip_question.response.text,
                               'is_in_grid': True,
                               'group_id': group_id,
                               'can_delete': True
        }
        self.assertEqual(skip_question.to_dictionary(user), expected_dictionary)


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

    def test_skip_subsection_rule_to_dictionary(self):
        skip_subsection = SkipSubsectionRuleFactory()
        user = self.create_user(username='global_user', org='WHO')
        expected_dictionary = {'id': skip_subsection.id,
                               'skip_subsection': (" %s. %s" % (skip_subsection.skip_subsection.order,
                                                                skip_subsection.skip_subsection.title)),
                               'root_question': skip_subsection.root_question.text,
                               'response': skip_subsection.response.text,
                               'can_delete': True
        }

        self.assertEqual(skip_subsection.to_dictionary(user), expected_dictionary)