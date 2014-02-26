Feature: Manage JRF

    Scenario: Global admin view
        Given I am logged in as a global admin
        Then I should see manage JRF, users, question bank, extract and attachments links
        Given I have four finalised questionnaires
        And I have two draft questionnaires for two years
        And I visit the manage JRF page
        Then I should see a list of the three most recent finalised questionnaires
        And I should see a list of draft questionnaires
        
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