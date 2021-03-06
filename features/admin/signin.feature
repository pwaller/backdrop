@use_admin_client
Feature: Sign in

  Scenario: Show signed in user name
    Given I am logged in as "Max" with email "test@example.com"
    When I go to "/"
    Then I should get a "cache-control" header of "private, must-revalidate"
    And I should see the text "Signed in as Max"

  Scenario: Show signed in list of actions
    Given I am logged in as "Alex" with email "test@example.com"
    And I can upload to "my_bucket"
    When I go to "/"
    Then I should see the text "Upload a CSV to the my_bucket bucket"
    And I should get a "x-frame-options" header of "SAMEORIGIN"
