Feature: Product Sorting Functionality

  Background:
    Given I am logged in as "standard_user"
    And I am on the inventory page

  @ui @sorting
  Scenario: Sort products from A to Z
    When I sort products by "az"
    Then products should be sorted alphabetically ascending
    And the first product should be "Sauce Labs Backpack"
    And the last product should be "Test.allTheThings() T-Shirt (Red)"

  @ui @sorting
  Scenario: Sort products from Z to A
    When I sort products by "za"
    Then products should be sorted alphabetically descending
    And the first product should be "Test.allTheThings() T-Shirt (Red)"
    And the last product should be "Sauce Labs Backpack" 