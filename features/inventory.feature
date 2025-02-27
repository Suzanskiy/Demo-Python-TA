Feature: Inventory Page Functionality

  @ui @inventory
  Scenario Outline: Verify inventory functionality as <username>
    Given I am logged in as "<username>"
    When I am on the inventory page
    Then I should see 6 products listed
    And each product should have correct details from test data
    And each product should have an "Add to cart" button

   Examples:
      | username    |
      | <all_users> |

  @ui @inventory @positive
  Scenario Outline: Add product to cart - <username>
    Given I am logged in as "<username>"
    When I am on the inventory page
    When I add "Sauce Labs Backpack" to the cart
    Then the cart badge should show "1"
    And the button text should change to "Remove"
       Examples:
      | username    |
      | <valid_users> |


  @ui @inventory
  Scenario Outline: Add multiple products to cart for <username>
    Given I am logged in as "<username>"
    When I am on the inventory page
    When I add "Sauce Labs Backpack" to the cart
    When I add "Sauce Labs Bike Light" to the cart
    When I add "Sauce Labs Bolt T-Shirt" to the cart
    Then the cart badge should show "3"
    Examples:
      | username    |
      | <valid_users> |


  @ui @inventory
  Scenario Outline: Remove product from cart for <username>
    Given I am logged in as "<username>"
    When I am on the inventory page
    When I add "Sauce Labs Backpack" to the cart
    And I click Remove for "Sauce Labs Backpack"
    Then the cart badge should not be visible
    And the button text should change to "Add to cart"
    Examples:
      | username    |
      | <valid_users> |