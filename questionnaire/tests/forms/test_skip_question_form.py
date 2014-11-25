from questionnaire.forms.skip_rule_form import SkipRuleForm, SkipQuestionForm, SkipSubsectionForm
from questionnaire.models import SkipRule, QuestionGroupOrder
from questionnaire.models.skip_rule import SkipQuestion
from questionnaire.tests.base_test import BaseTest
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.question_group_factory import QuestionGroupFactory
from questionnaire.tests.factories.question_option_factory import QuestionOptionFactory
from questionnaire.tests.factories.region_factory import RegionFactory
from questionnaire.tests.factories.skip_rule_factory import SkipQuestionRuleFactory, SkipSubsectionRuleFactory
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
        skip_question_form = SkipQuestionForm(data=self.form_data)
        skip_question_form.save()
        skip_question_rules = SkipQuestion.objects.filter(**self.form_data)
        self.assertEqual(skip_question_rules.count(), 1)

    def test_invalid_if_no_skip_question(self):
        data = {'root_question': self.root_question.id,
                'response': self.response.id,
                'subsection': self.subsection.id}

        skip_question_form = SkipQuestionForm(data=data)
        self.assertFalse(skip_question_form.is_valid())
        self.assertEqual({'skip_question': [u'This field is required.']}, skip_question_form.errors)

    def test_invalid_if_skip_question_is_same_as_root_question(self):
        data = {'root_question': self.root_question.id,
                'response': self.response.id,
                'skip_question': self.root_question.id,
                'subsection': self.subsection.id}

        skip_question_form = SkipQuestionForm(data=data)
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
        skip_question_rule_form = SkipQuestionForm(data=data)
        self.assertFalse(skip_question_rule_form.is_valid())

    def test_is_invalid_if_question_option_is_not_valid_option(self):
        invalid_option = QuestionOptionFactory()

        data = {'root_question': self.root_question.id,
                'response': invalid_option.id,
                'skip_question': self.question_to_skip.id,
                'subsection': self.subsection.id}

        skip_question_rule_form = SkipRuleForm(data=data)
        self.assertFalse(skip_question_rule_form.is_valid())

    def test_is_invalid_if_root_question_order_is_greater_than_skip_question(self):
        root_question = QuestionFactory()
        self.question_group.question.add(root_question)

        QuestionGroupOrder.objects.create(question=root_question, question_group=self.question_group, order=3)

        data = {'root_question': root_question.id,
                'response': self.response.id,
                'skip_question': self.question_to_skip.id,
                'subsection': self.subsection.id}

        skip_question_rule_form = SkipRuleForm(data=data)
        self.assertFalse(skip_question_rule_form.is_valid())

    def test_is_skip_question_unique(self):
        SkipQuestionRuleFactory(subsection=self.subsection, root_question=self.root_question, response=self.response,
                                skip_question=self.question_to_skip)
        skip_question_form = SkipQuestionForm(data=self.form_data)
        is_valid = skip_question_form.is_valid()
        self.assertFalse(is_valid)
        errors = 'This rule already exists'
        self.assertIn(errors, skip_question_form.errors['root_question'])


class SkipQuestionInHybridGridFormTest(BaseTest):
    def setUp(self):
        root_question = QuestionFactory()
        question_to_skip = QuestionFactory()
        response = QuestionOptionFactory(question=root_question)

        self.subsection = SubSectionFactory()
        hybrid_grid_group = QuestionGroupFactory(hybrid=True, order=1)

        root_question.question_group.add(hybrid_grid_group)
        question_to_skip.question_group.add(hybrid_grid_group)

        self.subsection.question_group.add(hybrid_grid_group)

        self.form_data = {'root_question': root_question.id,
                          'response': response.id,
                          'skip_question': question_to_skip.id,
                          'subsection': self.subsection.id}

        QuestionGroupOrder.objects.create(question=root_question, question_group=hybrid_grid_group, order=1)
        QuestionGroupOrder.objects.create(question=question_to_skip, question_group=hybrid_grid_group, order=2)

    def test_invalid_if_root_question_is_in_hybrid_grid_and_skip_question_not(self):
        question_to_skip = QuestionFactory()
        question_group = QuestionGroupFactory(order=2)
        question_to_skip.question_group.add(question_group)
        self.subsection.question_group.add(question_group)
        QuestionGroupOrder.objects.create(question=question_to_skip, question_group=question_group, order=2)

        form_data = self.form_data
        form_data['skip_question'] = question_to_skip.id

        skip_question_rule_form = SkipQuestionForm(data=form_data)
        self.assertFalse(skip_question_rule_form.is_valid())
        self.assertEqual({'skip_question': [u'Question to skip must be in the same hybrid grid']},
                         skip_question_rule_form.errors)

    def test_valid_if_root_question_and_skip_question_are_in_hybrid_grid(self):
        skip_question_form = SkipQuestionForm(data=self.form_data)
        self.assertTrue(skip_question_form.is_valid())


class SkipSubsectionRuleFormTest(BaseTest):
    def setUp(self):
        self.root_question = QuestionFactory()
        self.response = QuestionOptionFactory(question=self.root_question)
        self.subsection = SubSectionFactory(title="outside subsection", order=2)
        self.subsection_to_skip = SubSectionFactory()
        self.question_group = QuestionGroupFactory()

        self.root_question.question_group.add(self.question_group)
        self.subsection.question_group.add(self.question_group)

        self.form_data = {'root_question': self.root_question.id,
                          'response': self.response.id,
                          'skip_subsection': self.subsection_to_skip.id,
                          'subsection': self.subsection.id}
        QuestionGroupOrder.objects.create(question=self.root_question, question_group=self.question_group, order=1)

    def test_is_skip_subsection_is_unique(self):
        SkipSubsectionRuleFactory(subsection=self.subsection, root_question=self.root_question,
                                  response=self.response, skip_subsection=self.subsection_to_skip)
        skip_question_form = SkipSubsectionForm(data=self.form_data)
        is_valid = skip_question_form.is_valid()
        self.assertFalse(is_valid)
        errors = 'This rule already exists'
        self.assertIn(errors, skip_question_form.errors['root_question'])

    def test_is_invalid_if_root_question_is_in_the_subsection_to_skip(self):
        data = self.form_data
        data['skip_subsection'] = self.subsection.id
        skip_subsection_rule_form = SkipSubsectionForm(data=data)
        self.assertFalse(skip_subsection_rule_form.is_valid())
        errors = 'You cannot skip the subsection which the root question is in.'
        self.assertIn(errors, skip_subsection_rule_form.errors['skip_subsection'])

    def test_is_invalid_if_root_question_subsection_has_order_greater_than_subsection_to_skip(self):
        subsection = SubSectionFactory(order=1)
        question_group = QuestionGroupFactory()
        root_question = QuestionFactory(text='Another question')
        root_question.question_group.add(question_group)
        subsection.question_group.add(question_group)

        data = self.form_data
        data['skip_subsection'] = subsection.id
        skip_subsection_rule_form = SkipSubsectionForm(data=data)
        self.assertFalse(skip_subsection_rule_form.is_valid())
        errors = 'The subsection you have specified to skip comes before the root question.'
        self.assertIn(errors, skip_subsection_rule_form.errors['skip_subsection'])


class RegionalAdminSkipQuestionRuleFormTest(BaseTest):
    def setUp(self):
        self.region = RegionFactory()
        self.root_question = QuestionFactory()
        self.question_to_skip = QuestionFactory()
        self.response = QuestionOptionFactory(question=self.root_question)
        self.subsection = SubSectionFactory(region=self.region)
        self.question_group = QuestionGroupFactory(subsection=self.subsection)

        self.root_question.question_group.add(self.question_group)
        self.question_to_skip.question_group.add(self.question_group)

        self.form_data = {'root_question': self.root_question.id,
                          'response': self.response.id,
                          'skip_question': self.question_to_skip.id,
                          'subsection': self.subsection.id}
        QuestionGroupOrder.objects.create(question=self.root_question, question_group=self.question_group, order=1)
        QuestionGroupOrder.objects.create(question=self.question_to_skip, question_group=self.question_group, order=2)

    def test_is_valid_when_region_is_owner_of_skip_question(self):
        skip_question_form = SkipQuestionForm(data=self.form_data, initial={'region': None})
        self.assertTrue(skip_question_form.is_valid())

    def test_should_save_skip_rule_with_region(self):
        skip_question_form = SkipQuestionForm(data=self.form_data, initial={'region': None})
        skip_question_rule = skip_question_form.save()

        self.assertIsNone(skip_question_rule.region)
        self.assertEqual(skip_question_rule.root_question, self.root_question)

    def test_should_be_invalid_when_region_is_given_and_skip_question_belongs_other_region(self):
        region = RegionFactory()
        skip_question_form = SkipQuestionForm(data=self.form_data, initial={'region': region})

        self.assertFalse(skip_question_form.is_valid())
        message = 'Question to skip must belong to %s' % region.name
        self.assertIn(message, skip_question_form.errors['skip_question'])

    def test_save_skip_rule(self):
        question_to_skip = QuestionFactory(region=self.region)
        self.question_group.question.add(question_to_skip)

        QuestionGroupOrder.objects.create(question=question_to_skip, question_group=self.question_group, order=2)
        data = self.form_data
        data['skip_question'] = question_to_skip.id
        skip_question_form = SkipQuestionForm(data=data, initial={'region': self.region})
        skip_question_form.is_valid()
        skip_question_rule = skip_question_form.save()

        self.assertEqual(skip_question_rule.region, self.region)
        self.assertEqual(skip_question_rule.root_question, self.root_question)