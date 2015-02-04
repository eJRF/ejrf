Feature: Grid Creation

  Background:
    Given I am logged in as a global admin
    And I have both simple and primary questions in my Question Bank
    And I have a questionnaire with sections and with subsections
    And I am editing that questionnaire
    Then I should see an option to add a new grid question to each subsection
    When I choose to create a new grid question for a particular subsection
    Then I should see modal allowing me to select the grid options

  Scenario: Create Grid with All Options Shown
    When I choose to create a grid with all options shown
    When I choose a theme
    When I select the primary questions and columns for the all options grid
    And I save my grid
    When I close the modal
    Then I should see the all-options shown grid created
    When I choose to remove the grid
    Then I should see a delete grid confirmation prompt
    When I choose to continue with the deletion of the grid
    Then I should see a message that the grid was successfully removed
    And I should not see the grid in the questionnaire I am editing

  Scenario: Create Grid with add-more
    When I choose to create an add-more type of grid
    When I choose a theme
    When I select the primary questions and columns for the add-more grid
    And I save my grid
    When I close the modal
    Then I should see add-more grid created

  Scenario: Create hybrid grid
    When I choose to create a hybrid type of grid
    When I choose a theme
    When I select the hybrid primary question
    And I select the non-primary question at row "0" column "0"
    And I add a new row from row "0" column "0"
    And I select the non-primary question at row "1" column "0"
    And I add a new element on the right of row "1" column "0"
    And I select the non-primary question at row "1" column "1"
    And I add a new element on the right of row "1" column "1"
    And I delete the element at row "1" column "1"
    Then I should not see the same element at row "1" column "1"
    And I select the non-primary question at row "1" column "1"
    And I add a new row from row "1" column "1"
    And I select the non-primary question at row "2" column "0"
    And I save my grid
    When I close the modal
    Then I should see the hybrid grid created