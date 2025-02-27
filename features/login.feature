Feature: SauceDemo Login Functionality

  @ui @login
  Scenario Outline: Login as <username>
    Given I am on the SauceDemo login page
    When I enter username "<username>"
    And I enter password "secret_sauce"
    And I click the login button
    And I am on the inventory page

    Examples:
      | username      |
      | <valid_users> |

  @ui @login @locked-user
  Scenario: Login with locked out user
    Given I am on the SauceDemo login page
    When I enter username "locked_out_user"
    And I enter password "secret_sauce"
    And I click the login button
    Then I should see error message "Epic sadface: Sorry, this user has been locked out"

  @ui @auth @negative
  Scenario: Login with incorrect password
    Given I am on the SauceDemo login page
    When I enter username "standard_user"
    And I enter password "wrong_password"
    And I click the login button
    Then I should see error message "Epic sadface: Username and password do not match any user in this service"

  @ui @auth @negative
  Scenario: Login with typo in username
    Given I am on the SauceDemo login page
    When I enter username "standart_user_typo_in_name"
    And I enter password "secret_sauce"
    And I click the login button
    Then I should see error message "Epic sadface: Username and password do not match any user in this service"

  @ui @auth @positive
  Scenario: User can logout successfully
    Given I am on the SauceDemo login page
    When I enter username "standard_user"
    And I enter password "secret_sauce"
    And I click the login button
    And I click on burger menu
    And I click logout
    Then I should see the login page

  @ui @negative
  Scenario: Login with empty password
    Given I am on the SauceDemo login page
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
