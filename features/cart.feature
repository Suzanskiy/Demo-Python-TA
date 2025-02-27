Feature: Shopping Cart Functionality

  @ui @cart
  Scenario Outline: Add and remove items from cart as <username>
    Given I am logged in as "<username>"
    And I am on the inventory page
    When I add "Sauce Labs Backpack" to the cart
    And I add "Sauce Labs Bike Light" to the cart
    And I click on the shopping cart
    Then I should see 2 items in the cart
    And the cart should contain "Sauce Labs Bike Light"
    And the cart should contain "Sauce Labs Backpack"
    And the total price should be "$39.98"

    Examples:
      | username    |
      | <all_users> |
