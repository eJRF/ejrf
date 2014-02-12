Feature: Support document upload
  Scenario: Upload PDF file
   Given I am logged in as a data submitter
   And I have a questionnaire with sections and subsections
   And I have a pdf document
   And I visit the attachments page
   Then I should see the upload form
   When I select a file to upload 
   And I click upload button
   Then I should see the file was uploaded successfully
   And I clean up the files
   And I should be able to download the file

  Scenario: Upload Unacceptable File Extension
    Given I am logged in as a data submitter
    And I have a questionnaire with sections and subsections
    And I have a zip file
    And I visit the attachments page
    Then I should see the upload form
    When I select a file to upload
    And I click upload button
    Then I should see an error that the file type is not supported
    And I clean up the files

  Scenario: Delete attachment
    Given I am logged in as a data submitter
    And I have a questionnaire with sections and subsections
    And I have an attached file
    And I visit the attachments page
    And I click delete button next to that file
    Then I should see a warning dialog
    When I click confirm
    Then I should see that file was deleted