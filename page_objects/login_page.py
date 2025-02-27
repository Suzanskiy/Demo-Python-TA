#  © 2025 Serhii Suzanskyi
#  Open-source and awesome! Use it, modify it, share it—just don’t break it.
#  See LICENSE for details.

from selenium.webdriver.common.by import By

from .base_page import BasePage


class LoginPage(BasePage):
    # Locators
    LOCATORS = {
        "username_field": (By.ID, "user-name"),
        "password_field": (By.ID, "password"),
        "login_button": (By.ID, "login-button"),
        "error_message": (By.CLASS_NAME, "error-message-container"),
        "burger_menu": (By.ID, "react-burger-menu-btn"),
        "logout_link": (By.ID, "logout_sidebar_link")
    }

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.saucedemo.com/"

    def open(self):
        self.driver.get(self.url)
        return self

    def enter_username(self, username):
        self.input_text(self.LOCATORS["username_field"], username)
        return self

    def enter_password(self, password):
        self.input_text(self.LOCATORS["password_field"], password)
        return self

    def click_login(self):
        self.click(self.LOCATORS["login_button"])
        return self

    def get_error_message(self):
        return self.find_element(self.LOCATORS["error_message"]).text

    def is_on_login_page(self):
        return self.driver.current_url == self.url

    def click_on_burger_menu(self):
        return self.driver.find_element(*self.LOCATORS["burger_menu"]).click()

    def click_logout_link(self):
       el =  self.find_element(self.LOCATORS["logout_link"]).click()
       return self.click(el)

    def enter_empty_password(self):
        return "empty password"

    def enter_empty_username(self):
        return "empty username"