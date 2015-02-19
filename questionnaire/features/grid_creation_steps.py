from time import sleep
from lettuce import world, step
from nose.tools import assert_true, assert_equals
from questionnaire.features.pages.questionnaires import QuestionnairePage
from questionnaire.models import Question, QuestionOption, Theme, QuestionGroupOrder
from questionnaire.tests.factories.question_group_factory import QuestionGroupFactory


@step(u'And I have both simple and primary questions in my Question Bank')
def and_i_have_both_simple_and_primary_questions_in_my_question_bank(step):
    world.theme = Theme.objects.create(name="Grid Questions Theme")

    world.grid_question1 = Question.objects.create(text='Primary Option', UID='C00021', answer_type='MultiChoice',
                                                   is_primary=True, theme=world.theme)
    world.option1 = QuestionOption.objects.create(text='Option A', question=world.grid_question1)
    world.option2 = QuestionOption.objects.create(text='Option B', question=world.grid_question1)
    world.option3 = QuestionOption.objects.create(text='Option C', question=world.grid_question1)

    world.grid_question2 = Question.objects.create(text='First Column Question - Q2',
                                                   export_label='First Column Question - Q2', UID='C00022', answer_type='Number',
                                                   theme=world.theme)
    world.grid_question3 = Question.objects.create(text='Second Column Question - Q3', export_label='Second Column Question - Q3', UID='C00023', answer_type='Number',
                                                   theme=world.theme)
    world.grid_question4 = Question.objects.create(text='Third Column Question - Q4',
                                                   export_label='Third Column Question - Q4', UID='C00024', answer_type='Number',
                                                   theme=world.theme)
    world.grid_question5 = Question.objects.create(text='Fourth Column Question - Q5',
                                                   export_label='Fourth Column Question - Q5', UID='C00025', answer_type='Number',
                                                   theme=world.theme)
    world.grid_question6 = Question.objects.create(text='Sixth Column Question - Q6',
                                                   export_label='Sixth Column Question - Q6', UID='C00026', answer_type='Number',
                                                   theme=world.theme)


@step(u'And I am editing that questionnaire')
def and_i_am_editing_that_questionnaire(step):
    world.page = QuestionnairePage(world.browser, world.section1)
    world.page.visit_url('/questionnaire/entry/%s/section/%s/' % (world.questionnaire.id, world.section1.id))


@step(u'Then I should see an option to add a new grid question to each subsection')
def then_i_should_see_an_option_to_add_a_new_grid_question_to_each_subsection(step):
    assert world.page.is_element_present_by_id('id-create-grid-%s' % world.sub_section.id)


@step(u'When I choose to create a new grid question for a particular subsection')
def when_i_choose_to_create_a_new_grid_question_for_a_particular_subsection(step):
    world.page.click_by_id('id-create-grid-%s' % world.sub_section.id)


@step(u'Then I should see modal allowing me to select the grid options')
def then_i_should_see_modal_allowing_me_to_select_the_grid_options(step):
    world.page.is_text_present('Create Grid in Subsection')


@step(u'When I choose to create a grid with all options shown')
def when_i_choose_to_create_a_grid_with_all_options_shown(step):
    world.page.select('type', 'display_all')


@step(u'When I choose to create an add-more type of grid')
def when_i_choose_to_create_an_add_more_type_of_grid(step):
    world.page.select('type', 'allow_multiples')


@step(u'When I choose to create a hybrid type of grid')
def when_i_choose_to_create_a_hybrid_type_of_grid(step):
    world.page.select('type', 'hybrid')

@step(u'When I select the primary questions and columns for the all options grid')
def when_i_select_the_primary_questions_and_columns(step):
    world.page.select('primary_question', world.grid_question1.id)
    world.page.select_by_id('column-0', world.grid_question2.id)
    sleep(1)
    world.browser.find_by_id('td-0').mouse_over()
    world.page.click_by_id('add-column-0')
    world.browser.find_by_id('td-1').mouse_over()
    world.page.click_by_id('remove-column-1')

@step(u'When I select the primary questions and columns for the add-more grid')
def when_i_select_the_primary_questions_and_columns_for_the_add_more_grid(step):
    when_i_select_the_primary_questions_and_columns(step)

@step(u'And I save my grid')
def and_i_save_my_grid(step):
    world.page.click_by_id('save_grid_button')

@step(u'When I close the modal')
def when_i_close_the_modal(step):
    world.page.click_by_id('close-create-grid-modal')
    sleep(3)
    world.grid = world.grid_question1.group()


@step(u'Then I should see the all-options shown grid created')
def then_i_should_that_grid_created_in_the_subsection_of_my_questionnaire(step):
    assert world.page.is_element_present_by_id('delete-grid-%d' % world.grid.id)
    world.page.is_text_present(world.grid_question1.text)
    for option in world.grid_question1.options.all():
        world.page.is_text_present(option.text)

    world.page.is_text_present(world.grid_question2.text)


@step(u'Then I should see add-more grid created')
def then_i_should_see_the_grid_with_add_more_created(step):
    assert world.page.is_element_present_by_id('delete-grid-%d' % world.grid.id)
    world.page.is_text_present(world.grid_question1.text)
    world.page.is_text_present("Choose One")
    world.page.is_text_present(world.grid_question2.text)
    world.page.is_text_present('Add More')


@step(u'Then I should see the hybrid grid created')
def then_i_should_see_the_hybrid_grid_created(step):
    assert_true(world.page.is_element_present_by_id('delete-grid-%d' % world.grid.id))
    world.page.is_text_present('Add More')
    for option in world.grid_question1.options.all():
        world.page.select('MultiChoice-0-response', option.id)

    for i in range(1, 5):
        world.page.is_text_present(eval("world.grid_question%d" % i).text)


@step(u'When I choose to remove the grid')
def when_i_choose_to_remove_the_grid(step):
    world.page.click_by_id('delete-grid-%d' % world.grid.id)


@step(u'Then I should see a delete grid confirmation prompt')
def then_i_should_see_a_delete_grid_confirmation_prompt(step):
    world.page.is_text_present('Confirm Delete Grid')
    world.page.is_text_present('Are you sure you want to delete this grid?')


@step(u'When I choose to continue with the deletion of the grid')
def when_i_choose_to_continue_with_the_deletion_of_the_grid(step):
    world.page.click_by_id('confirm-delete-grid-%d' % world.grid.id)


@step(u'Then I should see a message that the grid was successfully removed')
def then_i_should_see_a_message_that_the_grid_was_successfully_removed(step):
    world.page.is_text_present('Grid successfully removed from questionnaire')


@step(u'And I should not see the grid in the questionnaire I am editing')
def and_i_should_not_see_the_grid_in_the_questionnaire_i_am_editing(step):
    assert_true(world.page.is_element_not_present_by_id('delete-grid-%d' % world.grid.id))

    for i in range(1, 4):
        world.page.is_text_present(eval("world.grid_question%d" % i).text, status=False)

@step(u'When I choose a theme')
def when_i_select_a_theme(step):
    world.page.select('theme', world.theme.id)

@step(u'When I select the hybrid primary question')
def when_i_select_the_primary_question(step):
    world.page.select('primary_question', world.grid_question1.id)

@step(u'And I select the non-primary question at row "([^"]*)" column "([^"]*)"')
def and_i_select_the_non_primary_question_at_row_group1_column_group1(step, row, column):
    world.hybrid_grid_questions = [[world.grid_question2],
                                   [world.grid_question3, world.grid_question4],
                                   [world.grid_question5]]
    world.page.select_by_id('column_%s_%s'%(row, column), world.hybrid_grid_questions[int(row)][int(column)].id)

@step(u'And I add a new element on the right of row "([^"]*)" column "([^"]*)"')
def and_i_add_a_new_element_on_the_right_of_row_group1_column_group2(step, row, column):
    row_column = (int(row), int(column))
    world.browser.find_by_id('column_%s_%s' % row_column).mouse_over()
    world.page.click_by_id('addElement_%s_%s' % row_column)

@step(u'Then I should not see the same element at row "([^"]*)" column "([^"]*)"')
def then_i_should_not_see_the_same_element_at_row_group1_column_group1(step, row, column):
    world.page.is_element_not_present_by_id('column_%s_%s'%(row, column))

@step(u'And I add a new row from row "([^"]*)" column "([^"]*)"')
def and_i_add_a_new_row_at_group1(step, row, column):
    row_column = (int(row), int(column))
    sleep(1)
    world.browser.find_by_id('column_%s_%s' % row_column).mouse_over()
    world.page.click_by_id('addRow_%s_%s' % row_column)

@step(u'And I delete the element at row "([^"]*)" column "([^"]*)"')
def and_i_delete_the_element_at_row_group1_column_group1(step, row, column):
    row_column = (int(row), int(column))
    sleep(1)
    world.browser.find_by_id('column_%s_%s' % row_column).mouse_over()
    world.page.click_by_id('remove_%s_%s' % (row, column))

@step(u'Then I should not see the element at row "([^"]*)" column "([^"]*)"')
def then_i_should_not_see_the_element_at_row_group1_column_group1(step, row, column):
    world.page.is_element_not_present_by_id('column_%s_%s' % (row, column))

@step(u'When I have a display all grid')
def when_i_have_a_display_all_grid(step):
    world.display_all_group = QuestionGroupFactory(grid=True, display_all=True,
                                                   subsection=world.sub_section, order=1)

    world.display_all_group.question.add(world.grid_question1, world.grid_question2, world.grid_question3)
    QuestionGroupOrder.objects.create(order=1, question=world.grid_question1, question_group=world.display_all_group)
    world.display_all_group.orders.create(order=2, question=world.grid_question2)
    world.display_all_group.orders.create(order=3, question=world.grid_question3)

@step(u'When I click edit the display all grid')
def when_i_click_edit_the_display_all_hybrid_grid(step):
    world.page.click_by_id('edit-grid-%s' % world.display_all_group.id)

@step(u'And I click move first question to the right')
def and_i_click_column_move_group1_question_to_the_left(step):
    sleep(1)
    world.browser.find_by_id('column-0').mouse_over()
    world.page.click_by_id('move-question-%s-right' % world.grid_question2.id)

@step(u'And I choose to move the same question to the left')
def and_i_choose_to_move_the_same_question_further_left(step):
    world.browser.find_by_id('column-1').mouse_over()
    sleep(0.5)
    world.page.click_by_id('move-question-%s-left' % world.grid_question2.id)
    sleep(1)

@step(u'And I click update the grid')
def and_i_click_update_the_grid(step):
    world.page.click_by_id('update_grid_button')

@step(u'Then I should see that the grid was updated successfully')
def then_i_should_see_that_the_grid_was_updated_successfully(step):
    world.page.is_text_present('The grid was updated successfully.')

@step(u'Then I should see it moved to the right')
def then_i_should_see_it_moved_to_the_left(step):
    world.page.assert_questions_ordered_in_edit_modal([world.grid_question3, world.grid_question2])


@step(u'Then I should see it moved back')
def then_i_should_see_it_moved_back(step):
    world.page.assert_questions_ordered_in_edit_modal([world.grid_question2, world.grid_question3])

@step(u'When I close the edit grid modal')
def when_i_close_the_edit_grid_modal(step):
    world.page.click_by_id('close-edit-grid-modal')
    sleep(3)

@step(u'Then I should see the grid questions in their new order')
def then_i_should_see_the_grid_questions_in_their_new_order(step):
    assert world.page.is_element_present_by_id('delete-grid-%d' % world.display_all_group.id)
    world.page.assert_questions_ordered_in_entry([world.grid_question3, world.grid_question2], world.display_all_group)

@step(u'When I have a hybrid grid in that questionnaire')
def when_i_have_a_hybrid_all_grid(step):
    world.hybrid_group = QuestionGroupFactory(grid=True, allow_multiples=True, hybrid=True,
                                              subsection=world.sub_section, order=1)
    world.hybrid_group.question.add(world.grid_question1,  world.grid_question2,  world.grid_question6)
    world.hybrid_group.orders.create(order=1, question=world.grid_question1)
    world.hybrid_group.orders.create(order=2, question=world.grid_question2)
    world.hybrid_group.orders.create(order=3, question=world.grid_question6)

@step(u'When I choose to edit the hybrid grid')
def when_i_click_edit_the_hybrid_grid(step):
    world.page.click_by_id('edit-grid-%s' % world.hybrid_group.id)


@step(u'Then I should see the hybrid grid with its questions in their new order')
def then_i_should_see_the_hybrid_grid_with_its_questions_in_their_new_order(step):
    assert world.page.is_element_present_by_id('delete-grid-%d' % world.hybrid_group.id)
    world.page.assert_questions_ordered_in_hybrid_grid_entry([world.grid_question1, world.grid_question2,
                                                              world.grid_question3, world.grid_question6],
                                                             world.hybrid_group)

@step(u'And I drag the first row to the second row')
def and_i_drag_the_first_row_to_the_second_row(step):
    world.page.move_draggable_id_by_this_number_of_steps('sortable-row-0', 0)
    sleep(3)

@step(u'Then I should see it moved to the second row')
def then_i_should_see_it_moved_to_the_second_row(step):
    sleep(4)
    world.page.assert_row_moved_to(position=1)

@step(u'And I choose to drag the same row to the third row')
def and_i_choose_to_drag_the_same_row_to_the_third_row(step):
    world.page.move_draggable_id_by_this_number_of_steps('sortable-row-1', 2)
    sleep(1)

@step(u'Then I should see it moved to the third row')
def then_i_should_see_it_moved_to_the_third_row(step):
    world.page.assert_row_moved_to(position=2)

@step(u'Then I should see the grid rows in their new order')
def then_i_should_see_the_grid_rows_in_their_new_order(step):
    grid_options = world.browser.find_by_css('.grid-option')
    expected_order_of_options = [world.option1.text, world.option3.text, world.option2.text]
    grid_options_text = map(lambda opt: opt.text, grid_options)
    assert_equals(expected_order_of_options, grid_options_text)

@step(u'And I drag the first hybrid row to the second hybrid row')
def and_i_drag_the_first_hybrid_row_to_the_second_hybrid_row(step):
    world.page.move_draggable_id_by_this_number_of_steps('drag-row-0', 1)
    sleep(3)

@step(u'And I drag the same hybrid row to the third hybrid row')
def and_i_drag_the_first_hybrid_row_to_the_second_hybrid_row(step):
    world.page.move_draggable_id_by_this_number_of_steps('drag-row-0', 1)
    sleep(3)

@step(u'Then I should see the hybrid grid rows in their new order')
def then_i_should_see_the_hybrid_grid_rows_in_their_new_order(step):
    question_texts = world.browser.find_by_css('.question-text')
    expected_order_of_options = [world.grid_question1.text, world.grid_question6.text, world.grid_question2.text]
    grid_question_text = map(lambda opt: opt.text, question_texts)
    assert_equals(expected_order_of_options, grid_question_text)
