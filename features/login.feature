Feature: SauceDemo Login Functionality

  Background: 
    Given I am on the SauceDemo login page

  @ui @auth @positive
  Scenario: Successful login with standard user
    When I enter username "standard_user"
    And I enter password "secret_sauce"
    And I click the login button
    Then I should be successfully logged in
    And I should see the inventory page

  @ui @auth @negative
  Scenario: Login with incorrect password
    When I enter username "standard_user"
    And I enter password "wrong_password"
    And I click the login button
    Then I should see error message "Epic sadface: Username and password do not match any user in this service"

  @ui @auth @negative
  Scenario: Login with typo in username
    When I enter username "standart_user_typo_in_name"
    And I enter password "secret_sauce"
    And I click the login button
    Then I should see error message "Epic sadface: Username and password do not match any user in this service"

  @ui @auth @positive
  Scenario: User can logout successfully
    When I enter username "standard_user"
    And I enter password "secret_sauce"
    And I click the login button
    And I click on burger menu
    And I click logout
    Then I should see the login page

  @ui @negative
  Scenario: Login with empty password
    When I enter username "standard_user"
    And I enter empty password
    And I click the login button
    Then I should see error message "Epic sadface: Password is required"

  @ui @negative
  Scenario: Login with empty username
    When I enter empty username
    And I enter password "secret_sauce"
    And I click the login button
    Then I should see error message "Epic sadface: Username is required"
