#  © 2025 Serhii Suzanskyi 🚀
#  Open-source and awesome! Use it, modify it, share it—just don’t break it. 😉
#  See LICENSE for details.

from behave import given, when, then, step
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Locators
LOCATORS = {
    "username_field": (By.ID, "user-name"),
    "password_field": (By.ID, "password"),
    "login_button": (By.ID, "login-button"),
    "error_message": (By.CLASS_NAME, "error-message-container"),
    "burger_menu": (By.ID, "react-burger-menu-btn"),
    "logout_link": (By.ID, "logout_sidebar_link")
}

@given('I am on the SauceDemo login page')
def step_impl(context):
    context.driver.get("https://www.saucedemo.com/")
    assert context.driver.current_url == "https://www.saucedemo.com/", "Not on login page"

@when('I enter username "{username}"')
def step_impl(context, username):
    username_field = context.driver.find_element(*LOCATORS["username_field"])
    username_field.clear()
    username_field.send_keys(username)

@when('I enter password "{password}')
def step_impl(context, password):
    password_field = context.driver.find_element(*LOCATORS["password_field"])
    password_field.clear()
    password_field.send_keys(password)

@when('I click the login button')
def step_impl(context):
    login_button = context.driver.find_element(*LOCATORS["login_button"])
    login_button.click()

@when('I click on burger menu')
def step_impl(context):
    wait = WebDriverWait(context.driver, 10)
    burger_menu = wait.until(EC.element_to_be_clickable(LOCATORS["burger_menu"]))
    burger_menu.click()

@when('I click logout')
def step_impl(context):
    wait = WebDriverWait(context.driver, 10)
    logout_link = wait.until(EC.element_to_be_clickable(LOCATORS["logout_link"]))
    logout_link.click()

@then('I should be successfully logged in')
def step_impl(context):
    wait = WebDriverWait(context.driver, 10)
    wait.until(lambda driver: driver.current_url == "https://www.saucedemo.com/inventory.html")
    assert context.driver.current_url == "https://www.saucedemo.com/inventory.html", "Login was not successful"

@then('I should see the inventory page')
def step_impl(context):
    assert context.driver.current_url == "https://www.saucedemo.com/inventory.html", "Not on inventory page"

@then('I should see the login page')
def step_impl(context):
    assert context.driver.current_url == "https://www.saucedemo.com/", "Not on login page"

@then('I should see error message "{expected_message}"')
def step_impl(context, expected_message):
    wait = WebDriverWait(context.driver, 10)
    error_message = wait.until(EC.presence_of_element_located(LOCATORS["error_message"]))
    actual_message = error_message.text
    assert expected_message in actual_message, f"Expected error message '{expected_message}' but got '{actual_message}'"


@step("I enter empty password")
def step_impl(context):
    password_field = context.driver.find_element(*LOCATORS["password_field"])
    password_field.clear()

@when("I enter empty username")
def step_impl(context):
    namefield = context.driver.find_element(*LOCATORS["username_field"])
    namefield.clear()