@api
Feature: ReqRes API Users Endpoint

  # AC1 1. Retrieve a list of users
  @users
  Scenario: Retrieve users from page 2
    When I send GET request to "users" and "page=2"
    Then the response status code should be 200
    And the response should match "users_page_2.json"
    And the response should have the following structure:
      | field       | value |
      | page        | 2     |
      | per_page    | 6     |
      | total       | 12    |
      | total_pages | 2     |
    And each user in response should have required fields:
      | id         |
      | email      |
      | first_name |
      | last_name  |
      | avatar     |

    #AC2 Perform a successful login
  @login
  Scenario: Successful login with valid credentials
    When I send POST request to "login" with data from "login.json"
    Then the response status code should be 200
    And the response should contain "token" field
    And the token should not be empty

    #AC3 Perform an update using PUT
  @update @put
  Scenario: Update user using PUT method
    When I send PUT request to "users/2" with data from "update_user.json"
    Then the response status code should be 200
    And the response should contain fields:
      | name | morpheus      |
      | job  | zion resident |
    And the response should contain "updatedAt" field
    And the "updatedAt" should be a valid timestamp

  #AC3 Perform an update using PATCH
  @update @patch
  Scenario: Update user using PATCH method
    When I send PATCH request to "users/2" with data from "update_user.json"
    Then the response status code should be 200
    And the response should contain fields:
      | name | morpheus      |
      | job  | zion resident |
    And the response should contain "updatedAt" field
    And the "updatedAt" should be a valid timestamp

    #AC4 Perform a delete
    @delete
  Scenario: Delete user successfully
    When I send DELETE request to "users/2"
    Then the response status code should be 204
    And the response body should be empty

     #AC5 Run 2 negative scenarios
  @login @negative
  Scenario: Failed login with missing password
    When I send POST request to "login" with data:
      | email    | eve.holt@reqres.in |
      | password |                    |
    Then the response status code should be 400
    And the response should contain "error" field
    And the "error" field should contain "Missing email or username"

  @login @negative
  Scenario: Failed login with unregistered email
    When I send POST request to "login" with data:
      | email    | serhii_is_good_candidate@please_hire_him.com |
      | password | real_cool_guy            |
    Then the response status code should be 400
    And the response should contain "error" field

#last AC I'm already tired but still enthusiastic
  @delayed
  Scenario Outline: Get users list with different delay times
    When I send GET request to "users" with delay of <delay> seconds
    Then the response status code should be 200
    And the response should match "users_delayed.json"
    And the response time should be less than <max_time> seconds

    Examples:
      | delay | max_time |
      | 1     | 2        |
      | 2     | 3        |
      | 3     | 4        |