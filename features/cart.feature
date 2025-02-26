Feature: Shopping Cart Functionality

  Background:
    Given I am logged in as "standard_user"
    And I am on the inventory page

  @ui @cart
  Scenario: Add multiple items to cart and verify total price
    When I add "Sauce Labs Backpack" to the cart
    And I add "Sauce Labs Bike Light" to the cart
    And I click on the shopping cart
    Then I should see 2 items in the cart
    And the cart should contain "Sauce Labs Bike Light"
    And the cart should contain "Sauce Labs Backpack"
    And the total price should be "$39.98"
