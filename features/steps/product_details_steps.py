#  © 2025 Serhii Suzanskyi
#  Open-source and awesome! Use it, modify it, share it—just don’t break it.
#  See LICENSE for details.

from behave import when, then
from page_objects.product_details_page import ProductDetailsPage

@when('I navigate to product "{product_id}" details page')
def step_impl(context, product_id):
    context.product_details_page = ProductDetailsPage(context.driver)
    context.product_details_page.open_product(product_id)

@then('I should see product "{product_name}" with price "{product_price}"')
def step_impl(context, product_name, product_price):
    actual_name = context.product_details_page.get_product_name()
    actual_price = context.product_details_page.get_product_price()
    
    assert actual_name == product_name, \
        f"Expected product name '{product_name}', but got '{actual_name}'"
    assert actual_price == product_price, \
        f"Expected price '{product_price}', but got '{actual_price}'"

@when('I add the current product to cart')
def step_impl(context):
    context.product_details_page.add_to_cart()

@when('I return to products page')
def step_impl(context):
    context.product_details_page.click_back_to_products() 