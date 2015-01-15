Feature: Manage JRF

  @WIP
  Scenario: Global admin viewing and Editing Questionnaires (Names)
    Given I am logged in as a global admin
    Then I should see manage JRF, users, question bank, extract links
    Given I have four finalised questionnaires
    And I have two draft questionnaires for two years
    And I visit the manage JRF page
    Then I should see a list of the three most recent finalised questionnaires
    And I should see a list of draft questionnaires
    When I choose the option to edit the name of a questionnaire
    Then I should see modal with the questionnaires current name
    When I update the name of the questionnaire and save my changes
    Then I should see a message that questionnaire was updated
    And I should see the questionnaire with its new name

    Scenario: Viewing older finalised questionnaires
        Given I am logged in as a global admin
        Given I have four finalised questionnaires
        And I visit the manage JRF page
        Then I should see a list of the three most recent finalised questionnaires
        And When I click Older
        Then I should also see the fourth finalised questionnaire

    Scenario: Duplicate a Questionnaire
        Given I am logged in as a global admin
        And I have four finalised questionnaires
        And I visit the manage JRF page
        When I choose to create a new questionnaire
        Then I should see options for selecting a finalized questionnaire and a reporting year
        When I choose to duplicate the questionnaire without specifying a questionnaire and reporting year
        Then I should a validation error message
        When I select a finalized questionnaire and a reporting year
        And I give it a new name
        When I choose to duplicate the questionnaire
        Then I should see a message that the questionnaire was duplicated successfully
        When I visit the manage JRF page
        Then I should see the new questionnaire listed

    Scenario: Global Admin locking and unlocking a Core Questionnaire
        Given I am a logged-in Global Admin
        And I have draft and finalised core questionnaires
        And I visit the manage JRF page
        Then I should see an option to lock each draft Core Questionnaire
        And I should see an option to unlock each finalised Core Questionnaire
        When I lock a draft Core Questionnaire
        Then it should now have an option to unlock it
        When I unlock a finalised Core Questionnaire
        Then it should now have an option to lock it
        When I click on a Draft Core Questionnaire
        Then it should open in an edit view
        When I visit the manage JRF page
        And I click on a Finalised Core Questionnaire
        Then it should open in a preview mode

    Scenario: Publish core questionnaire to regional admins
        Given I am logged in as a global admin
        And I have two finalised questionnaires
        When I visit the manage JRF page
        And I see finalized questionnaires
        Then I should see an option to send to regions on each of the finalized questionnaires

    Scenario: Send finalized core questionnaire to two regions
        Given I am logged in as a global admin
        And I have two finalised questionnaires
        And I visit the manage JRF page
        And I see finalized questionnaires
        When I choose option to send core questionnaire to regions
        Then I should see an interface to choose the regions to which to publish the finalised Core Questionnaire
        And I select two regions to which to publish the finalised Core Questionnaire
        When I click publish button
        And I should be able to confirm that the Core Questionnaire is published to the regions I selected
        And I should be able to confirm that the regions to which I published the questionnaire is not on the list

    Scenario: Global admin approves regional questionnaire
        Given I am logged in as a global admin
        And I have regions and countries
        And I have a finalised regional questionnaire
        When I visit the manage JRF page
        When I click that regional questionnaire
        Then it should open in a preview mode
        When I visit the manage JRF page
        When I select to approve the regional questionnaire
        Then I should see a confirmation prompt to approve the questionnaire
        When I confirm the questionnaire approval
        Then I should see a message that the questionnaire was approved
        And I should see a new status indicating that the questionnaire was approved
        And there should no longer be an option to approve the questionnaire

    Scenario: Global admin archives a core questionnaire
        Given I am logged in as a global admin
        And I have regions and countries
        And I have "1" "finalized" core questionnaire
        When I visit the manage JRF page
        When I click "archive" button on that core questionnaire
        When I confirm "archive" the questionnaire
        Then I should see the questionnaire "archived"
        When I click on the "archived" questionnaire
        Then I should view it in preview mode


    Scenario: Global admin deletes a core questionnaire
        Given I am logged in as a global admin
        And I have regions and countries
        And I have "2" "draft" core questionnaire
        When I visit the manage JRF page
        When I click "delete" button on that core questionnaire
        When I confirm "delete" the questionnaire
        Then I should see the questionnaire "deleted"