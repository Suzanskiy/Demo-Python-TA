#  © 2025 Serhii Suzanskyi
#  Open-source and awesome! Use it, modify it, share it—just don’t break it.
#  See LICENSE for details.

from behave import when, then
from page_objects.inventory_page import InventoryPage

@when('I sort products by "{sort_option}"')
def step_impl(context, sort_option):
    context.inventory_page.sort_products(sort_option)
    # Store the sorted products for later verification
    context.sorted_products = context.inventory_page.get_product_names_list()

@then('products should be sorted alphabetically ascending')
def step_impl(context):
    products = context.sorted_products
    sorted_products = sorted(products)
    assert products == sorted_products, \
        f"Products are not sorted A-Z. Current order: {products}"

@then('products should be sorted alphabetically descending')
def step_impl(context):
    products = context.sorted_products
    sorted_products = sorted(products, reverse=True)
    assert products == sorted_products, \
        f"Products are not sorted Z-A. Current order: {products}"

@then('the first product should be "{product_name}"')
def step_impl(context, product_name):
    first_product = context.sorted_products[0]
    assert first_product == product_name, \
        f"Expected first product to be '{product_name}', but got '{first_product}'"

@then('the last product should be "{product_name}"')
def step_impl(context, product_name):
    last_product = context.sorted_products[-1]
    assert last_product == product_name, \
        f"Expected last product to be '{product_name}', but got '{last_product}'" 