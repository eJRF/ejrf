from lettuce import world, step
from questionnaire.features.pages.home import HomePage
from questionnaire.models import Questionnaire, Section


@step(u'I have four finalised questionnaires')
def given_i_have_four_finalised_questionnaires(step):
    world.questionnaire1 = Questionnaire.objects.create(name="JRF Jamaica version", description="description",
                                                        year=2012, finalized=True)

    Section.objects.create(title="School Based Section1", order=0, questionnaire=world.questionnaire1, name="Name")

    world.questionnaire2 = Questionnaire.objects.create(name="JRF Brazil version", description="description",
                                                        year=2009, finalized=True)
    Section.objects.create(title="School Section1", order=0, questionnaire=world.questionnaire2, name="Section1 name")
    world.questionnaire3 = Questionnaire.objects.create(name="JRF Bolivia version", description="some more description",
                                                        year=2011, finalized=True)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire3, name="School Imm. Delivery")
    world.questionnaire4 = Questionnaire.objects.create(name="JRF kampala version", description="description",
                                                        year=2010, finalized=True)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire4, name="School Imm. Delivery")


@step(u'And I have two draft questionnaires for two years')
def and_i_have_two_draft_questionnaires_for_two_years(step):
    world.questionnaire5 = Questionnaire.objects.create(name="JRF Bolivia version", description="some more description",
                                                        year=2013, finalized=False)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire5, name="School Imm. Delivery")
    world.questionnaire6 = Questionnaire.objects.create(name="JRF kampala version", description="description",
                                                        year=2013, finalized=False)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire6, name="School Imm. Delivery")


@step(u'Then I should see manage JRF, users, question bank, extract and attachments links')
def then_i_should_see_manage_jrf_users_question_bank_extract_and_attachments_links(step):
    world.page.is_text_present("HOME", "EXTRACT", "ATTACHMENTS", "MANAGE JRF", "USERS", "QUESTION BANK")

@step(u'Then I should see a list of the three most recent finalised questionnaires')
def then_i_should_see_a_list_of_the_three_most_recent_finalised_questionnaires(step):
    world.page = HomePage(world.browser)
    world.page.links_present_by_text(["%s %s" % (world.questionnaire1.name, world.questionnaire1.year),
                                     "%s %s" % (world.questionnaire2.name, world.questionnaire2.year),
                                     "%s %s" % (world.questionnaire3.name, world.questionnaire3.year)])

@step(u'And I should see a list of draft questionnaires')
def and_i_should_see_a_list_of_draft_questionnaires(step):
    world.page.links_present_by_text(["%s %s" % (world.questionnaire6.name, world.questionnaire6.year),
                                     "%s %s" % (world.questionnaire5.name, world.questionnaire5.year)])
    world.page.links_present_by_text([" Edit", " Finalize"])

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
    world.page.is_element_present_by_id('id_questionnaire')
    world.page.is_element_present_by_id('id_year')

@step(u'When I select a finalized questionnaire and a reporting year')
def when_i_select_a_finalized_questionnaire_and_a_reporting_year(step):
    world.page.select('questionnaire', world.questionnaire1.id)
    world.page.select('year', world.questionnaire1.year+2)

@step(u'And I give it a new name')
def and_i_give_it_a_new_name(step):
    world.page.fill_form({'name': 'Latest Questionnaire'})

@step(u'When I choose to duplicate the questionnaire')
def when_i_choose_to_duplicate_the_questionnaire(step):
    world.page.click_by_id('save-select_survey_wizard')

@step(u'Then I should see a message that the questionnaire was duplicated successfully')
def then_i_should_see_a_message_that_the_questionnaire_was_duplicated_successfully(step):
    world.page.is_element_present_by_css('.alert alert-success')
    world.page.is_text_present('The questionnaire has been duplicated successfully, You can now go ahead and edit it')

@step(u'Then I should see the new questionnaire listed')
def then_i_should_see_the_new_questionnaire_listed(step):
    world.page.is_text_present('Latest Questionnaire %s' % str(world.questionnaire1.year+2))

@step(u'Then I should a validation error message')
def then_i_should_a_validation_error_message(step):
    world.page.is_element_present_by_css('.error')
    world.page.is_text_present('This field is required.')