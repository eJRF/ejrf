Feature: Skip Rules

  Scenario: Questions and subsections are displayed when creating skip rules
    Given I am logged in as a global admin
    And I have a questionnaire with sections and subsections
    And I have questions and responses in the correct section
    And I visit that questionnaires section page
    And I click to add a skip rule
    Then I should see options to add skip rules for skipping 'Question'
    Then I should see options to add skip rules for skipping 'Subsection'
    When I select to add skip rules for skipping questions
    Then I should see the questions in that subsection listed for skipping
    When I select to add skip rules for skipping subsections
    Then I should see the subsections in that section listed for skipping

  @WIP
  Scenario: Create and view skip rule
    Given I am logged in as a global admin
    And I have a questionnaire with sections and subsections
    And I have questions and responses in the correct section
    And I visit that questionnaires section page
    And I click to add a skip rule
    And I choose to see existing skip rules
    Then I should see '0' existing skip rules
    When I create a new question skip rule
    Then I should see '1' existing skip rules
    When I create a new subsection skip rule
    Then I should see '2' existing skip rules

  Scenario: Skip rules are applied when responses are selected
    Given I have a questionnaire with sections and subsections
    And I have questions and responses in the correct section
    And I have skip rules applied to a question
    And I have skip rules applied to a subsection
    Given I am logged in as a data submitter
    And the questionnaire has been published to the data submitter
    And I navigate to the section of the questionnaire to be filled in
    Then I should see the all the questions and subsections in that section
    When I select a response that skips a question and a subsection
    Then that question should no longer be displayed
    And that subsection should no longer be displayed

  Scenario: Delete skip rules
    Given I have a questionnaire with sections and subsections
    And I have questions and responses in the correct section
    And I have skip rules applied to a question
    Given I am logged in as a global admin
    And I visit that questionnaires section page
    And I click to add a skip rule
    And I choose to see existing skip rules
    Then I should see an option to delete skip rules
    When I have selected delete
    Then I should see the rule disappear and a message that the skip rule was successfully deleted
    Then I should see '0' existing skip rules"

  Scenario: Create Hybrid grid skip rule
    Given I am logged in as a global admin
    And I have a questionnaire with sections and subsections
    And I have a hybrid group with multichoice question and other questions
    And I visit that questionnaires section page
    And I click to add a grid skip rule
    And I choose to see existing grid skip rules
    Then I should see '0' existing grid skip rules
    When I click create a new hybrid grid question skip rule
    And I fill in the grid rule form
    And I click save rule
    And I choose to see existing grid skip rules
    Then I should see '1' existing grid skip rules

  Scenario: Regional admin creates, views and deletes skip rule
    Given that I am logged in as a regional admin
    And there is questionnaire for my region
    And I have core and regional questions assigned to the questionnaire
    And I am editing that questionnaire
    Then I should see options to add skip rules
    When I select the option to add skip rules to a subsection
    And I view existing skip rules
    Then I should see '0' existing skip rules
    When I create a new question skip rule
    Then I should see '1' existing skip rules
    When I create a new regional subsection skip rule
    Then I should see '2' existing skip rules
    When I choose to see existing skip rules
    Then I should see an option to delete skip rules
    When I have selected delete
    Then I should see the rule disappear and a message that the skip rule was successfully deleted
    Then I should see '1' existing skip rules

  Scenario: Skip rules are deleted when questions are unassigned
    Given I have a questionnaire with sections and subsections
    And I have questions and responses in the correct section
    And I have skip rules applied to a question
    And I have skip rules applied to another question
    And I have skip rules applied to a subsection
    Given I am logged in as a global admin
    And I visit that questionnaires section page
    And I click to add a skip rule
    And I choose to see existing skip rules
    Then I should see '3' existing skip rules"

    When I un-assign a question with a skip rule
    And I click to add a skip rule
    Then I should see '2' existing skip rules"
    When I delete a subsection with a skip rule
    And I click to add a skip rule
    Then I should see '1' existing skip rules"
    When I un-assign the root question to a skip rule
    And I click to add a skip rule
    Then I should see '0' existing skip rules"

  Scenario: Turn off cells in display all grid
    Given I am logged in as a global admin
    And I have a questionnaire with a grid
    And I am editing that questionnaire
    Then I should see the option to add skip rules to the grid
    When I select the option to add skip rules to the grid
    And I choose to see existing skip rules
    Then I should see '0' existing skip rules"
    When I specify a cell to skip in the grid
    Then I should see '1' existing skip rules"
    And that cell should be disabled