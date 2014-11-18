from time import sleep, time
from IPython import embed
from lettuce import step, world
from questionnaire.features.pages.questionnaires import QuestionnairePage
from questionnaire.features.pages.sections import CreateSubSectionPage
from questionnaire.features.pages.skip_rule_modal import SkipRuleModalPage
from questionnaire.models import SubSection, Section, Questionnaire, Question, QuestionGroupOrder
from questionnaire.models.skip_rule import SkipQuestion, SkipRule, SkipSubsection
from questionnaire.tests.factories.question_factory import QuestionFactory
from questionnaire.tests.factories.question_group_factory import QuestionGroupFactory
from questionnaire.tests.factories.question_option_factory import QuestionOptionFactory


@step(u'And I click add new subsection link')
def and_i_click_add_new_subsection_link(step):
    world.page.click_by_id("new-subsection")

@step(u'Then I should see a new subsection modal')
def then_i_should_see_a_new_subsection_modal(step):
    world.page = CreateSubSectionPage(world.browser, world.questionnaire, world.section_1)
    world.page.is_text_present("New Subsection", "Description", "Title")

@step(u'When i fill in the subsection data')
def when_i_fill_in_the_subsection_data(step):
    data = {'title': '',
            'description': 'some description'}

    world.page.fill_this_form('#new-subsection-modal', data)
    sleep(3)

@step(u'And I save the subsection')
def and_i_save_the_subsection(step):
    world.page.click_by_id('save-new-subsection-modal')

@step(u'Then I should see the subsection I just created')
def then_i_should_see_the_subsection_i_just_created(step):
    world.page = QuestionnairePage(world.browser, world.section_1)
    world.page.is_text_present('Subsection successfully created.')

@step(u'And I choose to update a subsection')
def and_i_choose_to_update_a_subsection(step):
    world.page.click_by_id('edit-subsection-%s' % world.sub_section.id)

@step(u'Then I should see an edit subsection modal')
def then_i_should_see_an_edit_subsection_modal(step):
    world.page = CreateSubSectionPage(world.browser, world.questionnaire, world.section_1)
    world.page.is_text_present("Edit SubSection", "Title", "Description")

@step(u'When I update the subsection details')
def when_i_update_the_subsection_details(step):
    world.data = {'title': 'New SubSection Name',
                  'description': 'New SubSection description'}
    world.page.fill_this_form('#edit_subsection_%s_modal_form' % world.sub_section.id, world.data)

@step(u'And I save the changes to the subsection')
def and_i_save_the_changes_to_the_subsection(step):
    world.page.click_by_id('submit_edit_subsection_%s' % world.sub_section.id)

@step(u'Then I should see a message that the subsection was updated')
def then_i_should_see_a_message_that_the_subsection_was_updated(step):
    world.page.is_text_present('SubSection updated successfully')

@step(u'And I should see the changes I made to the subsection in the questionnaire')
def and_i_should_see_the_changes_i_made_to_the_subsection_in_the_questionnaire(step):
    world.page.is_text_present(world.data['title'])


@step(u'And I choose to delete one of the sub sections from the questionnaire')
def and_i_choose_to_delete_one_of_the_sub_sections_from_the_questionnaire(step):
    world.page.click_by_id('delete-subsection-%s' % world.sub_section.id)

@step(u'Then I should not see core subsection edit link')
def then_i_should_not_see_core_subsection_edit_link(step):
    world.page.find_by_id("edit-subsection-%d" % world.core_sub_section.id, False)

@step(u'When I click the edit link for regional subsection')
def when_i_click_the_edit_link_for_regional_subsection(step):
    world.page.click_by_id("edit-subsection-%d" % world.sub_section.id)

@step(u'Then I should see a success message that the subsection was updated')
def then_i_should_see_a_success_message_that_the_subsection_was_updated(step):
    world.page.is_text_present('SubSection updated successfully')

@step(u'And I should see those changes to the regional subsection in the questionnaire')
def and_i_should_see_those_changes_to_the_regional_subsection_in_the_questionnaire(step):
    world.page.is_text_present('New SubSection Name')
    world.page.is_text_present('New SubSection description')

@step(u'And I have a questionnaire in a region with sections and subsections')
def and_i_have_a_questionnaire_in_a_region_with_sections_and_subsections(step):
    world.questionnaire = Questionnaire.objects.create(name="JRF Bolivia version", description="some more description",
                                                       year=2013, status=Questionnaire.DRAFT, region=world.region)
    world.section1 = Section.objects.create(order=0, title="WHO/UNICEF Joint Reporting Form",
                                            questionnaire=world.questionnaire, name="Cover page", region=world.region)
    world.section_1 = Section.objects.create(order=2, title="section_1",
                                             questionnaire=world.questionnaire, name="Cover page")
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
    world.sub_section = SubSection.objects.create(title="other R subs", order=1, section=world.section_1,
                                                  region=world.region)
    world.core_sub_section = SubSection.objects.create(title="core subs", order=2, section=world.section_1)


@step(u'And I have questions and responses in the correct section')
def and_i_have_questions_and_responses_in_the_correct_section(step):
    world.root_question = QuestionFactory()
    world.question_to_skip = QuestionFactory(text="question 2")
    world.response = QuestionOptionFactory(question=world.root_question)
    question_group = QuestionGroupFactory(subsection=world.sub_section, order=1)
    QuestionGroupOrder.objects.create(question=world.root_question, order=1, question_group=question_group)
    QuestionGroupOrder.objects.create(question=world.question_to_skip, order=2, question_group=question_group)

    world.root_question.question_group.add(question_group)
    world.question_to_skip.question_group.add(question_group)


@step(u'And I click to add a skip rule')
def and_i_click_to_add_a_skip_rule(step):
    world.page.click_by_id('id-create-skip-rule-%s' % world.sub_section.id)
    world.skip_rule_page = SkipRuleModalPage(world.browser)

@step(u'And I choose to see existing skip rules')
def and_i_choose_to_see_existing_skip_rules(step):
    world.skip_rule_page.view_existing_rules()

@step(u'Then I should see \'([^\']*)\' existing skip rules')
def then_i_should_see_group1_existing_skip_rules(step, number_of_rules):
    actual_number = world.skip_rule_page.number_of_rules()
    sleep(2)
    assert (actual_number == int(number_of_rules)), 'Expecting %s number of rules, got %s number of rules' % (int(number_of_rules), actual_number)

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

@step(u'I should see the questions in that subsection listed')
def i_should_see_the_questions_in_that_subsection_listed(step):
    world.browser.find_by_name('skip_question')[0].click()
    world.page.is_text_present('question 2')

@step(u'I should see the subsections in that section listed')
def i_should_see_the_subsections_in_that_section_listed(step):
    world.browser.find_by_name('skip_subsection')[0].click()
    world.page.is_text_present('Subsection Title Sample')

@step(u'And I have skip rules applied to a question')
def and_i_have_skip_rules_applied_to_a_question(step):
    SkipQuestion.objects.create(skip_question=world.question_to_skip, response=world.response,
                                root_question=world.root_question, subsection=world.sub_section)

@step(u'And I have skip rules applied to a subsection')
def and_i_have_skip_rules_applied_to_a_subsection(step):
    SkipSubsection.objects.create(skip_subsection=world.sub_section_2, response=world.response,
                                root_question=world.root_question, subsection=world.sub_section)

@step(u'And the questionnaire has been published to the data submitter')
def and_the_questionnaire_has_been_published_to_the_data_submitter(step):
    world.questionnaire.region = world.region
    world.questionnaire.status = Questionnaire.PUBLISHED
    world.questionnaire.save()

@step(u'Then I should see the all the questions and subsections in that section')
def then_i_should_see_the_all_the_questions_in_that_section_and_subsection(step):
    world.page._is_text_present(world.question_to_skip.text)
    world.page._is_text_present(world.root_question.text)
    world.page._is_text_present(world.sub_section_2.title)

@step(u'When I select a response that skips a question')
def when_i_select_a_response_that_skips_a_question(step):
    world.page.choose('MultiChoice-0-response', '1')

@step(u'Then that question should no longer be displayed')
def then_that_question_should_no_longer_be_displayed(step):
    world.page._is_text_present(world.question_to_skip.text, False)

@step(u'When I create a new subsection skip rule')
def when_i_create_a_new_subsection_skip_rule(step):
    world.skip_rule_page.create_new_sub_rule()

@step(u'And that subsection should no longer be displayed')
def and_that_subsection_should_no_longer_be_displayed(step):
    world.page._is_text_present(world.sub_section_2.title, False)