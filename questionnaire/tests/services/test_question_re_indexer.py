from mock import patch
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionOption, QuestionGroup, \
    QuestionGroupOrder
from questionnaire.services.question_re_indexer import QuestionReIndexer, OrderBasedReIndexer, GridReorderer
from questionnaire.tests.base_test import BaseTest
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.question_group_factory import QuestionGroupFactory
from questionnaire.tests.factories.questionnaire_factory import QuestionnaireFactory
from questionnaire.tests.factories.section_factory import SectionFactory
from questionnaire.tests.factories.sub_section_factory import SubSectionFactory


class TestQuestionReIndexer(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.PUBLISHED)

        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                                order=1,
                                                questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                     section=self.section_1)

        self.question1 = Question.objects.create(text='Disease', UID='C00001', answer_type='MultiChoice')
        self.question2 = Question.objects.create(text='B. Number of cases tested',
                                                 instructions="Enter the total number of cases for which specimens were collected, and tested in laboratory",
                                                 UID='C00003', answer_type='Number')

        self.question3 = Question.objects.create(text='C. Number of cases positive',
                                                 instructions="Include only those cases found positive for the infectious agent.",
                                                 UID='C00004', answer_type='Number')

        self.option1 = QuestionOption.objects.create(text='tusker lager', question=self.question1)
        self.option2 = QuestionOption.objects.create(text='tusker lager1', question=self.question1)
        self.option3 = QuestionOption.objects.create(text='tusker lager2', question=self.question1)

        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1)
        self.question_group.question.add(self.question1, self.question3, self.question2)

        self.order1 = QuestionGroupOrder.objects.create(question_group=self.question_group, question=self.question1,
                                                        order=1)
        self.order2 = QuestionGroupOrder.objects.create(question_group=self.question_group, question=self.question2,
                                                        order=2)
        self.order3 = QuestionGroupOrder.objects.create(question_group=self.question_group, question=self.question3,
                                                        order=3)
        self.data = {'Number-0-response-order': ["%d,%d, 0" % (self.question_group.id, self.order3.id)],
                     'Text-1-response-order': ["%d,%d, 1" % (self.question_group.id, self.order2.id)],
                     'Text-0-response-order': ["%d,%d, 2" % (self.question_group.id, self.order1.id)]}

    def test_reorder_questions(self):
        dirty_data_query_dict = self.cast_to_queryDict(self.data)
        QuestionReIndexer(dirty_data_query_dict).reorder_questions()
        updated_orders = self.question_group.question_orders()
        self.assertEqual(3, updated_orders.count())
        self.assertEqual(self.order1, updated_orders.get(order=3))
        self.assertEqual(self.order2, updated_orders.get(order=2))
        self.assertEqual(self.order3, updated_orders.get(order=1))

    def test_get_old_orders(self):
        expected = {self.order1: ["%d" % self.question_group.id, "%s" % self.order1.id, " %s" % 2],
                    self.order2: ["%d" % self.question_group.id, "%s" % self.order2.id, " %s" % 1],
                    self.order3: ["%d" % self.question_group.id, "%s" % self.order3.id, " %s" % 0]}
        dirty_data_query_dict = self.cast_to_queryDict(self.data)
        question_re_indexer = QuestionReIndexer(dirty_data_query_dict)
        self.assertEqual(expected, question_re_indexer.get_old_orders())

    def test_clean_posted_data(self):
        dirty_data = {u'Text-3-response-order': [u'', u'179,5'], u'Text-6-response-order': [u'', u'182,6'],
                      u'Text-5-response-order': [u'', u'181,4'],
                      u'Number-0-response-order': [u'', u'183,7'], u'Text-0-response-order': [u'', u'176,0'],
                      u'Text-2-response-order': [u'', u'178,3'], u'Text-4-response-order': [u'', u'180,2'],
                      u'csrfmiddlewaretoken': [u'f5YpJke56IFgXPxEq2H3jhrWMSDGHMnn'],
                      u'Text-1-response-order': [u'', u'177,1']}

        dirty_data_query_dict = self.cast_to_queryDict(dirty_data)
        cleaned_data = {u'Text-3-response-order': [u'179', u'5'], u'Text-6-response-order': [u'182', u'6'],
                        u'Text-5-response-order': [u'181', u'4'],
                        u'Number-0-response-order': [u'183', u'7'], u'Text-0-response-order': [u'176', u'0'],
                        u'Text-2-response-order': [u'178', u'3'], u'Text-4-response-order': [u'180', u'2'],
                        u'Text-1-response-order': [u'177', u'1']}

        question_re_indexer = QuestionReIndexer(dirty_data_query_dict)
        self.assertEqual(cleaned_data, question_re_indexer.clean_data_posted())

    def test_is_allowed(self):
        question_re_indexer = QuestionReIndexer({})
        self.assertTrue(question_re_indexer.is_allowed("Text-3-response-order"))
        self.assertFalse(question_re_indexer.is_allowed("Text-3-response-haha"))
        self.assertFalse(question_re_indexer.is_allowed("Beer-3-response-hehe"))
        self.assertFalse(question_re_indexer.is_allowed("csrfmiddlewaretoken"))

    def test_clean_values(self):
        dirty_values = u'179,5'
        question_re_indexer = QuestionReIndexer({})
        self.assertEqual([u'179', u'5'], question_re_indexer.clean_values(dirty_values))

    @patch("questionnaire.models.QuestionGroup.delete_empty_groups")
    @patch("questionnaire.utils.model_utils.reindex_orders_in")
    def test_reorder_questions_cross_question_groups(self, mock_reindex_orders_in,mock_delete_empty_groups):
        question4 = Question.objects.create(text='new group question 1', UID='C00057', answer_type='Number')
        question5 = Question.objects.create(text='new group question 2', UID='C00043', answer_type='Number')

        question_group1 = QuestionGroup.objects.create(subsection=self.sub_section, order=2)
        question_group1.question.add(question4, question5)

        order1 = QuestionGroupOrder.objects.create(question_group=question_group1, question=question4, order=1)
        order2 = QuestionGroupOrder.objects.create(question_group=question_group1, question=question5, order=2)

        cross_data = {'Number-0-response-order': ["%d,%d, 0" % (self.question_group.id, self.order3.id)],
                      'Text-1-response-order': ["%d,%d, 1" % (self.question_group.id, self.order2.id)],
                      'Text-2-response-order': ["%d,%d, 2" % (self.question_group.id, order1.id)],
                      'Text-0-response-order': ["%d,%d, 0" % (question_group1.id, self.order1.id)],
                      'Text-3-response-order': ["%d,%d, 1" % (question_group1.id, order2.id)]}

        dirty_data_query_dict = self.cast_to_queryDict(cross_data)
        QuestionReIndexer(dirty_data_query_dict).reorder_questions()
        updated_orders = self.question_group.question_orders()
        self.assertEqual(3, updated_orders.count())
        self.assertEqual(order1, updated_orders.get(order=3))
        self.assertEqual(self.order2, updated_orders.get(order=2))
        self.assertEqual(self.order3, updated_orders.get(order=1))

        question4_order = QuestionGroupOrder.objects.get(question=question4)
        self.assertEqual(Question.objects.get(UID='C00057'), question4_order.question)
        self.assertNotIn(order1.question, question_group1.ordered_questions())
        self.assertIn(order1.question, self.question_group.ordered_questions())

        updated_orders = question_group1.question_orders()
        self.assertEqual(2, updated_orders.count())
        self.assertEqual(self.order1, updated_orders.get(order=1))
        self.assertEqual(order2, updated_orders.get(order=2))
        self.assertIn(self.question1, question_group1.ordered_questions())
        self.assertNotIn(self.question1, self.question_group.ordered_questions())

        mock_delete_empty_groups.assert_called_with(order1.question_group.subsection)
        mock_reindex_orders_in.assert_called()


class SubsectionReIndexerServiceTest(BaseTest):

    def setUp(self):
        self.section = SectionFactory()
        self.subsection1 = SubSectionFactory(order=1, section=self.section)
        self.subsection2 = SubSectionFactory(order=2, section=self.section)
        self.subsection3 = SubSectionFactory(order=3, section=self.section)
        self.subsection4 = SubSectionFactory(order=4, section=self.section)
        self.subsection5 = SubSectionFactory(order=5, section=self.section)
        self.subsection6 = SubSectionFactory(order=6, section=self.section)

    def test_swap_for_the_first_two_subsections(self):
        subsection_indexer = OrderBasedReIndexer(self.subsection1, 2, section=self.section)
        subsection_indexer.reorder()
        re_ordered = SubSection.objects.filter(section=self.section).order_by('order')
        subsections_in_new_orders = [self.subsection2, self.subsection1, self.subsection3, self.subsection4, self.subsection5, self.subsection6]
        self.assertEqual(list(re_ordered), subsections_in_new_orders)

    def test_move_sub_section_displaces_other_subsections_forwards(self):
        subsection_indexer = OrderBasedReIndexer(self.subsection3, 5, section=self.section)
        subsection_indexer.reorder()
        subsections_in_new_orders = [self.subsection1, self.subsection2, self.subsection4, self.subsection5, self.subsection3, self.subsection6]
        re_ordered = SubSection.objects.filter(section=self.section).order_by('order')
        self.assertEqual(list(re_ordered), subsections_in_new_orders)

    def test_move_sub_section_displaces_other_subsection_backwards(self):
        subsection_indexer = OrderBasedReIndexer(self.subsection6, 2, section=self.section)
        subsection_indexer.reorder()
        re_ordered = SubSection.objects.filter(section=self.section).order_by('order')
        subsections_in_new_orders = [self.subsection1, self.subsection6, self.subsection2, self.subsection3, self.subsection4, self.subsection5]

        self.assertEqual(list(re_ordered), subsections_in_new_orders)

    def test_move_sub_section_to_position_1_displaces_other_subsection_backwards(self):
        subsection_indexer = OrderBasedReIndexer(self.subsection6, 1, section=self.section)
        subsection_indexer.reorder()
        subsections_in_new_orders = [self.subsection6, self.subsection1, self.subsection2, self.subsection3, self.subsection4, self.subsection5]
        re_ordered = SubSection.objects.filter(section=self.section).order_by('order')

        self.assertEqual(list(re_ordered), subsections_in_new_orders)

    def test_moved_subsection_order_is_persisted(self):
        subsection_indexer = OrderBasedReIndexer(self.subsection1, 3, section=self.section)
        subsection_indexer.reorder()
        subsection_order = SubSection.objects.get(id=self.subsection1.id)
        self.assertEqual(3, subsection_order.order)


class SectionReIndexerTest(BaseTest):
    def setUp(self):
        self.questionnaire = QuestionnaireFactory()
        self.section1 = SectionFactory(order=1, questionnaire=self.questionnaire, name='section 1')
        self.section2 = SectionFactory(order=2, questionnaire=self.questionnaire, name='section 2')
        self.section3 = SectionFactory(order=3, questionnaire=self.questionnaire, name='section 3')
        self.section4 = SectionFactory(order=4, questionnaire=self.questionnaire, name='section 4')
        self.section5 = SectionFactory(order=5, questionnaire=self.questionnaire, name='section 5')
        self.section6 = SectionFactory(order=6, questionnaire=self.questionnaire, name='section 6')
        self.section7 = SectionFactory(order=1)

    def test_move_section_displaces_other_sections_forwards(self):
        section_indexer = OrderBasedReIndexer(self.section3, 5, questionnaire=self.questionnaire)
        section_indexer.reorder()
        sections_in_new_orders = [self.section1, self.section2, self.section4, self.section5, self.section3, self.section6]
        re_ordered = Section.objects.filter(questionnaire=self.questionnaire).order_by('order')
        self.assertEqual(list(re_ordered), sections_in_new_orders)

    def test_move_section_displaces_other_sections_backwards(self):
        section_indexer = OrderBasedReIndexer(self.section5, 1, questionnaire=self.questionnaire)
        section_indexer.reorder()
        sections_in_new_orders = [self.section5, self.section1, self.section2, self.section3, self.section4, self.section6]
        re_ordered = Section.objects.filter(questionnaire=self.questionnaire).order_by('order')
        self.assertEqual(list(re_ordered), sections_in_new_orders)

    def test_move_section_from_first_position_to_second_displaces_other_sections_up_words(self):
        section_indexer = OrderBasedReIndexer(self.section1, 2, questionnaire=self.questionnaire)
        section_indexer.reorder()
        sections_in_new_orders = [self.section2, self.section1, self.section3, self.section4, self.section5, self.section6]
        re_ordered = Section.objects.filter(questionnaire=self.questionnaire).order_by('order')
        self.assertEqual(list(re_ordered), sections_in_new_orders)

    def test_reorders_sections_with_newest_duplicate_section_comming_first(self):
        self.section1.order = 2
        section_indexer = OrderBasedReIndexer(self.section1, 2, questionnaire=self.questionnaire)
        section_indexer.reorder()
        sections_in_new_orders = [self.section2, self.section1, self.section3, self.section4, self.section5, self.section6]
        re_ordered = Section.objects.filter(questionnaire=self.questionnaire).order_by('order')
        self.assertEqual(list(re_ordered), sections_in_new_orders)


class GridReordererTest(BaseTest):
    def setUp(self):
        self.subsection = SubSectionFactory()
        self.question_group1 = QuestionGroupFactory(subsection=self.subsection, order=1, grid=True)
        self.question_group2 = QuestionGroupFactory(subsection=self.subsection, order=2, grid=True)
        self.question_group3 = QuestionGroupFactory(subsection=self.subsection, order=3)
        self.question_group4 = QuestionGroupFactory(subsection=self.subsection, order=4, grid=True)

        self.question_group1.question.add(QuestionFactory(text="group 1"))
        self.question_group2.question.add(QuestionFactory(text="group 2"))
        self.question = QuestionFactory(text="group 3")
        self.question_group3.question.add(self.question)
        self.question_group4.question.add(QuestionFactory(text= "group 4"))
        QuestionGroupOrder.objects.create(question=self.question, question_group=self.question_group3, order=1)

    def test_reorder_group_with_sub_section(self):
        GridReorderer(self.question_group2, "up").reorder_group_in_sub_section()

        question_group1 = QuestionGroup.objects.get(id=self.question_group1.id)
        self.assertEqual(self.question_group2.order, 1)
        self.assertEqual(question_group1.order, 2)


    def test_reorder_group_when_group_order_is_one_nothing_happens(self):
        GridReorderer(self.question_group1, "up").reorder_group_in_sub_section()

        self.assertEqual(self.question_group1.order, 1)

    def test_reorder_group_with_sub_sections_when_grid_is_moving_down(self):
        GridReorderer(self.question_group1, "down").reorder_group_in_sub_section()

        question_group2 = QuestionGroup.objects.get(id=self.question_group2.id)
        self.assertEqual(question_group2.order, 1)
        self.assertEqual(self.question_group1.order, 2)

    def test_reorder_group_does_nothing_when_the_grid_is_at_the_bottom(self):
        GridReorderer(self.question_group4, "down").reorder_group_in_sub_section()

        self.assertEqual(self.question_group4.order, 4)

    def test_reorder_group_when_group_above_is_not_a_grid_and_has_one_question(self):
        self.assertEqual(QuestionGroup.objects.all().count(), 4)
        GridReorderer(self.question_group4, "up").reorder_group_in_sub_section()
        question_group3 = QuestionGroup.objects.get(id=self.question_group3.id)
        self.assertEqual(self.question_group4.order, 3)
        self.assertEqual(question_group3.order, 4)
        self.assertEqual(len(QuestionGroup.objects.all()), 4)

    def test_reorder_group_when_group_below_is_not_a_grid_and_has_one_question(self):
        self.assertEqual(QuestionGroup.objects.all().count(), 4)
        GridReorderer(self.question_group2, "down").reorder_group_in_sub_section()
        question_group3 = QuestionGroup.objects.get(id=self.question_group3.id)
        self.assertEqual(self.question_group2.order, 3)
        self.assertEqual(question_group3.order, 2)
        self.assertEqual(len(QuestionGroup.objects.all()), 4)

    def test_reorder_group_when_group_above_is_not_a_grid_and_has_two_questions(self):
        second_question = QuestionFactory(text='question to be moved down')
        self.question_group3.question.add(second_question)
        QuestionGroupOrder.objects.create(question=second_question, question_group=self.question_group3, order=2)
        self.assertEqual(QuestionGroup.objects.all().count(), 4)

        GridReorderer(self.question_group4, "up").reorder_group_in_sub_section()

        self.assertEqual(self.question_group3.order, 3)
        self.assertEqual(self.question_group4.order, 4)
        self.assertEqual(len(self.question_group3.and_sub_group_questions()), 1)
        self.assertEqual(self.question_group3.and_sub_group_questions()[0], self.question)
        self.assertEqual(len(QuestionGroup.objects.all()), 5)
        new_group = self.subsection.question_group.get(order=self.question_group4.order + 1)
        self.assertEqual(len(new_group.and_sub_group_questions()), 1)
        self.assertEqual(new_group.and_sub_group_questions()[0], second_question)

    def test_reorder_group_when_group_below_is_not_a_grid_and_two_or_more_questions(self):
        second_question = QuestionFactory(text='second question')
        self.question_group3.question.add(second_question)
        QuestionGroupOrder.objects.create(question=second_question, question_group=self.question_group3, order=2)

        self.assertEqual(QuestionGroup.objects.all().count(), 4)

        GridReorderer(self.question_group2, "down").reorder_group_in_sub_section()

        question_group2 = QuestionGroup.objects.get(id=self.question_group2.id)
        question_group3 = QuestionGroup.objects.get(id=self.question_group3.id)
        question_group4 = QuestionGroup.objects.get(id=self.question_group4.id)
        self.assertEqual(question_group2.order, 3)
        self.assertEqual(question_group3.order, 4)
        self.assertEqual(question_group4.order, 5)
        self.assertEqual(len(question_group3.ordered_questions()), 1)
        self.assertEqual(question_group3.ordered_questions()[0], second_question)
        self.assertEqual(question_group3.orders.all()[0].order, 1)
        self.assertEqual(question_group3.orders.all()[0].question, second_question)
        self.assertEqual(QuestionGroup.objects.all().count(), 5)
        self.assertEqual(len(QuestionGroup.objects.all()), 5)
        new_group = self.subsection.question_group.get(order=question_group2.order - 1)
        self.assertEqual(len(new_group.and_sub_group_questions()), 1)
        self.assertEqual(new_group.and_sub_group_questions()[0], self.question)
        self.assertEqual(new_group.orders.all()[0].order, 1)

    def test_reorder_group_when_group_above_is_not_a_grid_and_two_or_more_questions(self):
        second_question = QuestionFactory(text='second question')
        self.question_group3.question.add(second_question)
        QuestionGroupOrder.objects.create(question=second_question, question_group=self.question_group3, order=2)

        self.assertEqual(QuestionGroup.objects.all().count(), 4)

        GridReorderer(self.question_group4, "up").reorder_group_in_sub_section()

        question_group2 = QuestionGroup.objects.get(id=self.question_group2.id)
        question_group3 = QuestionGroup.objects.get(id=self.question_group3.id)
        question_group4 = QuestionGroup.objects.get(id=self.question_group4.id)
        self.assertEqual(question_group2.order, 2)
        self.assertEqual(question_group3.order, 3)
        self.assertEqual(question_group4.order, 4)
        self.assertEqual(len(question_group3.ordered_questions()), 1)
        self.assertEqual(question_group3.ordered_questions()[0], self.question)
        self.assertEqual(question_group3.orders.all()[0].order, 1)
        self.assertEqual(question_group3.orders.all()[0].question, self.question)
        self.assertEqual(QuestionGroup.objects.all().count(), 5)
        self.assertEqual(len(QuestionGroup.objects.all()), 5)
        new_group = self.subsection.question_group.get(order=question_group4.order + 1)
        self.assertEqual(len(new_group.and_sub_group_questions()), 1)
        self.assertEqual(new_group.and_sub_group_questions()[0], second_question)
        self.assertEqual(new_group.orders.all()[0].order, 1)

    def test_reorder_group_when_group_above_is_not_a_grid_and_two_or_more_questions_with_a_subgroups(self):
        second_question = QuestionFactory()
        self.question_group3.question.add(second_question)
        QuestionGroupOrder.objects.create(question=second_question, question_group=self.question_group3, order=2)

        sub_group = QuestionGroupFactory(parent=self.question_group3)
        sub_group_question = QuestionFactory(text='Subgroup question')
        sub_group.question.add(sub_group_question)
        QuestionGroupOrder.objects.create(question=sub_group_question, question_group=self.question_group3, order=3)

        self.assertEqual(QuestionGroup.objects.all().count(), 5)

        GridReorderer(self.question_group4, "up").reorder_group_in_sub_section()

        question_group2 = QuestionGroup.objects.get(id=self.question_group2.id)
        question_group3 = QuestionGroup.objects.get(id=self.question_group3.id)
        question_group4 = QuestionGroup.objects.get(id=self.question_group4.id)
        self.assertEqual(question_group2.order, 2)
        self.assertEqual(question_group3.order, 3)
        self.assertEqual(question_group4.order, 4)
        self.assertEqual(len(question_group3.ordered_questions()), 2)
        self.assertEqual(question_group3.ordered_questions()[0], self.question)
        self.assertEqual(question_group3.question_orders()[0].order, 1)
        self.assertEqual(len(question_group3.and_sub_group_questions()), 2)
        self.assertEqual(QuestionGroup.objects.filter(subsection=self.subsection).count(), 5)

        new_group = self.subsection.question_group.get(order=question_group4.order + 1)
        self.assertEqual(len(new_group.ordered_questions()), 1)
        self.assertEqual(new_group.ordered_questions()[0], sub_group_question)
        self.assertEqual(new_group.orders.all()[0].order, 1)
        all_groups = QuestionGroup.objects.filter(subsection=self.subsection)
        self.assertEqual(len(filter(lambda group: len(group.and_sub_group_questions()) == 0, all_groups)), 0)