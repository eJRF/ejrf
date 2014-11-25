import json

from django.test import Client

from questionnaire.tests.base_test import BaseTest
from questionnaire.models import Question, SkipRule, QuestionOption, Questionnaire, Section, SubSection, \
    QuestionGroup, QuestionGroupOrder
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.question_group_factory import QuestionGroupFactory
from questionnaire.tests.factories.region_factory import RegionFactory
from questionnaire.tests.factories.skip_rule_factory import SkipQuestionRuleFactory
from questionnaire.tests.factories.sub_section_factory import SubSectionFactory


class SkipRuleViewPostTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.url = "/questionnaire/subsection/skiprules/"
        user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.assign('can_edit_questionnaire', user)
        self.client.login(username=user.username, password='pass')
        region = None

        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, region=region)

        section = Section.objects.create(name="section", questionnaire=questionnaire, order=1)

        subsection = SubSection.objects.create(title="subsection 1", section=section, order=1)
        subsection2 = SubSection.objects.create(title="subsection 2", section=section, order=1)
        subsection3 = SubSection.objects.create(title="subsection 2", section=section, order=1)
        self.subsection_id = subsection.pk
        question_group = QuestionGroup.objects.create(subsection_id=subsection.id)

        root_question = Question.objects.create(text='Q1', UID='C00003', answer_type='MultiChoice', region=region)
        skip_question = Question.objects.create(text='Q2', UID='C00004', answer_type='Number', region=region)
        self.random_question = Question.objects.create(text='Q3', UID='C00005', answer_type='Number', region=region)

        question_group.question.add(root_question)
        question_group.question.add(skip_question)
        question_group.question.add(self.random_question)
        QuestionGroupOrder.objects.create(question=root_question, question_group=question_group, order=1)
        QuestionGroupOrder.objects.create(question=skip_question, question_group=question_group, order=2)

        self.subsection_with_only_root_question = subsection3.pk
        question_group2 = QuestionGroup.objects.create(subsection_id=self.subsection_with_only_root_question)
        question_group2.question.add(root_question)

        self.subsection_with_only_skip_question = subsection2.pk
        question_group3 = QuestionGroup.objects.create(subsection_id=self.subsection_with_only_skip_question)
        question_group3.question.add(skip_question)

        response = QuestionOption.objects.create(text="Some response", question=root_question, UID="U0003")
        self.form_data = {'root_question': str(root_question.pk),
                          'response': str(response.pk),
                          'skip_question': str(skip_question.pk),
                          'subsection': str(self.subsection_id)}

    def test_post_skip_question(self):
        self.assertEqual(SkipRule.objects.all().count(), 0)
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(SkipRule.objects.all().count(), 1)

    def test_post_skip_question_for_root_question_not_existing(self):
        self.assertEqual(SkipRule.objects.all().count(), 0)
        data = self.form_data
        data['root_question'] = '341543'
        response = self.client.post(self.url, data=data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(SkipRule.objects.all().count(), 0)
        expected_errors = [u'Select a valid choice. That choice is not one of the available choices.']

        self.assertEqual(json.loads(response.content)['result'], expected_errors)

    def test_post_skip_question_for_response_not_existing(self):
        self.assertEqual(SkipRule.objects.all().count(), 0)
        data = self.form_data
        data['response'] = '341543'
        response = self.client.post(self.url, data=data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(SkipRule.objects.all().count(), 0)
        expected_error_message = [u'The selected option is not a valid option for the root question']
        self.assertEqual(json.loads(response.content)['result'], expected_error_message)

    def test_post_skip_question_for_skip_question_not_existing(self):
        self.assertEqual(SkipRule.objects.all().count(), 0)
        data = self.form_data
        data['skip_question'] = '341543'
        response = self.client.post(self.url, data=data)
        self.assertEqual(400, response.status_code)

        self.assertEqual(SkipRule.objects.all().count(), 0)
        expected_error_message = [u'Select a valid choice. That choice is not one of the available choices.']
        self.assertEqual(json.loads(response.content)['result'], expected_error_message)

    def test_post_skip_question_for_root_question_not_being_part_of_subsection(self):
        self.assertEqual(SkipRule.objects.all().count(), 0)
        data = self.form_data
        data['subsection'] = self.subsection_with_only_skip_question
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(400, response.status_code)

        self.assertEqual(SkipRule.objects.all().count(), 0)
        self.assertEqual(json.loads(response.content)['result'],
                         [u'Both questions should belong to the same subsection'])

    def test_post_skip_question_for_skip_question_not_being_part_of_subsection(self):
        self.assertEqual(SkipRule.objects.all().count(), 0)
        data = self.form_data
        data['subsection'] = self.subsection_with_only_root_question
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(400, response.status_code)

        self.assertEqual(SkipRule.objects.all().count(), 0)
        self.assertEqual(json.loads(response.content)['result'],
                         [u'Both questions should belong to the same subsection'])

    def test_post_skip_question_for_response_one_of_root_questions_options(self):
        self.assertEqual(SkipRule.objects.all().count(), 0)
        data = self.form_data
        data['response'] = str(int(data['response']) + 10)
        response = self.client.post(self.url, data=data)
        self.assertEqual(400, response.status_code)

        expected_error_message = [u'The selected option is not a valid option for the root question']
        self.assertEqual(json.loads(response.content)['result'], expected_error_message)
        self.assertEqual(SkipRule.objects.all().count(), 0)

    def test_post_skip_question_root_question_is_not_equal_to_skip_question(self):
        self.assertEqual(SkipRule.objects.all().count(), 0)
        data = self.form_data
        data['skip_question'] = data['root_question']
        response = self.client.post(self.url, data=data)
        self.assertEqual(400, response.status_code)

        self.assertEqual(SkipRule.objects.all().count(), 0)
        self.assertEqual(json.loads(response.content)['result'], [u'Root question cannot be the same as skip question'])


class SkipQuestionGetTest(BaseTest):

    def setUp(self):
        self.subsection = SubSectionFactory()
        self.question_group = QuestionGroupFactory(grid=True, hybrid=True)
        self.question = QuestionFactory()
        self.question_group.question.add(self.question)
        self.skip_rule = SkipQuestionRuleFactory(root_question=self.question, subsection=self.question_group.subsection)
        self.client = Client()
        user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.assign('can_edit_questionnaire', user)
        self.client.login(username=user.username, password='pass')
        self.url = "/questionnaire/subsection/%d/skiprules/" % self.subsection.id

    def test_get_existing_skip_rules(self):
        self.assertEqual(SkipRule.objects.all().count(), 1)
        response = self.client.get(self.url)
        expected_data = [
            {"skip_question": "A nice question", "root_question": "A nice question", "is_in_hygrid": True, "id": 1,
             "response": "Yes"}]

        self.assertEqual(expected_data, json.loads(response.content))
        self.assertEqual(response.status_code, 200)


class RegionalSkipQuestionGetTest(BaseTest):
    def setUp(self):
        self.client = Client()
        user = self.create_user(group=self.REGIONAL_ADMIN, org="WHO", region='AFR')
        region = user.user_profile.region
        self.assign('can_edit_questionnaire', user)
        self.client.login(username=user.username, password='pass')

        self.global_question_group = QuestionGroupFactory(grid=True, hybrid=True)
        self.global_question = QuestionFactory()
        self.global_question_group.question.add(self.global_question)
        group_subsection = self.global_question_group.subsection
        self.global_skip_rule = SkipQuestionRuleFactory(root_question=self.global_question,
                                                        subsection=group_subsection,
                                                        region=None)
        asia = RegionFactory(name='ASIAN')
        SkipQuestionRuleFactory(root_question=self.global_question, subsection=group_subsection, region=asia)

        self.question_group = QuestionGroupFactory(grid=True, hybrid=True, subsection=group_subsection)
        self.question = QuestionFactory(text='regional question')
        self.question_group.question.add(self.question)
        self.skip_rule = SkipQuestionRuleFactory(root_question=self.question,
                                                 subsection=group_subsection,
                                                 region=region)

        self.url = "/questionnaire/subsection/%d/skiprules/" % self.global_skip_rule.subsection.id

    def test_get_existing_skip_rules(self):
        response = self.client.get(self.url)
        global_rules = {"skip_question": "A nice question",
                        "root_question": "A nice question",
                        "is_in_hygrid": True,
                        "id": self.global_skip_rule.id, "response": "Yes"}

        regional_rules = {u"skip_question": u"A nice question",
                          u"root_question": u"regional question",
                          u"is_in_hygrid": True,
                          u"id": self.skip_rule.id,
                          u"response": u"Yes"}

        self.assertEqual(response.status_code, 200)
        json_loads = json.loads(response.content)

        self.assertEqual(global_rules, json_loads['global_rules'][0])
        self.assertEqual(regional_rules, json_loads['regional_rules'][0])

class SkipQuestionDeleteTest(BaseTest):

    def setUp(self):
        self.skip_rule = SkipQuestionRuleFactory()
        self.client = Client()
        user = self.create_user(group=self.GLOBAL_ADMIN, org="WHO")
        self.assign('can_edit_questionnaire', user)
        self.client.login(username=user.username, password='pass')

    def test_should_delete_skip_rule_when_it_exists(self):
        #given
        url = '/questionnaire/subsection/skiprule/%d/' % self.skip_rule.id
        #when
        response = self.client.delete(url)
        #then
        self.assertEqual(200, response.status_code)
        self.assertEqual(SkipRule.objects.filter(id=self.skip_rule.id).count(), 0)

    def test_should_not_delete_skip_rule_when_it_doesnt_exists(self):
        #given
        url = '/questionnaire/subsection/skiprule/%d/' % (self.skip_rule.id + 1)
        #when
        response = self.client.delete(url)
        #then
        self.assertEqual(204, response.status_code)
        self.assertEqual(SkipRule.objects.filter(id=self.skip_rule.id).count(), 1)
