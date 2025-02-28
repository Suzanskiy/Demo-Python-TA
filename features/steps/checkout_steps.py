#  © 2025 Serhii Suzanskyi
#  Open-source and awesome! Use it, modify it, share it—just don't break it.
#  See LICENSE for details.

from behave import when, then, step
from page_objects.checkout_page import CheckoutPage
from page_objects.order_complete_page import OrderCompletePage
from page_objects.inventory_page import InventoryPage

from decimal import Decimal

@when('I click checkout')
def step_impl(context):
    context.cart_page.click_checkout()
    context.checkout_page = CheckoutPage(context.driver)
    assert context.checkout_page.is_on_checkout_page()

@when('I click continue')
def step_impl(context):
    context.checkout_page.click_continue()

@when('I click finish')
def step_impl(context):
    context.checkout_page.click_finish()

@then('the order summary should show')
def step_impl(context):
    expected_values = {row[0]: Decimal(row[1].replace('$', '')) for row in context.table}

    actual_values = {
        "Item total": context.checkout_page.get_item_total(),
        "Tax": context.checkout_page.get_tax(),
        "Total": context.checkout_page.get_total()
    }

    errors = []  # Collect all mismatches

    for key, expected in expected_values.items():
        actual = actual_values[key]
        if actual != expected:
            errors.append(f"{key} mismatch: expected ${expected}, but got ${actual}")

    # Verify the total calculation
    calculated_total = actual_values["Item total"] + actual_values["Tax"]
    if calculated_total != actual_values["Total"]:
        errors.append(f"Total amount mismatch: expected ${calculated_total}, but got ${actual_values['Total']}")

    if errors:
        raise AssertionError("\n".join(errors))  # Raise an error with all mismatches

@then('I should see the order confirmation page')
def step_impl(context):
    context.order_complete_page = OrderCompletePage(context.driver)
    assert context.order_complete_page.is_on_complete_page(), "Not on order confirmation page"
    assert context.order_complete_page.is_order_complete_container_displayed(), \
        "Order complete container is not displayed"

@then('the confirmation header should be "{expected_header}"')
def step_impl(context, expected_header):
    actual_header = context.order_complete_page.get_confirmation_header()
    assert actual_header == expected_header, \
        f"Expected header '{expected_header}', but got '{actual_header}'"

@then('the confirmation text should contain "{expected_text}"')
def step_impl(context, expected_text):
    actual_text = context.order_complete_page.get_confirmation_text()
    assert expected_text in actual_text, \
        f"Expected text to contain '{expected_text}', but got '{actual_text}'"

@when('I click back home')
def step_impl(context):
    context.order_complete_page.click_back_home()

@then('I should be back on the inventory page')
def step_impl(context):
    context.inventory_page = InventoryPage(context.driver)
    assert context.inventory_page.is_on_inventory_page(), "Not back on inventory page"

@step('I enter first name "{name}"')
def step_impl(context, name):
    context.checkout_page.enter_name(name)

@step('I enter last name "{name}"')
def step_impl(context, name):
    context.checkout_page.enter_last_name(name)

@step('I enter postal code "{code}"')
def step_impl(context, code):
    context.checkout_page.enter_postal_code(code)