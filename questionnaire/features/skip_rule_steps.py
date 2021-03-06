from lettuce import step, world
import time
from questionnaire.features.pages.skip_rule_modal import SkipRuleModalPage
from questionnaire.models.skip_rule import SkipQuestion, SkipSubsection
from questionnaire.models import QuestionGroupOrder, Questionnaire, Question, QuestionGroup, QuestionOption, Section, \
    SubSection
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.question_group_factory import QuestionGroupFactory
from questionnaire.tests.factories.question_option_factory import QuestionOptionFactory
from questionnaire.tests.factories.sub_section_factory import SubSectionFactory
from questionnaire.utils.answer_type import AnswerTypes


@step(u'Then I should see an option to delete skip rules')
def then_i_should_see_an_option_to_delete_skip_rules(step):
    world.page.is_text_present("Delete")


@step(u'When I have selected delete')
def when_i_have_selected_delete(step):
    skip_question = SkipQuestion.objects.all()[0]
    world.page.click_by_id("delete-rule-%d" % skip_question.id)


@step(u'Then I should see the rule disappear and a message that the skip rule was successfully deleted')
def then_i_should_see_the_rule_disappear_and_a_message_that_the_skip_rule_was_successfully_deleted(step):
    world.page.is_text_present('Rule successfully deleted')


@step(u'And I click to add a skip rule')
def and_i_click_to_add_a_skip_rule(step):
    world.page.click_by_id('id-create-skip-rule-%s' % world.sub_section.id)
    world.skip_rule_page = SkipRuleModalPage(world.browser)


@step(u'I choose to see existing skip rules')
def and_i_choose_to_see_existing_skip_rules(step):
    world.skip_rule_page.view_existing_rules()


@step(u'Then I should see \'([^\']*)\' existing skip rules')
def then_i_should_see_group1_existing_skip_rules(step, number_of_rules):
    time.sleep(2)
    actual_number = world.skip_rule_page.number_of_skip_rules()
    time.sleep(2)
    assert (actual_number == int(number_of_rules)), 'Expecting %s number of rules, got %s number of rules' % (
        int(number_of_rules), actual_number)


@step(u'When I create a new question skip rule')
def when_i_create_a_new_skip_rule(step):
    world.skip_rule_page.create_new_qn_rule()


@step(u'Then I should see options to add skip rules for skipping \'([^\']*)\'')
def then_i_should_see_options_to_add_skip_rules_for_skipping_group1(step, element_to_skip):
    world.skip_rule_page.skip_tab_is_present_for(element_to_skip)


@step(u'When I select to add skip rules for skipping questions')
def when_i_select_to_add_skip_rules_for_skipping_questions(step):
    world.skip_rule_page.view_create_new_qn_rules()


@step(u'When I select to add skip rules for skipping subsections')
def when_i_select_to_add_skip_rules_for_skipping_subsections(step):
    world.skip_rule_page.view_create_new_sub_rules()


@step(u'And I have skip rules applied to a question')
def and_i_have_skip_rules_applied_to_a_question(step):
    SkipQuestion.objects.create(skip_question=world.skip_question01, response=world.response,
                                root_question=world.root_question, subsection=world.sub_section)


@step(u'And I have skip rules applied to a subsection')
def and_i_have_skip_rules_applied_to_a_subsection(step):
    SkipSubsection.objects.create(skip_subsection=world.sub_section_2, response=world.response,
                                  root_question=world.root_question, subsection=world.sub_section)


@step(u'And I have questions and responses in the correct section')
def and_i_have_questions_and_responses_in_the_correct_section(step):
    world.root_question = QuestionFactory()
    world.skip_question01 = QuestionFactory(text="Skip Question 01")
    world.skip_question02 = QuestionFactory(text="Skip Question 02")

    world.response = QuestionOptionFactory(question=world.root_question)
    question_group = QuestionGroupFactory(subsection=world.sub_section, order=1)
    QuestionGroupOrder.objects.create(question=world.root_question, order=1, question_group=question_group)
    QuestionGroupOrder.objects.create(question=world.skip_question01, order=2, question_group=question_group)
    QuestionGroupOrder.objects.create(question=world.skip_question02, order=3, question_group=question_group)

    world.root_question.question_group.add(question_group)
    world.skip_question01.question_group.add(question_group)
    world.skip_question02.question_group.add(question_group)


@step(u'I should see the questions in that subsection listed')
def i_should_see_the_questions_in_that_subsection_listed(step):
    world.browser.find_by_name('skip_question')[0].click()
    world.page.is_text_present(world.skip_question01.text)


@step(u'I should see the subsections in that section listed')
def i_should_see_the_subsections_in_that_section_listed(step):
    world.browser.find_by_name('skip_subsection')[0].click()
    world.page.is_text_present('Subsection Title Sample')


@step(u'And the questionnaire has been published to the data submitter')
def and_the_questionnaire_has_been_published_to_the_data_submitter(step):
    world.questionnaire.region = world.region
    world.questionnaire.status = Questionnaire.PUBLISHED
    world.questionnaire.save()


@step(u'Then I should see the all the questions and subsections in that section')
def then_i_should_see_the_all_the_questions_in_that_section_and_subsection(step):
    world.page.is_text_present(world.skip_question01.text)
    world.page.is_text_present(world.root_question.text)
    world.page.is_text_present(world.sub_section_2.title)


@step(u'When I select a response that skips a question')
def when_i_select_a_response_that_skips_a_question(step):
    world.page.choose('MultiChoice-0-response', '1')


@step(u'Then that question should no longer be displayed')
def then_that_question_should_no_longer_be_displayed(step):
    world.page.is_text_present(world.skip_question01.text, status=False)


@step(u'When I create a new subsection skip rule')
def when_i_create_a_new_subsection_skip_rule(step):
    world.skip_rule_page.create_new_sub_rule(world.root_question, world.sub_section_2)


@step(u'And I have a hybrid group with multichoice question and other questions')
def and_i_have_a_hybrid_group_with_multichoice_question_and_other_questions(step):
    world.root_question = QuestionFactory(is_primary=True)
    world.question_to_skip = QuestionFactory(answer_type="Number", text="Text question to be skipped")

    world.response = QuestionOptionFactory(question=world.root_question)
    world.subsection = SubSectionFactory(section=world.section_1)
    world.question_group = QuestionGroupFactory(grid=True, hybrid=True, subsection=world.subsection, order=1)

    world.root_question.question_group.add(world.question_group)
    world.question_to_skip.question_group.add(world.question_group)

    QuestionGroupOrder.objects.create(question=world.root_question, question_group=world.question_group, order=1)
    QuestionGroupOrder.objects.create(question=world.question_to_skip, question_group=world.question_group, order=2)


@step(u'And I click to add a grid skip rule')
def and_i_click_to_add_a_grid_skip_rule(step):
    world.page.click_by_id('grid-question-%s' % world.question_group.id)


@step(u'And I choose to see existing grid skip rules')
def and_i_choose_to_see_existing_grid_skip_rules(step):
    world.skip_rule_page = SkipRuleModalPage(world.browser)
    world.skip_rule_page.view_existing_rules()


@step(u'When I click create a new hybrid grid question skip rule')
def when_i_click_create_a_new_hybrid_grid_question_skip_rule(step):
    world.page.click_by_id('selectNewRuleTab')


@step(u'And I fill in the grid rule form')
def and_i_fill_in_the_grid_rule_form(step):
    world.page.select('root_question', world.root_question.id)
    world.page.browser.find_by_id('id-question-option-%s' % world.response.id).check()
    world.page.select('skip_question', world.question_to_skip.id)


@step(u'And I click save rule')
def and_i_click_save_rule(step):
    world.page.click_by_id('save-skip-rule-button')


@step(u'Then I should see \'([^\']*)\' existing grid skip rules')
def then_i_should_see_group1_existing_grid_skip_rules(step, count):
    actual_number = world.skip_rule_page.number_of_skip_rules()
    assert (actual_number == int(count)), 'Expecting %s number of rules, got %s number of rules' % (
        int(count), actual_number)


@step(u'And I have core and regional questions assigned to the questionnaire')
def and_i_have_core_and_regional_questions_assigned_to_the_questionnaire(step):
    world.core_qn01 = Question.objects.create(text='Core Question 01', export_label='Core Qn 01', UID='01', answer_type=AnswerTypes.MULTI_CHOICE)
    QuestionOption.objects.create(text='Option 1 of Core Question', question=world.core_qn01)
    QuestionOption.objects.create(text='Option 2 of Core Question', question=world.core_qn01)

    world.regional_qn02 = Question.objects.create(text='Regional Question 02', export_label='Regional Qn 02', UID='02', answer_type='Text', region=world.region)
    world.regional_qn03 = Question.objects.create(text='Regional Question 03', export_label='Regional Qn 03', UID='03', answer_type='Text', region=world.region)

    parent = QuestionGroup.objects.create(subsection=world.sub_section, order=1)
    parent.question.add(world.core_qn01, world.regional_qn02, world.regional_qn03)

    QuestionGroupOrder.objects.create(question=world.core_qn01, question_group=parent, order=1)
    QuestionGroupOrder.objects.create(question=world.regional_qn02, question_group=parent, order=2)
    QuestionGroupOrder.objects.create(question=world.regional_qn03, question_group=parent, order=3)


@step(u'Then I should see options to add skip rules')
def then_i_should_see_options_to_add_skip_rules(step):
    world.page.is_text_present('Add Skip Rule')
    world.page.is_element_present_by_id('id-create-skip-rule-%s' % world.sub_section.id)

@step(u'When I create a new regional subsection skip rule')
def when_i_create_a_new_regional_subsection_skip_rule(step):
    world.skip_rule_page.create_new_sub_rule(world.core_qn01, world.regional_subsection)

@step(u'When I select the option to add skip rules to a subsection')
def when_i_select_the_option_to_add_skip_rules_to_a_subsection(step):
    world.page.click_by_id('id-create-skip-rule-%s' % world.sub_section.id)


@step(u'And I view existing skip rules')
def and_i_view_existing_skip_rules(step):
    world.skip_rule_page = SkipRuleModalPage(world.browser)
    world.skip_rule_page.view_existing_rules()

@step(u'And there is questionnaire for my region')
def and_there_is_questionnaire_for_my_region(step):
    world.questionnaire = Questionnaire.objects.create(name="JRF Bolivia version", description="some more description",
                                                       year=2013, status=Questionnaire.DRAFT, region=world.region)
    world.section1 = Section.objects.create(order=0, title="section 1",
                                            questionnaire=world.questionnaire, name="section 1", region=world.region)
    world.section_1 = Section.objects.create(order=4, title="section_1",
                                            questionnaire=world.questionnaire, name="section_1")
    world.section2 = Section.objects.create(order=1, title="Another title",
                                            description="This is just another one of them",
                                            questionnaire=world.questionnaire, name="Reported Cases",
                                            region=world.region)
    world.section3 = Section.objects.create(order=2, title="Section 3 Title",
                                            description="Section 3 description",
                                            questionnaire=world.questionnaire, name="Section 3", region=world.region)
    world.section4 = Section.objects.create(order=3, title="Core Section",
                                            description="Section 3 description",
                                            questionnaire=world.questionnaire, name="Section 3")
    world.sub_section = SubSection.objects.create(title="regional subs", order=1, section=world.section1, region=world.region)
    world.regional_subsection = SubSection.objects.create(title="Other regional subsection", order=2, section=world.section1, region=world.region)
    world.sub_section_1 = SubSection.objects.create(title="other R subs", order=1, section=world.section_1, region=world.region)
    world.core_sub_section = SubSection.objects.create(title="core subs", order=2, section=world.section_1)


@step(u'And I have skip rules applied to another question')
def and_i_have_skip_rules_applied_to_another_question(step):
    SkipQuestion.objects.create(skip_question=world.skip_question02, response=world.response,
                                root_question=world.root_question, subsection=world.sub_section)


@step(u'When I un-assign a question with a skip rule')
def when_i_un_assign_a_question_with_a_skip_rule(step):
    world.page.click_by_id('close-skip-rule')
    time.sleep(1)
    world.page.click_by_id('unassign-question-%s' % world.skip_question02.id)
    time.sleep(1)
    world.page.click_by_id('confirm-unassign-question-%s' % world.skip_question02.id)

@step(u'When I un-assign the root question to a skip rule')
def when_i_un_assign_the_root_question_to_a_skip_rule(step):
    step.given('And I visit that questionnaires section page')
    world.page.click_by_id('unassign-question-%s' % world.root_question.id)
    time.sleep(1)
    world.page.click_by_id('confirm-unassign-question-%s' % world.root_question.id)

@step(u'When I delete a subsection with a skip rule')
def when_i_delete_a_subsection_with_a_skip_rule(step):
    step.given('And I visit that questionnaires section page')
    world.page.click_by_id('delete-subsection-%s' % world.sub_section_2.id)
    time.sleep(1)
    world.page.click_by_id('confirm-delete-subsection-%s' % world.sub_section_2.id)

@step(u'Then I should see the option to add skip rules to the grid')
def then_i_should_see_the_option_to_add_skip_rules_to_the_grid(step):
    world.page.is_text_present('Add Grid Rules')
    assert world.page.is_element_present_by_id('grid-question-1')

@step(u'When I select the option to add skip rules to the grid')
def when_i_select_the_option_to_add_skip_rules_to_the_grid(step):
    world.page.click_by_id('grid-question-1')
    world.skip_rule_page = SkipRuleModalPage(world.browser)
    world.skip_rule_page.view_existing_rules()

@step(u'When I specify a cell to skip in the grid')
def when_i_specify_a_cell_to_skip_in_the_grid(step):
    world.skip_rule_page.create_new_qn_rule()

@step(u'And that cell should be disabled')
def and_that_cell_should_be_disabled(step):
    world.page.click_by_id('close-skip-rule-button')
    time.sleep(1)
    world.page.assert_one_cell_disabled()