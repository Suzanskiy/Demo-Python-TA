#  © 2025 Serhii Suzanskyi 🚀
#  Open-source and awesome! Use it, modify it, share it—just don’t break it. 😉
#  See LICENSE for details.

import json
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load test data
with open('test_data/products.json') as f:
    PRODUCT_DATA = json.load(f)

# Locators
LOCATORS = {
    "cart_badge": (By.CLASS_NAME, "shopping_cart_badge"),
    "cart_button": (By.ID, "shopping_cart_container"),
    "product_names": (By.CLASS_NAME, "inventory_item_name"),
    "product_descriptions": (By.CLASS_NAME, "inventory_item_desc"),
    "product_prices": (By.CLASS_NAME, "inventory_item_price"),
    "product_images": (By.XPATH, "//img[@class='inventory_item_img']"),
    "add_to_cart_buttons": (By.CLASS_NAME, "btn_small")
}

@given('I am logged in as "{username}"')
def step_impl(context, username):
    context.driver.get("https://www.saucedemo.com/")
    context.driver.find_element(By.ID, "user-name").send_keys(username)
    context.driver.find_element(By.ID, "password").send_keys("secret_sauce")
    context.driver.find_element(By.ID, "login-button").click()

@given('I am on the inventory page')
def step_impl(context):
    wait = WebDriverWait(context.driver, 10)
    wait.until(lambda driver: driver.current_url == "https://www.saucedemo.com/inventory.html")

@then('I should see {count:d} products listed')
def step_impl(context, count):
    products = context.driver.find_elements(*LOCATORS["product_names"])
    assert len(products) == count, f"Expected {count} products, but found {len(products)}"

@then('each product should have correct details from test data')
def step_impl(context):
    product_names = context.driver.find_elements(*LOCATORS["product_names"])
    product_descriptions = context.driver.find_elements(*LOCATORS["product_descriptions"])
    product_prices = context.driver.find_elements(*LOCATORS["product_prices"])
    product_images = context.driver.find_elements(*LOCATORS["product_images"])

    for i, product in enumerate(PRODUCT_DATA["products"]):
        assert product["name"] == product_names[i].text, f"Product name mismatch for product {i}"
        assert product["description"] == product_descriptions[i].text, f"Description mismatch for {product['name']}"
        assert f"${product['price']}" == product_prices[i].text, f"Price mismatch for {product['name']}"
        assert product['image_url'] in product_images[i].get_attribute("src"), \
            f"Image URL mismatch for {product['name']}"

@then('each product should have an "Add to cart" button')
def step_impl(context):
    buttons = context.driver.find_elements(*LOCATORS["add_to_cart_buttons"])
    product_count = len(context.driver.find_elements(*LOCATORS["product_names"]))
    assert len(buttons) == product_count, "Not all products have Add to cart button"

@when('I add "{product_name}" to the cart')
def step_impl(context, product_name):
    product_data = next(p for p in PRODUCT_DATA["products"] if p["name"] == product_name)
    button_id = product_data["id"]
    context.driver.find_element(By.ID, button_id).click()

@then('the cart badge should show "{count}"')
def step_impl(context, count):
    badge = context.driver.find_element(*LOCATORS["cart_badge"])
    assert badge.text == count, f"Expected cart count {count}, but got {badge.text}"

@then('the button text should change to "{text}"')
def step_impl(context, text):
    wait = WebDriverWait(context.driver, 10)
    button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"button:contains('{text}')")))
    assert button.text == text, f"Expected button text '{text}', but got '{button.text}'"

@when('I add the following products to cart')
def step_impl(context):
    for row in context.table:
        product_name = row[0]
        step_impl(context, product_name)

@when('I click Remove for "{product_name}"')
def step_impl(context, product_name):
    product_data = next(p for p in PRODUCT_DATA["products"] if p["name"] == product_name)
    button_id = product_data["id"].replace("add-to-cart", "remove")
    context.driver.find_element(By.ID, button_id).click()

@then('the cart badge should not be visible')
def step_impl(context):
    badges = context.driver.find_elements(*LOCATORS["cart_badge"])
    assert len(badges) == 0, "Cart badge is still visible" 