Feature: Grid positioning

  Scenario: Move grid
    Given I am logged in as a global admin
    And I have a questionnaire with a grid
    And I am editing that questionnaire
    Then I should see options to move the grid position up or down
    When I select the option to move the grid up
    Then I should see a message that it cannot be moved 'up'
    When I select the option to move the grid down
    Then I should see a message that it cannot be moved 'down'

    Given there are other questions in that subsection
    And I am editing that questionnaire
    Then I should see the questions in the grid numbered as '1.1.1' '1.1.2' '1.1.3'
    When I select the option to move the grid down
    Then I should see the questions in the grid numbered as '1.2.1' '1.2.2' '1.2.3'
    When I select the option to move the grid up
    Then I should see the questions in the grid numbered as '1.1.1' '1.1.2' '1.1.3'