Feature: Login Functionality
  As a user
  I want to be able to login to the website
  So that I can access secure content

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter "$valid_user.username" as username
    And I enter "$valid_user.password" as password
    And I click the login button
    Then I should be logged in successfully
    And I should see the secure area page
    
  Scenario: Failed login with invalid credentials
    Given I am on the login page
    When I enter "$invalid_user.username" as username
    And I enter "$invalid_user.password" as password
    And I click the login button
    Then I should see an error message
    And The error message should contain "Your username is invalid!" 