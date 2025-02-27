#  © 2025 Serhii Suzanskyi 🚀
#  Open-source and awesome! Use it, modify it, share it—just don't break it. 😉
#  See LICENSE for details.

from behave import given, when, then, step

from page_objects.inventory_page import InventoryPage
from page_objects.login_page import LoginPage
from config.users import Users

@given('I am on the SauceDemo login page')
def step_impl(context):
    context.login_page = LoginPage(context.driver)
    context.login_page.open()
    assert context.login_page.is_on_login_page()

@given('I am logged in as "{username}"')
def step_impl(context, username):
    context.login_page = LoginPage(context.driver)
    context.login_page.open()
    password = Users.get_password(username)
    context.login_page.enter_username(username)
    context.login_page.enter_password(password)
    context.login_page.click_login()

@when('I enter username "{username}"')
def step_impl(context, username):
    context.login_page.enter_username(username)

@when('I enter password "{password}"')
def step_impl(context, password):
    context.login_page.enter_password(password)

@when('I click the login button')
def step_impl(context):
   context.login_page.click_login()

@when('I click on burger menu')
def step_impl(context):
    context.login_page.click_on_burger_menu()

@when('I click logout')
def step_impl(context):
    context.inventory_page = InventoryPage(context.driver)
    context.inventory_page.click_logout()

@then('I should see the inventory page')
def step_impl(context):
    assert context.driver.current_url == "https://www.saucedemo.com/inventory.html", "Not on inventory page"

@then('I should see the login page')
def step_impl(context):
    assert context.driver.current_url == "https://www.saucedemo.com/", "Not on login page"

@then('I should see error message "{expected_message}"')
def step_impl(context, expected_message):
    actual_message = context.login_page.get_error_message()
    assert expected_message in actual_message, f"Expected error message '{expected_message}' but got '{actual_message}'"


@step("I enter empty password")
def step_impl(context):
    context.login_page.enter_empty_password()

@when("I enter empty username")
def step_impl(context):
    context.login_page.enter_empty_username()