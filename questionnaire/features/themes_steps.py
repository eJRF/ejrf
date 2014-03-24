from time import sleep
from lettuce import step, world
from questionnaire.features.pages.theme import ThemePage
from questionnaire.models import Theme


@step(u'Given I have 100 themes')
def given_i_have_100_themes(step):
    for counter in range(100):
        Theme.objects.create(name='theme %d' % counter, description="Description for theme %d" % counter)


@step(u'And I visit the themes listing page')
def and_i_visit_the_themes_listing_page(step):
    world.page = ThemePage(world.browser)
    world.page.visit()


@step(u'Then I should see 2 of the themes')
def then_i_should_see_the_themes_paginated(step):
    for counter in range(2):
        world.page.is_text_present('theme %d' % counter, "Description for theme %d" % counter)


@step(u'And I click New Theme button')
def and_i_click_new_theme_button(step):
    world.page.click_by_id("new-theme")
    sleep(2)


@step(u'When I fill in valid theme details')
def when_i_fill_in_valid_theme_details(step):
    world.theme_data = {
        'name': "Immunization",
        'description': 'About Immunization'}
    world.page.fill_form(world.theme_data)


@step(u'Then I should see the success message')
def then_i_should_see_the_success_message(step):
    world.page.is_text_present("Theme successfully created.")


@step(u'And I should see the newly created theme in the themes list')
def and_i_should_see_the_newly_created_theme_in_the_themes_list(step):
    world.page.is_text_present(world.theme_data['name'], world.theme_data['description'])


@step(u'And I click the save theme button')
def and_i_click_the_save_theme_button(step):
    world.page.click_by_id("save-new-themes-modal")


@step(u'And I fill in only description')
def and_i_fill_in_only_description(step):
    world.page.fill_form({'description': 'name of the theme is missing'})


@step(u'Then I should see errors on the form')
def then_i_should_see_errors_on_the_form(step):
    world.page.is_text_present("This field is required.")


@step(u'And I click Edit theme button')
def and_i_click_edit_theme_button(step):
    world.page.click_by_id('edit-theme-%s-btn' % world.theme1.id)


@step(u'And i fill in the theme name')
def and_i_fill_in_the_theme_name(step):
    sleep(1)
    world.page.fill_form({'name': 'Edited name'})


@step(u'Then I should see the update success message')
def then_i_should_see_the_update_success_message(step):
    world.page.is_text_present("Theme successfully updated.")

@step(u'And I click the update theme button')
def and_i_click_the_update_theme_button(step):
    world.page.click_by_id("save-theme-%s-btn" % world.theme1.id)

@step(u'And I should see the updated theme in the themes list')
def and_i_should_see_the_updated_theme_in_the_themes_list(step):
    world.page.is_text_present('Edited name')