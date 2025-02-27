#  © 2025 Serhii Suzanskyi
#  Open-source and awesome! Use it, modify it, share it—just don’t break it.
#  See LICENSE for details.

import json
from behave import when, then, step
from page_objects.inventory_page import InventoryPage

# Load test data
with open('test_data/products.json') as f:
    PRODUCT_DATA = json.load(f)

@step('I am on the inventory page')
def step_impl(context):
    context.inventory_page = InventoryPage(context.driver)
    context.inventory_page.wait_for_page_load()
    assert context.inventory_page.is_on_inventory_page(), \
        f"Expected to be on the Inventory page, but currently on: {context.driver.current_url}"

@then('I should see {count:d} products listed')
def step_impl(context, count):
    actual_count = context.inventory_page.get_product_count()
    assert actual_count == count, f"Expected {count} products, but found {actual_count}"

@then('each product should have correct details from test data')
def step_impl(context):
    product_names = context.inventory_page.get_product_details()
    errors = []  # Collect all mismatches

    for i, (name, description, price, image) in enumerate(product_names):
        product = PRODUCT_DATA["products"][i]

        if product["name"] != name.text:
            errors.append(f"Product name mismatch for {i}: expected '{product['name']}', got '{name.text}'")

        if product["description"] != description.text:
            errors.append(f"Description mismatch for {product['name']}: expected '{product['description']}', got '{description.text}'")

        expected_price = f"${product['price']}"
        if expected_price != price.text:
            errors.append(f"Price mismatch for {product['name']}: expected '{expected_price}', got '{price.text}'")

        if product['image_url'] not in image.get_attribute("src"):
            errors.append(f"Image URL mismatch for {product['name']}: expected part of '{product['image_url']}', got '{image.get_attribute('src')}'")

    if errors:
        raise AssertionError("\n".join(errors))  # Raise AssertionError with full list


@then('each product should have an "Add to cart" button')
def step_impl(context):
    buttons = context.inventory_page.get_add_to_cart_buttons()
    product_count = len(context.inventory_page.get_product_names())
    assert len(buttons) == product_count, "Not all products have Add to cart button"

@step('I add "{product_name}" to the cart')
def step_impl(context, product_name):
    product_data = next(p for p in PRODUCT_DATA["products"] if p["name"] == product_name)
    context.inventory_page.add_to_cart(product_data["id"])


@then('the cart badge should show "{count}"')
def step_impl(context, count):
    actual_count = context.inventory_page.get_cart_badge_count()
    assert actual_count == int(count), f"Expected cart count {count}, but got {actual_count}"

@then('the button text should change to "{text}"')
def step_impl(context, text):
    buttons = context.inventory_page.get_add_to_cart_buttons()
    res = lambda driver: any(button.text.strip() == text for button in buttons)
    assert any(button.text.strip() == text for button in buttons), f"No button changed to '{text}'"

@when('I click Remove for "{product_name}"')
def step_impl(context, product_name):
    product_data = next(p for p in PRODUCT_DATA["products"] if p["name"] == product_name)
    context.inventory_page.remove_from_cart(product_data["id"])

@then('the cart badge should not be visible')
def step_impl(context):
    badges = context.inventory_page.get_cart_badge_count()
    assert badges == 0, "Cart badge is still visible"