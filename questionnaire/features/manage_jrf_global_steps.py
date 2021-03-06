from time import sleep
from lettuce import world, step
from datetime import datetime
from nose.tools import assert_false

from questionnaire.features.pages.home import HomePage
from questionnaire.features.pages.manage import ManageJrfPage
from questionnaire.models import Questionnaire, Section, Organization, Region, SubSection, Question, QuestionGroup
from questionnaire.tests.factories.questionnaire_factory import QuestionnaireFactory
from questionnaire.tests.factories.section_factory import SectionFactory


@step(u'I have four finalised questionnaires')
def given_i_have_four_finalised_questionnaires(step):
    world.finalized_questionnaire_year = 2015
    world.questionnaire1 = Questionnaire.objects.create(name="JRF Jamaica version", description="description",
                                                        year=2012, status=Questionnaire.FINALIZED)

    Section.objects.create(title="School Based Section1", order=0, questionnaire=world.questionnaire1, name="Name")

    world.questionnaire2 = Questionnaire.objects.create(name="JRF Brazil version", description="description",
                                                        year=2009, status=Questionnaire.FINALIZED)
    Section.objects.create(title="School Section1", order=0, questionnaire=world.questionnaire2, name="Section1 name")
    world.questionnaire3 = Questionnaire.objects.create(name="JRF Bolivia version", description="some more description",
                                                        year=2011, status=Questionnaire.FINALIZED)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire3, name="School Imm. Delivery")
    world.questionnaire4 = Questionnaire.objects.create(name="JRF kampala version", description="description",
                                                        year=world.finalized_questionnaire_year, status=Questionnaire.FINALIZED)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire4, name="School Imm. Delivery")


@step(u'And I have two draft questionnaires for two years')
def and_i_have_two_draft_questionnaires_for_two_years(step):
    world.questionnaire5 = Questionnaire.objects.create(name="JRF Bolivia version", description="some more description",
                                                        year=2013, status=Questionnaire.DRAFT)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire5, name="School Imm. Delivery")
    world.questionnaire6 = Questionnaire.objects.create(name="JRF kampala version", description="description",
                                                        year=2013, status=Questionnaire.DRAFT)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire6, name="School Imm. Delivery")


@step(u'Then I should see manage JRF, users, question bank, extract links')
def then_i_should_see_manage_jrf_users_question_bank_extract_and_attachments_links(step):
    world.page.is_text_present("HOME", "EXTRACT", "MANAGE JRF", "USERS", "QUESTIONS")


@step(u'Then I should see a list of the three most recent finalised questionnaires')
def then_i_should_see_a_list_of_the_three_most_recent_finalised_questionnaires(step):
    world.page = HomePage(world.browser)
    world.page.links_present_by_text(["%s %s" % (world.questionnaire1.name, world.questionnaire1.year),
                                      "%s %s" % (world.questionnaire2.name, world.questionnaire2.year),
                                      "%s %s" % (world.questionnaire3.name, world.questionnaire3.year)])


@step(u'And I should see a list of draft questionnaires')
def and_i_should_see_a_list_of_draft_questionnaires(step):
    world.page.links_present_by_text(["%s %s" % (world.questionnaire5.name, world.questionnaire5.year),
                                      "%s %s" % (world.questionnaire6.name, world.questionnaire6.year)])
    assert world.page.is_element_present_by_id('id-edit-questionnaire-%s' % world.questionnaire5.id)
    assert world.page.is_element_present_by_id('id-edit-questionnaire-%s' % world.questionnaire6.id)
    assert world.page.is_element_present_by_id('id-finalize-%s' % world.questionnaire5.id)
    assert world.page.is_element_present_by_id('id-finalize-%s' % world.questionnaire6.id)


@step(u'I visit the manage JRF page')
def and_i_visit_manage_jrf_page(step):
    world.page.click_by_id('id-manage-jrf')


@step(u'And When I click Older')
def and_when_i_click_older(step):
    world.page.click_by_id('id-older-jrf')


@step(u'Then I should also see the fourth finalised questionnaire')
def then_i_should_also_see_the_fourth_finalised_questionnaire(step):
    world.page.links_present_by_text(["%s %s" % (world.questionnaire4.name, world.questionnaire4.year)])


@step(u'When I choose to create a new questionnaire')
def when_i_choose_to_create_a_new_questionnaire(step):
    world.page.click_by_id('id-create-new')


@step(u'Then I should see options for selecting a finalized questionnaire and a reporting year')
def then_i_should_see_options_for_selecting_a_finalized_questionnaire_and_a_reporting_year(step):
    world.page.is_text_present('Finalized Questionnaires')
    world.page.is_text_present('Reporting Year')
    assert world.page.is_element_present_by_id('id_questionnaire')
    assert world.page.is_element_present_by_id('id_year')


@step(u'When I select a finalized questionnaire and a reporting year')
def when_i_select_a_finalized_questionnaire_and_a_reporting_year(step):
    world.page.select('questionnaire', world.questionnaire1.id)
    world.page.select('year', (datetime.now().year + 1))


@step(u'And I give it a new name')
def and_i_give_it_a_new_name(step):
    world.page.fill_form({'name': 'Latest Questionnaire'})


@step(u'When I choose to duplicate the questionnaire')
def when_i_choose_to_duplicate_the_questionnaire(step):
    world.page.click_by_id('duplicate_questionnaire_button')


@step(u'Then I should see a message that the questionnaire was duplicated successfully')
def then_i_should_see_a_message_that_the_questionnaire_was_duplicated_successfully(step):
    world.page.is_element_present_by_css('.alert alert-success')
    world.page.is_text_present('The questionnaire has been duplicated successfully, You can now go ahead and edit it')


@step(u'Then I should see the new questionnaire listed')
def then_i_should_see_the_new_questionnaire_listed(step):
    world.latest_questionnaire = Questionnaire.objects.filter(status=Questionnaire.FINALIZED).latest('created')
    assert world.page.is_element_present_by_id("questionnaire-%s" % world.latest_questionnaire.id)


@step(u'Then I should a validation error message')
def then_i_should_a_validation_error_message(step):
    world.page.is_element_present_by_css('.error')
    world.page.is_text_present('This field is required.')


@step(u'And I have draft and finalised core questionnaires')
def and_i_have_draft_and_finalised_core_questionnaires(step):
    world.questionnaire1 = Questionnaire.objects.create(name="Questionnaire1", description="Section 1 Description",
                                                        year=2010, status=Questionnaire.FINALIZED)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire1, name="Section 1 Name")
    world.questionnaire2 = Questionnaire.objects.create(name="Questionnaire2", description="Section 1 Description",
                                                        year=2011, status=Questionnaire.FINALIZED)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire2, name="Section 1 Name")
    world.questionnaire3 = Questionnaire.objects.create(name="Questionnaire3", description="Section 1 Description",
                                                        year=2012, status=Questionnaire.DRAFT)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire3, name="Section 1 Name")
    world.questionnaire4 = Questionnaire.objects.create(name="Questionnaire4", description="Section 1 Description",
                                                        year=2013, status=Questionnaire.DRAFT)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire4, name="Section 1 Name")


@step(u'Then I should see an option to lock each draft Core Questionnaire')
def then_i_should_see_an_option_to_lock_each_draft_core_questionnaire(step):
    assert (world.page.is_element_present_by_id('id-finalize-%s' % world.questionnaire3.id))
    assert (world.page.is_element_present_by_id('id-finalize-%s' % world.questionnaire4.id))


@step(u'And I should see an option to unlock each finalised Core Questionnaire')
def and_i_should_see_an_option_to_unlock_each_finalised_core_questionnaire(step):
    assert (world.page.is_element_present_by_id('id-unfinalize-%s' % world.questionnaire1.id))
    assert (world.page.is_element_present_by_id('id-unfinalize-%s' % world.questionnaire2.id))


@step(u'When I lock a draft Core Questionnaire')
def when_i_lock_a_draft_core_questionnaire(step):
    world.page.click_by_id('id-finalize-%s' % world.questionnaire3.id)


@step(u'Then it should now have an option to unlock it')
def then_it_should_now_have_an_option_to_unlock_it(step):
    world.page.click_by_id('id-unfinalize-%s' % world.questionnaire3.id)


@step(u'When I unlock a finalised Core Questionnaire')
def when_i_unlock_a_finalised_core_questionnaire(step):
    world.page.click_by_id('id-unfinalize-%s' % world.questionnaire1.id)


@step(u'Then it should now have an option to lock it')
def then_it_should_now_have_an_option_to_lock_it(step):
    world.page.click_by_id('id-finalize-%s' % world.questionnaire1.id)


@step(u'When I click on a Draft Core Questionnaire')
def when_i_click_on_a_draft_core_questionnaire(step):
    world.page.click_by_id('questionnaire-%s' % world.questionnaire4.id)


@step(u'Then it should open in an edit view')
def then_it_should_open_in_an_edit_view(step):
    world.page.is_text_present('New Section')
    world.page.is_text_present('New Subsection')


@step(u'I click on a Finalised Core Questionnaire')
def when_i_click_on_a_finalised_core_questionnaire(step):
    world.page.click_by_id('questionnaire-%s' % world.questionnaire2.id)


@step(u'Then it should open in a preview mode')
def then_it_should_open_in_a_preview_mode(step):
    world.page.is_text_present('New Section', status=False)
    world.page.is_text_present('Assign Question', status=False)
    world.page.is_text_present('New Subsection', status=False)


@step(u'And I have two finalised questionnaires')
def and_i_have_two_finalised_questionnaires(step):
    world.questionnaire7 = Questionnaire.objects.create(name="JRF Kampala", description="description",
                                                        year=2014, status=Questionnaire.FINALIZED)

    Section.objects.create(title="School Based Section1", order=0, questionnaire=world.questionnaire7, name="Name")

    world.questionnaire8 = Questionnaire.objects.create(name="JRF Brazil", description="description",
                                                        year=2015, status=Questionnaire.FINALIZED)
    Section.objects.create(title="School Section1", order=0, questionnaire=world.questionnaire8, name="Section1 name")

    world.org = Organization.objects.create(name="WHO")
    world.afro = Region.objects.create(name="AFRO", organization=world.org)
    world.amer = Region.objects.create(name="AMER", organization=world.org)
    world.euro = Region.objects.create(name="EURO", organization=world.org)
    world.asia = Region.objects.create(name="ASIA", organization=world.org)


@step(u'And I see finalized questionnaires')
def and_i_see_finalized_questionnaires(step):
    world.page.links_present_by_text(["%s %s" % (world.questionnaire7.name, world.questionnaire7.year),
                                      "%s %s" % (world.questionnaire8.name, world.questionnaire8.year)])
    world.page.is_element_present_by_id('id-unfinalize-%s' % world.questionnaire8.id)


@step(u'Then I should see an option to send to regions on each of the finalized questionnaires')
def then_i_should_see_an_option_to_send_to_regions_on_each_of_the_finalized_questionnaires(step):
    world.page.is_element_present_by_id('id-publish-questionnaire-%s' % world.questionnaire7.id)
    world.page.is_element_present_by_id('id-publish-questionnaire-%s' % world.questionnaire8.id)


@step(u'When I choose option to send core questionnaire to regions')
def when_i_choose_option_to_send_core_questionnaire_to_regions(step):
    world.page.click_by_id('id-publish-questionnaire-%s' % world.questionnaire7.id)


@step(u'Then I should see an interface to choose the regions to which to publish the finalised Core Questionnaire')
def then_i_should_see_an_interface_to_choose_the_regions_to_which_to_publish_the_finalised_core_questionnaire(step):
    world.page.is_text_present("Publish Questionnaire : %s" % world.questionnaire7.name)


@step(u'And I should be able to select one region to which to publish the finalised Core Questionnaire')
def and_i_should_be_able_to_select_one_region_to_which_to_publish_the_finalised_core_questionnaire(step):
    world.page.check("%s" % world.afro.id)
    world.page.click_by_css('button.submit')


@step(u'And I select two regions to which to publish the finalised Core Questionnaire')
def and_i_select_two_regions_to_which_to_publish_the_finalised_core_questionnaire(step):
    world.page.check(world.amer.id)
    world.page.check(world.asia.id)


@step(u'When I click publish button')
def when_i_click_publish_button(step):
    world.page.click_by_css('.submit')


@step(u'And I should be able to confirm that the Core Questionnaire is published to the regions I selected')
def and_i_should_be_able_to_confirm_that_the_core_questionnaire_is_published_to_the_regions_i_selected(step):
    world.page.is_text_present("The questionnaire has been published to %s, %s" % (world.amer.name, world.asia.name))
    world.page.is_text_present("%s" % world.amer.name)
    world.page.is_text_present("%s" % world.asia.name)


@step(u'And I should be able to confirm that the regions to which I published the questionnaire is not on the list')
def and_i_should_be_able_to_confirm_that_the_regions_to_which_i_published_the_questionnaire_is_not_on_the_list(step):
    world.page.click_by_id('id-publish-questionnaire-%s' % world.questionnaire7.id)
    world.page.is_text_present("%s" % world.amer.name, status=False)
    world.page.is_text_present("%s" % world.asia.name, status=False)


@step(u'And I have a finalised regional questionnaire')
def and_i_have_a_finalised_regional_questionnaire(step):
    world.finalised_regional_questionnaire = Questionnaire.objects.create(name="JRF Finalised Regional",
                                                                          description="Description",
                                                                          year=2014, status=Questionnaire.FINALIZED,
                                                                          region=world.region_afro)
    world.regional_section = Section.objects.create(order=0, title="Section AFRO", description="Description",
                                                    questionnaire=world.finalised_regional_questionnaire,
                                                    name="Cover page")
    world.regional_subsection = SubSection.objects.create(order=1, section=world.regional_section)

    world.regional_question1 = Question.objects.create(text='Name of person in Ministry of Health', UID='C001',
                                                       answer_type='Text')

    parent = QuestionGroup.objects.create(subsection=world.regional_subsection, order=1)
    parent.question.add(world.regional_question1)


@step(u'When I click that regional questionnaire')
def when_i_click_that_regional_questionnaire(step):
    world.page.click_by_id('questionnaire-%s' % world.finalised_regional_questionnaire.id)


@step(u'When I select to approve the regional questionnaire')
def when_i_select_to_approve_the_regional_questionnaire(step):
    world.page.click_by_id('id-approve-questionnaire-%s' % world.finalised_regional_questionnaire.id)


@step(u'Then I should see a confirmation prompt to approve the questionnaire')
def then_i_should_see_a_confirmation_prompt_to_approve_the_questionnaire(step):
    world.page.is_text_present('Confirm Questionnaire Acceptance')
    world.page.is_text_present('Are you sure you want to accept this questionnaire?')


@step(u'When I confirm the questionnaire approval')
def when_i_confirm_the_questionnaire_approval(step):
    world.page.click_by_id('confirm-accept-questionnaire-%s' % world.finalised_regional_questionnaire.id)


@step(u'Then I should see a message that the questionnaire was approved')
def then_i_should_see_a_message_that_the_questionnaire_was_approved(step):
    world.page.is_text_present('The questionnaire has been accepted successfully.')


@step(u'And I should see a new status indicating that the questionnaire was approved')
def and_i_should_see_a_new_status_indicating_that_the_questionnaire_was_approved(step):
    world.page.is_text_present('Published')


@step(u'And there should no longer be an option to approve the questionnaire')
def and_there_should_no_longer_be_an_option_to_approve_the_questionnaire(step):
    assert world.page.is_element_not_present_by_id(
        "id-approve-questionnaire-%s" % world.finalised_regional_questionnaire.id)


@step(u'Then I should see modal with the questionnaires current name')
def then_i_should_see_modal_with_the_questionnaires_current_name(step):
    world.page.is_text_present('Edit Name Of Questionnaire')
    world.page.is_text_present(world.questionnaire5.name)


@step(u'When I update the name of the questionnaire and save my changes')
def when_i_update_the_name_of_the_questionnaire_and_save_my_changes(step):
    world.page.fill_this_element('id_name', 'Updated Questionnaire Name')
    world.page.select('year', 2014)
    world.page.click_by_id('save-questionnaire-name-%s' % world.questionnaire5.id)


@step(u'Then I should see a message that questionnaire was updated')
def then_i_should_see_a_message_that_questionnaire_was_updated(step):
    world.page.is_text_present('The revision was updated successfully.')


@step(u'And I should see the questionnaire with its new name')
def and_i_should_see_the_questionnaire_with_its_new_name(step):
    sleep(10)
    world.page.is_text_present('Updated Questionnaire Name')


@step(u'Then I should view it in preview mode')
def then_i_should_view_it_in_preview_mode(step):
    assert_false(world.page.is_element_present_by_id('id-edit-section-%s' % world.finalised_section.id))
    assert_false(world.page.is_element_present_by_id('id-delete-section-%s' % world.finalised_section.id))


@step(u'And I have "([^"]*)" "([^"]*)" core questionnaire')
def and_i_have_group1_group2_core_questionnaire(step, number, status):
    create_questionnaire(world, number, status)


@step(u'When I click "([^"]*)" button on that core questionnaire')
def when_i_click_group1_button_on_that_core_questionnaire(step, action):
    world.page.click_by_id('id-%s-questionnaire-%s' % (action, world.finalised_core_questionnaire.id))


@step(u'When I confirm "([^"]*)" the questionnaire')
def when_i_confirm_group1_the_questionnaire(step, action):
    world.page.click_by_id('confirm-%s-questionnaire-%s' % (action, world.finalised_core_questionnaire.id))
    sleep(1)

@step(u'Then I should see the questionnaire "([^"]*)"')
def then_i_should_see_the_questionnaire_group1(step, status):
    sleep(2)
    world.page.is_text_present(
        'The questionnaire \'%s\' was %s successfully.' % (world.finalised_core_questionnaire.name, status))


@step(u'When I click on the "([^"]*)" questionnaire')
def when_i_click_on_the_group1_questionnaire(step, status):
    world.page.click_by_id('%s-questionnaire-%s' % (status, world.finalised_core_questionnaire.id))


def create_questionnaire(world, number, status):
    for i in range(int(number)):
        world.finalised_core_questionnaire = Questionnaire.objects.create(
            name="JRF %s Regional %d" % (status.capitalize(), i),
            description="Description",
            year='201%d' % i, status=status,
            region=None)
        world.finalised_section = SectionFactory(questionnaire=world.finalised_core_questionnaire)
        world.finalized_subsection = SubSection.objects.create(order=1, section=world.finalised_section)

        world.refinalized_question1 = Question.objects.create(text='Name of person in Ministry of Health',
                                                              UID='C001%s' % i,
                                                              answer_type='Text')

        parent = QuestionGroup.objects.create(subsection=world.finalized_subsection, order=i)
        parent.question.add(world.refinalized_question1)


@step(u'When I click the edit questionnaire button')
def when_i_click_the_edit_questionnaire_button(step):
    world.page.click_by_id('id-edit-questionnaire-%s' % world.questionnaire5.id)
    sleep(2)


@step(u'I update the year to one of the finalized questionnaire year')
def and_i_update_the_year_to_2014(step):
    world.page.select('year', world.finalized_questionnaire_year)


@step(u'Then I should see a warning message')
def then_i_should_see_a_warning_message(step):
    warning_message = 'A Revision of the year %s already exists. If you go ahead, that revision will be archived.' % world.finalized_questionnaire_year
    world.page.is_text_present(warning_message)


@step(u'When I save my changes')
def when_i_save_my_changes(step):
    world.page.click_by_id('save-questionnaire-name-%s' % world.questionnaire5.id)


@step(u'I should see the corresponding existing finalized questionnaire is archived')
def then_i_should_see_the_existing_2012_questionnaire_is_archived(step):
    world.page.is_element_present_by_id('archived-questionnaire-%s' % world.questionnaire4.id)