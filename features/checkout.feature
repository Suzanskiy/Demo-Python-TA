Feature: Checkout Process

  Background:
    Given I am logged in as "standard_user"
    And I am on the inventory page

  # AC1 checkout via inventory page
  @ui @checkout
  Scenario: Complete checkout process with multiple items
    When I add "Sauce Labs Backpack" to the cart
    And I add "Sauce Labs Bike Light" to the cart
    And I click on the shopping cart
    And I click checkout
    And I enter first name "Serhii"
    And I enter last name "Suzanskyi"
    And I enter postal code "5701NR"
    And I click continue
    Then the order summary should show:
      | Item total | $39.98 |
      | Tax        | $3.20  |
      | Total      | $43.18 |
    When I click finish
    Then I should see the order confirmation page
    And the confirmation header should be "Thank you for your order!"
    And the confirmation text should contain "Your order has been dispatched, and will arrive just as fast as the pony can get there!"
    When I click back home
    Then I should be back on the inventory page

    # AC2 checkout via product page
  @ui @checkout @product-details
  Scenario: Checkout process through product details pages
    When I navigate to product "4" details page
    Then I should see product "Sauce Labs Backpack" with price "$29.99"
    When I add the current product to cart
    And I navigate to product "0" details page
    Then I should see product "Sauce Labs Bike Light" with price "$9.99"
    When I add the current product to cart
    And I click on the shopping cart
    Then I should see 2 items in the cart
    When I click checkout
    And I enter first name "Serhii"
    And I enter last name "Suzanskyi"
    And I enter postal code "5701NR"
    And I click continue
    Then the order summary should show:
      | Item total | $39.98 |
      | Tax        | $3.20  |
      | Total      | $43.18 |
    When I click finish
    Then I should see the order confirmation page
    And the confirmation header should be "Thank you for your order!" 