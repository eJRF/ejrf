from questionnaire.models import Section, SubSection, Organization, Region, Country, NumericalAnswer, Answer, Question, \
    QuestionGroup
from questionnaire.models.questionnaires import Questionnaire
from questionnaire.tests.base_test import BaseTest
from questionnaire.tests.factories.questionnaire_factory import QuestionnaireFactory
from questionnaire.tests.factories.answer_factory import NumericalAnswerFactory


class QuestionnaireTest(BaseTest):
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
        self.sub_group = QuestionGroup.objects.create(subsection=self.sub_section_1, name="Laboratory Investigation")
        self.sub_group.question.add(self.question1)

        self.question1_answer = NumericalAnswer.objects.create(question=self.question1, country=self.country,
                                                               status=Answer.SUBMITTED_STATUS, response=23)
        self.question1_answer_2 = NumericalAnswer.objects.create(question=self.question1, country=self.country,
                                                                 status=Answer.SUBMITTED_STATUS, response=1)

    def test_questionnaire_unicode(self):
        self.assertEqual(str(self.questionnaire), "JRF 2013 Core English".encode('utf8'))

    def test_questionnaire_fields(self):
        fields = [str(item.attname) for item in Questionnaire._meta.fields]
        self.assertEqual(9, len(fields))
        for field in ['id', 'created', 'modified', 'name', 'description', 'year', 'status', 'region_id', 'parent_id']:
            self.assertIn(field, fields)

    def test_questionnaire_store(self):
        self.failUnless(self.questionnaire.id)
        self.assertEqual("JRF 2013 Core English", self.questionnaire.name)
        self.assertEqual(self.questionnaire.status, Questionnaire.DRAFT)

    def test_questionnaire_can_find_its_subsection(self):
        questionnaire_sub_sections = self.questionnaire.sub_sections()
        self.assertEqual(2, len(questionnaire_sub_sections))
        self.assertIn(self.sub_section_1, questionnaire_sub_sections)
        self.assertIn(self.sub_section_2, questionnaire_sub_sections)

    def test_questionnaire_can_get_all_its_questions(self):
        all_questions = self.questionnaire.get_all_questions()
        self.assertEqual(1, len(all_questions))
        self.assertIn(self.question1, all_questions)

    def test_questionnaire_knows_all_question_groups(self):
        question1 = Question.objects.create(text='B. Number of cases tested', UID='C00033', answer_type='Number')
        another_group = QuestionGroup.objects.create(subsection=self.sub_section_2, name="Laboratory Investigation2")
        another_group.question.add(question1)

        self.assertEqual(2, len(self.questionnaire.all_groups()))
        self.assertIn(self.sub_group, self.questionnaire.all_groups())
        self.assertIn(another_group, self.questionnaire.all_groups())

    def test_questionnaire_does_not_know_groups_that_do__not_belong_to_it(self):
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English")
        section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                           order=1, questionnaire=questionnaire, name="Reported Cases")
        sub_section_1 = SubSection.objects.create(title="Reported cases for the year 2013", order=1, section=section_1)
        another_group = QuestionGroup.objects.create(subsection=sub_section_1, name="Laboratory Investigation2")

        self.assertEqual(1, len(self.questionnaire.all_groups()))
        self.assertIn(self.sub_group, self.questionnaire.all_groups())
        self.assertNotIn(another_group, self.questionnaire.all_groups())

    def test_questionnaire_knows_its_finalized(self):
        self.assertFalse(self.questionnaire.is_finalized())

        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.FINALIZED)
        self.assertTrue(questionnaire.is_finalized())

    def test_questionnaire_knows_its_archived(self):
        self.assertFalse(self.questionnaire.is_archived())

        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.ARCHIVED)
        self.assertTrue(questionnaire.is_archived())

    def test_questionnaire_knows_its_published(self):
        self.assertFalse(self.questionnaire.is_published())

        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.PUBLISHED)
        self.assertTrue(questionnaire.is_published())

    def test_questionnaire_knows_it_has_more_than_one_section(self):
        self.assertFalse(self.questionnaire.has_more_than_one_section())

        section_2 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                           order=2,
                                           questionnaire=self.questionnaire, name="Reported Cases")

        self.assertTrue(self.questionnaire.has_more_than_one_section())

    def test_questionnaire_knows_its_sections_in_order(self):
        section_2 = Section.objects.create(title="section2", order=2, questionnaire=self.questionnaire, name="sec2")
        ordered_sections = self.questionnaire.ordered_sections()
        self.assertEqual(2, ordered_sections.count())
        self.assertEqual(self.section_1, ordered_sections[0])
        self.assertEqual(section_2, ordered_sections[1])

    def test_questionnaire_knows_its_newest_un_submited_answer_version(self):
        NumericalAnswer.objects.create(question=self.question1, country=self.country,
                                       status=Answer.DRAFT_STATUS, response=23, version=2,
                                       questionnaire=self.questionnaire)
        self.assertEqual(2, self.questionnaire.current_answer_version())

    def test_questionnaire_is_archivable_only_if_finalized(self):
        questionnaire = QuestionnaireFactory(status=Questionnaire.FINALIZED)
        self.assertTrue(questionnaire.is_archivable())

        questionnaire = QuestionnaireFactory(status=Questionnaire.DRAFT)
        self.assertFalse(questionnaire.is_archivable())

        questionnaire = QuestionnaireFactory(status=Questionnaire.PUBLISHED)
        self.assertTrue(questionnaire.is_archivable())

    def test_questionnaire_is_archivable_if_published_and_no_answers_submitted_in_region(self):
        questionnaire = QuestionnaireFactory(status=Questionnaire.PUBLISHED)
        self.assertTrue(questionnaire.is_archivable())

        regional_questionaire = QuestionnaireFactory(status=Questionnaire.PUBLISHED, parent=questionnaire)
        NumericalAnswerFactory(questionnaire=regional_questionaire)

        self.assertFalse(questionnaire.is_archivable())

    def test_archiving_questionnaire_changes_its_status(self):
        questionnaire = QuestionnaireFactory(status=Questionnaire.FINALIZED)
        questionnaire.archive()

        self.assertEqual(Questionnaire.ARCHIVED, questionnaire.status)

    def test_questionnaire_is_deletable(self):
        questionnaire = QuestionnaireFactory(status=Questionnaire.FINALIZED)
        self.assertTrue(questionnaire.is_deletable())

        questionnaire = QuestionnaireFactory(status=Questionnaire.DRAFT)
        self.assertTrue(questionnaire.is_deletable())

        questionnaire = QuestionnaireFactory(status=Questionnaire.PUBLISHED)
        self.assertTrue(questionnaire.is_deletable())

        questionnaire = QuestionnaireFactory(status=Questionnaire.ARCHIVED)
        self.assertTrue(questionnaire.is_deletable())

    def test_questionnaire_is_deletable_if_published_and_no_answers_submitted_in_region(self):
        questionnaire = QuestionnaireFactory(status=Questionnaire.PUBLISHED)
        regional_questionaire = QuestionnaireFactory(status=Questionnaire.PUBLISHED, parent=questionnaire)
        NumericalAnswerFactory(questionnaire=regional_questionaire)

        self.assertFalse(questionnaire.is_deletable())