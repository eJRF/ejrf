Feature: Subsection feature

  Scenario: Create a subsection
    Given I am logged in as a global admin
    And I have a questionnaire with sections and subsections
    And I visit that questionnaires section page
    And I click add new subsection link
    Then I should see a new subsection modal
    When i fill in the subsection data
    And I save the subsection
    Then I should see the subsection I just created

  Scenario: Update Subsection in Core Questionnaire
    Given I am logged in as a global admin
    And I have a questionnaire with sections and subsections
    And I visit that questionnaires section page
    And I choose to update a subsection
    Then I should see an edit subsection modal
    When I update the subsection details
    And I save the changes to the subsection
    Then I should see a message that the subsection was updated
    And I should see the changes I made to the subsection in the questionnaire

  Scenario: Delete Regional Subsection from a regional Questionnaire
    Given I am a Regional Admin
    And I have a questionnaire for my region with sections and subsections
    And I have regional questions already assigned to my questionnaire
    And I login the regional user
    When I open that regional questionnaire for editing
    And I choose to delete one of the sub sections from the questionnaire
    Then I should see a delete subsection confirmation message
    When I confirm my intention to delete that subsection
    Then I should see a message that the sub-section was deleted
    And the sub section should no longer appear in the Questionnaire

  Scenario: Create Regional subsection
    Given I am a Regional Admin
    And I have a questionnaire for my region with sections and subsections
    And I have regional questions already assigned to my questionnaire
    And I login the regional user
    When I open that regional questionnaire for editing
    And I click add new subsection link
    Then I should see a new subsection modal
    When i fill in the subsection data
    And I save the subsection
    Then I should see the subsection I just created

  Scenario: Update Subsection in Regional Questionnaire
    Given that I am logged in as a regional admin
    And I have a questionnaire in a region with sections and subsections
    And I visit that questionnaires section page
    Then I should not see core subsection edit link
    When I click the edit link for regional subsection
    Then I should see an edit subsection modal
    When I update the subsection details
    And I save the changes to the subsection
    Then I should see a success message that the subsection was updated
    And I should see those changes to the regional subsection in the questionnaire

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