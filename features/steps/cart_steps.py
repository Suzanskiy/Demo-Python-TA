#  © 2025 Serhii Suzanskyi
#  Open-source and awesome! Use it, modify it, share it—just don’t break it.
#  See LICENSE for details.

from behave import when, then, step
from page_objects.cart_page import CartPage
from decimal import Decimal

@when('I click on the shopping cart')
def step_impl(context):
    context.cart_page = CartPage(context.driver)
    context.inventory_page.find_element(context.inventory_page.LOCATORS["cart_button"]).click()
    assert context.cart_page.is_on_cart_page(), "Not on cart page"

@then('I should see {count:d} items in the cart')
def step_impl(context, count):
    items = context.cart_page.get_cart_items()
    assert len(items) == count, f"Expected {count} items in cart, but found {len(items)}"

@then('the total price should be "{expected_total}"')
def step_impl(context, expected_total):
    actual_total = context.cart_page.get_total_price()
    expected = Decimal(expected_total.replace("$", ""))
    assert Decimal(str(actual_total)) == expected, \
        f"Expected total price {expected_total}, but got ${actual_total:.2f}"

@when('I remove "{product_name}" from the cart')
def step_impl(context, product_name):
    context.cart_page.remove_item(product_name)

@then('the cart should be empty')
def step_impl(context):
    items = context.cart_page.get_cart_items()
    assert len(items) == 0, f"Expected empty cart, but found {len(items)} items"

@step("the cart should contain {item}")
def step_impl(context, item):
    item = item.strip('"')  # Remove unnecessary quotes
    elements = context.cart_page.get_cart_items()
    names = [element.text.strip() for element in elements]  # Extract and clean text

    assert item in names, f"Expected item '{item}', but found {names}"