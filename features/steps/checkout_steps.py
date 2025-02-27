#  © 2025 Serhii Suzanskyi
#  Open-source and awesome! Use it, modify it, share it—just don’t break it.
#  See LICENSE for details.

from behave import when, then, step
from page_objects.checkout_page import CheckoutPage
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
    """
    Verify order summary from table:
    | Item total | $39.98 |
    | Tax        | $3.20  |
    | Total      | $43.18 |
    """
    expected_values = {row[0]: Decimal(row[1].replace('$', '')) for row in context.table}
    
    actual_item_total = context.checkout_page.get_item_total()
    actual_tax = context.checkout_page.get_tax()
    actual_total = context.checkout_page.get_total()

    assert actual_item_total == expected_values['Item total'], \
        f"Expected item total ${expected_values['Item total']}, but got ${actual_item_total}"
    
    assert actual_tax == expected_values['Tax'], \
        f"Expected tax ${expected_values['Tax']}, but got ${actual_tax}"
    
    assert actual_total == expected_values['Total'], \
        f"Expected total ${expected_values['Total']}, but got ${actual_total}"

    # Verify the calculation
    calculated_total = actual_item_total + actual_tax
    assert calculated_total == actual_total, \
        f"Total amount ${actual_total} doesn't match calculated total ${calculated_total}"

@then('I should see the order confirmation')
def step_impl(context):
    assert "checkout-complete" in context.driver.current_url, "Not on order confirmation page"


@step('I enter first name "Serhii"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And I enter first name "Serhii"')


@step('I enter last name "Suzanskyi"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And I enter last name "Suzanskyi"')


@step('I enter postal code "5701NR"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And I enter postal code "5701NR"')