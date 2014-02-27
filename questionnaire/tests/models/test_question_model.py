from django.db import IntegrityError
from questionnaire.models import Questionnaire, Section, SubSection, Organization, Region, Country, QuestionGroup, \
    NumericalAnswer, Answer, QuestionGroupOrder, AnswerGroup
from questionnaire.models.questions import Question, QuestionOption
from questionnaire.tests.base_test import BaseTest


class QuestionTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan")
        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                                order=1,
                                                questionnaire=self.questionnaire, name="Reported Cases")
        self.sub_section_1 = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                       section=self.section_1)
        self.sub_section_2 = SubSection.objects.create(title="Another", order=2, section=self.section_1)
        self.organisation = Organization.objects.create(name="WHO")
        self.regions = Region.objects.create(name="The Afro", organization=self.organisation)
        self.country = Country.objects.create(name="Uganda")
        self.regions.countries.add(self.country)
        self.question1 = Question.objects.create(text='B. Number of cases tested',
                                                 instructions="Enter the total number of cases for which specimens were collected, and tested in laboratory",
                                                 UID='C00003', answer_type='Number')
        self.parent_group = QuestionGroup.objects.create(subsection=self.sub_section_1, name="Laboratory Investigation")
        self.parent_group.question.add(self.question1)

        self.question1_answer = NumericalAnswer.objects.create(question=self.question1, country=self.country,
                                                               status=Answer.SUBMITTED_STATUS, response=23)
        self.question1_answer_2 = NumericalAnswer.objects.create(question=self.question1, country=self.country,
                                                                 status=Answer.SUBMITTED_STATUS, response=1)

    def test_question_unicode(self):
        self.assertEqual(str(self.question1), 'B. Number of cases tested'.encode('utf8'))

    def test_question_fields(self):
        question = Question()
        fields = [str(item.attname) for item in question._meta.fields]
        self.assertEqual(11, len(fields))
        for field in ['id', 'created', 'modified', 'text', 'instructions', 'UID', 'answer_type',
                      'is_core', 'is_primary', 'is_required', 'export_label']:
            self.assertIn(field, fields)

    def test_question_store(self):
        question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        self.failUnless(question.id)
        self.assertEqual('Uganda Revision 2014 what what?', question.text)
        self.assertIsNone(question.instructions)
        self.assertEqual('abc123', question.UID)
        self.assertFalse(question.is_core)
        self.assertFalse(question.is_primary)
        self.assertFalse(question.is_required)

    def test_question_uid_is_unique(self):
        a_question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        question_with_same_uid = Question(text='haha', UID='abc123', answer_type='Text')
        self.assertRaises(IntegrityError, question_with_same_uid.save)

    def test_question_can_get_its_answers(self):
        self.assertEqual(2, len(self.question1.all_answers()))
        self.assertIn(self.question1_answer, self.question1.all_answers())
        self.assertIn(self.question1_answer_2, self.question1.all_answers())

    def test_question_knows_if_it_is_first_in_its_group(self):
        question2 = Question.objects.create(text='question 2', UID='C00004', answer_type='Number')
        question3 = Question.objects.create(text='question 3', UID='C00005', answer_type='Number')
        self.sub_group = QuestionGroup.objects.create(subsection=self.sub_section_1, name="subgroup",
                                                      parent=self.parent_group)
        self.sub_group.question.add(question2, question3)

        QuestionGroupOrder.objects.create(question=self.question1, question_group=self.parent_group, order=1)
        QuestionGroupOrder.objects.create(question=question2, question_group=self.parent_group, order=2)
        QuestionGroupOrder.objects.create(question=question3, question_group=self.parent_group, order=3)

        self.assertTrue(self.question1.is_first_in_group())
        self.assertTrue(question2.is_first_in_group())
        self.assertFalse(question3.is_first_in_group())

    def test_question_knows_if_it_is_last_in_its_group(self):
        question2 = Question.objects.create(text='question 2', UID='C00004', answer_type='Number')
        question3 = Question.objects.create(text='question 3', UID='C00005', answer_type='Number')
        self.sub_group = QuestionGroup.objects.create(subsection=self.sub_section_1, name="subgroup",
                                                      parent=self.parent_group)
        self.sub_group.question.add(question2, question3)

        QuestionGroupOrder.objects.create(question=self.question1, question_group=self.parent_group, order=1)
        QuestionGroupOrder.objects.create(question=question2, question_group=self.parent_group, order=2)
        QuestionGroupOrder.objects.create(question=question3, question_group=self.parent_group, order=3)

        self.assertFalse(self.question1.is_last_in_group())
        self.assertFalse(question2.is_last_in_group())
        self.assertTrue(question3.is_last_in_group())

    def test_question_knows_option_has_options(self):
        question = Question.objects.create(text='what do you drink?', UID='C_2013', answer_type='MultiChoice')
        QuestionOption.objects.create(text='tusker lager', question=question,
                                      instructions="Pick your favorite beer?")
        self.assertTrue(question.has_question_option_instructions())

        question = Question.objects.create(text='what do you drink?', UID='C_2014', answer_type='MultiChoice')
        QuestionOption.objects.create(text='tusker lager', question=question)
        self.assertFalse(question.has_question_option_instructions())

    def test_question_knows_latest_answer_for_draft_given_group_and_country(self):
        question1 = Question.objects.create(text='question1', UID='C00015', answer_type='Number', is_primary=True)
        question2 = Question.objects.create(text='question2', UID='C00016', answer_type='Number')
        question3 = Question.objects.create(text='question3', UID='C00017', answer_type='Number')
        self.parent_group.question.add(question1, question2)

        group2 = QuestionGroup.objects.create(subsection=self.sub_section_1, name="group2")
        group2.question.add(question3)

        question1_answer = NumericalAnswer.objects.create(question=question1, country=self.country,
                                                          status=Answer.DRAFT_STATUS, response=23)
        question2_answer = NumericalAnswer.objects.create(question=question2, country=self.country,
                                                          status=Answer.DRAFT_STATUS, response=1)
        question3_answer = NumericalAnswer.objects.create(question=question3, country=self.country,
                                                          status=Answer.SUBMITTED_STATUS, response=11)

        answer_group1 = AnswerGroup.objects.create(grouped_question=self.parent_group, row=1)
        answer_group1.answer.add(question1_answer, question2_answer)

        answer_group2 = AnswerGroup.objects.create(grouped_question=group2, row=1)
        answer_group2.answer.add(question3_answer)

        country_2 = Country.objects.create(name="Uganda 2")
        question1_answer_2 = NumericalAnswer.objects.create(question=question1, country=country_2,
                                                            status=Answer.DRAFT_STATUS, response=23)
        question2_answer_2 = NumericalAnswer.objects.create(question=question2, country=country_2,
                                                            status=Answer.DRAFT_STATUS, response=1)
        answer_group_2 = AnswerGroup.objects.create(grouped_question=self.parent_group, row=2)
        answer_group_2.answer.add(question1_answer_2, question2_answer_2)

        self.assertEqual(question1_answer, question1.latest_answer(self.parent_group, self.country))
        self.assertEqual(question2_answer, question2.latest_answer(self.parent_group, self.country))
        self.assertEqual(question3_answer, question3.latest_answer(group2, self.country))

        self.assertEqual(question1_answer_2, question1.latest_answer(self.parent_group, country_2))
        self.assertEqual(question2_answer_2, question2.latest_answer(self.parent_group, country_2))

    def test_get_next_uid_given_given_largest_uid_question(self):
        self.assertEqual('00004', Question.next_uid())

    def test_get_next_uid_given_given_largest_uid_is_9th(self):
        Question.objects.create(text='question 3', UID='C00009', answer_type='Number')
        self.assertEqual('00010', Question.next_uid())

    def test_knows_can_be_deleted(self):
        question = Question.objects.create(text='what do you drink?', UID='C_2014', answer_type='MultiChoice')
        self.assertTrue(question.can_be_deleted())

    def test_knows_can_not_be_deleted_when_answered(self):
        question = Question.objects.create(text='what do you drink?', UID='C_2014', answer_type='MultiChoice')
        country = Country.objects.create(name="Peru")
        Answer.objects.create(question=question, country=country, status="Submitted")
        self.assertFalse(question.can_be_deleted())

    def test_knows_is_in_latest_finalized_questionnaire(self):
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013, status=Questionnaire.FINALIZED)
        section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                                      questionnaire=questionnaire, name="Reported Cases")
        sub_section = SubSection.objects.create(title="Another", order=2, section=section_1)
        question1 = Question.objects.create(text='B. Number of cases tested',
                                                 instructions="Enter the total number of cases for which specimens were collected, and tested in laboratory",
                                                 UID='C00030', answer_type='Number')
        parent_group = QuestionGroup.objects.create(subsection=sub_section, name="Laboratory Investigation")
        parent_group.question.add(question1)
        self.assertTrue(question1.is_in_active_questionnaire())
        self.assertFalse(self.question1.is_in_active_questionnaire())



class QuestionOptionTest(BaseTest):

    def test_question_option_fields(self):
        question = QuestionOption()
        fields = [str(item.attname) for item in question._meta.fields]
        self.assertEqual(7, len(fields))
        for field in ['id', 'created', 'modified', 'text', 'instructions', 'question_id', 'UID']:
            self.assertIn(field, fields)

    def test_question_store(self):
        question = Question.objects.create(text='what do you drink?', UID='abc123', answer_type='Text')
        question_option = QuestionOption.objects.create(text='tusker lager', question=question)

        self.failUnless(question_option.id)
        self.assertEqual('tusker lager', question_option.text)
        self.assertEqual(question, question_option.question)
        self.assertEqual(None, question_option.instructions)
        self.assertEqual(None, question_option.UID)