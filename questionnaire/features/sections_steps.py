from time import sleep
from lettuce import step, world
from questionnaire.features.pages.home import HomePage
from questionnaire.features.pages.questionnaires import QuestionnairePage
from questionnaire.features.pages.sections import CreateSectionPage
from questionnaire.features.pages.step_utils import create_user_with_no_permissions, assign, \
    create_global_admin_with_no_permissions
from questionnaire.features.pages.users import LoginPage
from nose.tools import assert_false


@step(u'Given I am logged in as a global admin')
def given_i_am_logged_in_as_a_global_admin(step):
    world.region = None
    user = create_global_admin_with_no_permissions(username='Rajni')
    world.user = user
    world.user = assign('can_view_users', user)
    world.user = assign('can_edit_questionnaire', user)
    world.user = assign('can_view_questionnaire', user)

    world.page = LoginPage(world.browser)
    world.page.visit()
    world.page.login(world.user, "pass")


@step(u'I click add new section link')
def and_i_click_add_new_section_link(step):
    world.page.click_by_id("new-section")


@step(u'Then I should see a new section modal')
def then_i_should_see_a_new_section_modal(step):
    world.page = CreateSectionPage(world.browser, world.questionnaire)
    world.page.is_text_present("New Section", "Description", "Name", "Title")


@step(u'When i fill in the section data')
def when_i_fill_in_the_section_data(step):
    world.page.fill_form({'name': 'Some section'})
    sleep(2)
    world.page.fill_form({'title': 'Some title'})
    sleep(2)
    world.page.fill_form({'description': 'some description'})
    sleep(2)


@step(u'Then I should see the section I created')
def then_i_should_see_the_section_i_created(step):
    world.page = QuestionnairePage(world.browser, world.section_1)
    world.page.is_text_present('Section created successfully')
    world.page.is_text_present('Some section')


@step(u'And I save the section')
def and_i_save_the_section(step):
    world.page.click_by_id('save-new-section-modal')
    sleep(5)


@step(u'And I fill in invalid data')
def and_i_fill_in_invalid_data(step):
    data = {'name': '',
            'title': '',
            'description': 'some description'}
    world.page = CreateSectionPage(world.browser, world.questionnaire)
    world.page.fill_form(data)


@step(u'Then I should see error messages against the fields')
def then_i_should_see_error_messages_against_the_fields(step):
    world.page.is_text_present('This field is required')


@step(u'I choose to update a section')
def and_i_choose_to_update_a_section(step):
    world.page.click_by_id('id-edit-section-%s' % world.section1.id)


@step(u'Then I should see an edit section modal')
def then_i_should_see_an_edit_section_modal(step):
    world.page = CreateSectionPage(world.browser, world.questionnaire)
    world.page.is_text_present("Edit Section", "Description", "Name", "Title")


@step(u'When I update the section details')
def when_i_update_the_section_details(step):
    data = {'name': 'New Section Name',
            'title': 'New Section Title'}
    world.page.fill_form(data)


@step(u'And I save the changes to the section')
def and_i_save_the_changes_to_the_section(step):
    world.page.click_by_id('submit_edit_section_%s' % world.section1.id)


@step(u'Then I should see a message that the section was updated')
def then_i_should_see_a_message_that_the_section_was_updated(step):
    world.page.is_text_present('Section updated successfully')


@step(u'And I should see the changes I made to the section in the questionnaire')
def and_i_should_see_the_changes_i_made_to_the_section_in_the_questionnaire(step):
    world.page.is_text_present('New Section Name')
    world.page.is_text_present('New Section Title')


@step(u'Then I should see an option to delete each section')
def then_i_should_see_an_option_to_delete_each_section(step):
    assert world.page.is_element_present_by_id('id-delete-section-%s' % world.section_1.id)
    assert world.page.is_element_present_by_id('id-delete-section-%s' % world.section_2.id)

@step(u'Then I should not see an option to delete that section')
def then_i_should_see_an_option_to_delete_each_section(step):
    assert_false(world.page.is_element_present_by_id('id-delete-section-%s' % world.section_1.id))

@step(u'When I choose to delete a section')
def when_i_choose_to_delete_a_section(step):
    world.page.click_by_id('id-delete-section-%s' % world.section_2.id)


@step(u'Then I should see a confirmation message')
def then_i_should_see_a_confirmation_message(step):
    world.page.is_text_present('Delete Section')
    world.page.is_text_present('Are you sure you want to delete this section')


@step(u'When I confirm the deletion')
def when_i_confirm_the_deletion(step):
    world.page.click_by_id('confirm-delete-section-%s' % world.section_2.id)


@step(u'Then I should see a message that the section was deleted')
def then_i_should_see_a_message_that_the_section_was_deleted(step):
    world.page.is_text_present('Section successfully deleted')


@step(u'And the section should no longer appear in the Questionnaire')
def and_the_section_should_no_longer_appear_in_the_questionnaire(step):
    world.page.is_text_present(world.section_2.name, status=False)


@step(u'And the section numbering should be updated')
def and_the_section_numbering_should_be_updated(step):
    world.page.click_link_by_partial_href(
        'questionnaire/entry/%s/section/%s' % (world.questionnaire.id, world.section_3.id))
    world.page.is_text_present('2. %s' % world.section_3.title)


@step(u'Given I am logged in as a regional admin')
def given_i_am_logged_in_as_a_regional_admin(step):
    user, _, _ = create_user_with_no_permissions(username='Rajni')
    world.user = assign('can_edit_questionnaire', user)

    world.page = LoginPage(world.browser)
    world.page.visit()
    world.page.login(world.user, "pass")


@step(u'And I save the regional section')
def and_i_save_the_regional_section(step):
    and_i_save_the_section(step)


@step(u'Then I should see the regional section I created')
def then_i_should_see_the_regional_section_i_created(step):
    world.page.is_text_present('%s - %s' % (world.region.name, 'Some section'))


@step(u'I choose to delete one of the section from the questionnaire')
def and_i_choose_to_delete_one_of_the_section_from_the_questionnaire(step):
    world.page.click_by_id("id-delete-section-%s" % world.section_2.id)


@step(u'Then I should not see edit icon for core sections')
def then_i_should_not_see_edit_icon_for_core_sections(step):
    world.page.find_by_id("id-edit-section-%d" % world.section4.id, False)


@step(u'And I should see the changes I made to the regional section in the questionnaire')
def and_i_should_see_the_changes_i_made_to_the_regional_section_in_the_questionnaire(step):
    world.page.is_text_present('%s - %s' % (world.region.name, 'New Section Name'))
    world.page.is_text_present('%s - %s' % (world.region.name, 'New Section Title'))

@step(u'Then I should see a delete subsection confirmation message')
def then_i_should_see_a_delete_subsection_confirmation_message(step):
    world.page.is_text_present('Confirm Delete Subsection')
    world.page.is_text_present('Are you sure you want to delete this subsection')


@step(u'Then I should see a message that the sub-section was deleted')
def then_i_should_see_a_message_that_the_sub_section_was_deleted(step):
    world.page.is_text_present("Subsection successfully deleted.")

@step(u'And the sub section should no longer appear in the Questionnaire')
def and_the_sub_section_should_no_longer_appear_in_the_questionnaire(step):
    world.page.is_text_present("%s" % world.sub_section.title, status=False)

@step(u'When I confirm my intention to delete that subsection')
def when_i_confirm_my_intention_to_delete_that_subsection(step):
    world.page.click_by_id('confirm-delete-subsection-%s' % world.sub_section.id)


@step(u'Then I should see an option to add a new regional section')
def then_i_should_see_an_option_to_add_a_new_regional_section(step):
    world.page.is_text_present('New Section')
    assert world.page.is_element_present_by_id('new-section')


@step(u'And its name and title should be prefixed with the region name')
def and_its_name_and_title_should_be_prefixed_with_the_region_name(step):
    world.page.is_text_present('%s - %s' % (world.region.name, 'Some section'))
    world.page.is_text_present('%s - %s' % (world.region.name, 'Some title'))


@step(u'And I should see an option to edit regional sections')
def and_i_should_see_an_option_to_edit_regional_sections(step):
    world.page.find_by_id("id-edit-section-%d" % world.section1.id)

@step(u'When I confirm my intention to delete that subsection')
def when_i_confirm_my_intention_to_delete_that_subsection(step):
    world.page.click_by_id('confirm-delete-subsection-%s' % world.sub_section.id)


@step(u'Then I should see options to delete the regional sections')
def then_i_should_see_options_to_delete_the_regional_sections(step):
    world.page.find_by_id("id-delete-section-%d" % world.section1.id)


@step(u'And I am viewing the manage regional JRF page')
def and_i_am_viewing_the_manage_regional_jrf_page(step):
    world.page = HomePage(world.browser)
    world.page.visit()


@step(u'When I choose to delete one of the regional sections')
def when_i_choose_to_delete_one_of_the_regional_sections(step):
    world.page.click_by_id('id-delete-section-%s' % world.section1.id)


@step(u'When I confirm the regional section deletion')
def when_i_confirm_the_regional_section_deletion(step):
    world.page.click_by_id('confirm-delete-section-%s' % world.section1.id)


@step(u'And the regional section should no longer appear in the Questionnaire')
def and_the_regional_section_should_no_longer_appear_in_the_questionnaire(step):
    world.page.is_text_present(world.section1.name, status=False)


@step(u'And the numbering of the remaining sections should be updated')
def and_the_numbering_of_the_remaining_sections_should_be_updated(step):
    world.page.click_link_by_partial_href('/questionnaire/entry/%s/section/%s/' %(world.questionnaire.id, world.section3.id))
    world.page.is_text_present('%d. %s - %s' %(world.section3.order, world.region, world.section3.name))
