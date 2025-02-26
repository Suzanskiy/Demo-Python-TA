#  © 2025 Serhii Suzanskyi 🚀
#  Open-source and awesome! Use it, modify it, share it—just don't break it. 😉
#  See LICENSE for details.

import json
from behave import given, when, then
from page_objects.inventory_page import InventoryPage
from page_objects.login_page import LoginPage

# Load test data
with open('test_data/products.json') as f:
    PRODUCT_DATA = json.load(f)

@given('I am logged in as "{username}"')
def step_impl(context, username):
    login_page = LoginPage(context.driver)
    login_page.open()
    login_page.enter_username(username)
    login_page.enter_password("secret_sauce")
    login_page.click_login()
    
    context.inventory_page = InventoryPage(context.driver)
    assert context.inventory_page.is_on_inventory_page()


@given('I am on the inventory page')
def step_impl(context):
    context.inventory_page = InventoryPage(context.driver)
    context.inventory_page.wait_for_page_load()
    assert context.inventory_page.is_on_inventory_page()

@then('I should see {count:d} products listed')
def step_impl(context, count):
    actual_count = context.inventory_page.get_product_count()
    assert actual_count == count, f"Expected {count} products, but found {actual_count}"

@then('each product should have correct details from test data')
def step_impl(context):
    product_names = context.inventory_page.get_product_details()
    for i, (name, description, price, image) in enumerate(product_names):
        product = PRODUCT_DATA["products"][i]
        assert product["name"] == name.text, f"Product name mismatch for product {i}"
        assert product["description"] == description.text, f"Description mismatch for {product['name']}"
        assert f"${product['price']}" == price.text, f"Price mismatch for {product['name']}"
        assert product['image_url'] in image.get_attribute("src"), \
            f"Image URL mismatch for {product['name']}"

@then('each product should have an "Add to cart" button')
def step_impl(context):
    buttons = context.inventory_page.get_add_to_cart_buttons()
    product_count = len(context.inventory_page.get_product_names())
    assert len(buttons) == product_count, "Not all products have Add to cart button"

@when('I add "{product_name}" to the cart')
def step_impl(context, product_name):
    product_data = next(p for p in PRODUCT_DATA["products"] if p["name"] == product_name)
    context.inventory_page.add_to_cart(product_data["id"])

@then('the cart badge should show "{count}"')
def step_impl(context, count):
    actual_count = context.inventory_page.get_cart_badge_count()
    assert actual_count == count, f"Expected cart count {count}, but got {actual_count}"

@then('the button text should change to "{text}"')
def step_impl(context, text):
    buttons = context.inventory_page.get_add_to_cart_buttons()
    var = lambda driver: any(button.text.strip() == text for button in buttons)
    assert any(button.text.strip() == text for button in buttons), f"No button changed to '{text}'"

@when('I add the following products to cart')
def step_impl(context):
  raise NotImplementedError()

@when('I click Remove for "{product_name}"')
def step_impl(context, product_name):
    product_data = next(p for p in PRODUCT_DATA["products"] if p["name"] == product_name)
    context.inventory_page.remove_from_cart(product_data["id"])

@then('the cart badge should not be visible')
def step_impl(context):
    badges = context.inventory_page.get_cart_badge_count()
    assert len(badges) == 0, "Cart badge is still visible" 