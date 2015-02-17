from time import sleep
from lettuce import step, world
from questionnaire.features.pages.questionnaires import QuestionnairePage
from questionnaire.features.pages.sections import CreateSubSectionPage
from questionnaire.models import SubSection, Section, Questionnaire


@step(u'And I click add new subsection link')
def and_i_click_add_new_subsection_link(step):
    world.page.click_by_id("new-subsection")

@step(u'Then I should see a new subsection modal')
def then_i_should_see_a_new_subsection_modal(step):
    world.page = CreateSubSectionPage(world.browser, world.questionnaire, world.section_1)
    world.page.is_text_present("New Subsection", "Description", "Title")

@step(u'When i fill in the subsection data')
def when_i_fill_in_the_subsection_data(step):
    data = {'title': ''}
    world.page.fill_this_form('#new-subsection-modal', data)
    world.page.fill_trumbowyg_editor('#new-subsection-modal', 'some description')
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
    world.data = {'title': 'New SubSection Name'}
    form_id = '#edit_subsection_%s_modal_form' % world.sub_section.id
    world.page.fill_this_form(form_id, world.data)
    world.page.fill_trumbowyg_editor(form_id, 'New SubSection description')
    sleep(2)

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


@step(u'And that subsection should no longer be displayed')
def and_that_subsection_should_no_longer_be_displayed(step):
    world.page.click_by_id('save_draft_button')
    world.page.is_text_present(world.sub_section_2.title, status=False)

@step(u'Then I should see the subsections numbered according to their respective orders')
def then_i_should_see_the_subsections_numbered_according_to_their_respective_orders(step):
    world.page.validate_numbering_of_subsection('1.1.', world.sub_section)
    world.page.validate_numbering_of_subsection('1.2.', world.sub_section_2)
    world.page.validate_numbering_of_subsection('1.3.', world.sub_section_3)

@step(u'When I select the option to change the position of the second subsection')
def when_i_select_the_option_to_change_the_position_of_the_second_subsection(step):
    world.page.click_by_id("id-change-position-%s" % world.sub_section_2.id)

@step(u'Then I should see its current position marked as such')
def then_i_should_see_its_current_position_marked_as_such(step):
    world.page.is_text_present('2 (Current)')

@step(u'And I should see the other positions available')
def and_i_should_see_the_other_positions_available(step):
    world.browser.find_by_name('modal-subsection-position')[0].click()
    world.page.is_text_present('1')
    world.page.is_text_present('3')

@step(u'When I move the second subsection to the first position')
def when_i_move_the_second_subsection_to_the_first_position(step):
    world.page.select('modal-subsection-position', 1)
    world.page.click_by_id('submit_subsection_position_button')

@step(u'Then the numbering of all the other subsections should be updated')
def then_the_numbering_of_all_the_other_subsections_should_be_updated(step):
    world.page.validate_numbering_of_subsection('1.1.', world.sub_section_2)
    world.page.validate_numbering_of_subsection('1.2.', world.sub_section)
    world.page.validate_numbering_of_subsection('1.3.', world.sub_section_3)