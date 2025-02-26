Feature: Inventory Page Functionality

  Background:
    Given I am logged in as "standard_user"
    And I am on the inventory page

  @ui @inventory
  Scenario: Verify all products are displayed correctly
    Then I should see 6 products listed
    And each product should have correct details from test data
    And each product should have an "Add to cart" button

  @ui @inventory
  Scenario: Add product to cart
    When I add "Sauce Labs Backpack" to the cart
    Then the cart badge should show "1"
    And the button text should change to "Remove"

  @ui @inventory
  Scenario: Add multiple products to cart
    When I add the following products to cart:
      | Sauce Labs Backpack     |
      | Sauce Labs Bike Light   |
      | Sauce Labs Bolt T-Shirt |
    Then the cart badge should show "3"

  @ui @inventory
  Scenario: Remove product from cart
    When I add "Sauce Labs Backpack" to the cart
    And I click Remove for "Sauce Labs Backpack"
    Then the cart badge should not be visible
    And the button text should change to "Add to cart" 