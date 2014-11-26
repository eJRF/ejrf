from time import sleep
from lettuce import step, world
from questionnaire.models import Question, QuestionGroup, QuestionGroupOrder


@step(u'And I have a questionnaire with a grid')
def and_i_have_a_questionnaire_with_a_grid(step):
    step.given('And I have both simple and primary questions in my Question Bank')
    step.given('And I have a questionnaire with sections and with subsections')
    step.given('And I am editing that questionnaire')
    step.given('When I choose to create a new grid question for a particular subsection')
    sleep(1)
    step.given('When I choose to create a grid with all options shown')
    step.given('When I select the primary questions and columns for the all options grid')
    step.given('And I save my grid')


@step(u'Then I should see options to move the grid position up or down')
def then_i_should_see_options_to_move_the_grid_position_up_or_down(step):
    world.page.is_text_present('Move Up')
    world.page.is_text_present('Move Down')


@step(u'When I select the option to move the grid down')
def when_i_select_the_option_to_move_the_grid_down(step):
    world.page.click_by_id('btn-movedwn-1')


@step(u'Then I should see a message that it cannot be moved \'([^\']*)\'')
def then_i_should_see_a_message_that_it_cannot_be_moved_group1(step, direction):
    if direction == 'up':
        world.page.is_text_present('The Grid was not moved up because its the first in this subsection')
    else:
        world.page.is_text_present('The Grid was not moved down because its the last in this subsection')


@step(u'When I select the option to move the grid up')
def when_i_select_the_option_to_move_the_grid_up(step):
    world.page.click_by_id('btn-moveup-1')


@step(u'Given there are other questions in that subsection')
def given_there_are_other_questions_in_that_subsection(step):
    world.question1 = Question.objects.create(text='UNICEF contact', export_label='UNICEF Contact',
                                              UID='00026', answer_type='Text')
    world.question2 = Question.objects.create(text='WHO contact', export_label='WHO Contact', UID='00028',
                                              answer_type='Text')

    parent = QuestionGroup.objects.create(subsection=world.sub_section, order=2)
    parent.question.add(world.question1, world.question2)

    QuestionGroupOrder.objects.create(question=world.question1, question_group=parent, order=1)
    QuestionGroupOrder.objects.create(question=world.question2, question_group=parent, order=2)


@step(u'Then I should see the questions in the grid numbered as \'([^\']*)\' \'([^\']*)\' \'([^\']*)\'')
def then_i_should_see_the_questions_in_the_grid_numbered_as_pos1_pos2_pos3(step, position1, position2, position3):
    world.page.is_text_present(position1)
    world.page.is_text_present(position2)
    world.page.is_text_present(position3)