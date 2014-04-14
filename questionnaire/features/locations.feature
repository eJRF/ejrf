Feature: Location types
    Background:
      Given I am a logged-in Global Admin

    Scenario: List Regions
      And I have two regions
      And I visit the list regions page
      Then I should see the list of regions
      When I click on the first region name
      Then I should see the list country page

    Scenario: List Countries
      Given I have two countries in a region
      And I visit the list countries page in that region
      Then I should see the list of countries in that region
