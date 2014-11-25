from lettuce import step, world
from questionnaire.models.skip_rule import SkipQuestion


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
    step.given("Then I should see '0' existing skip rules")