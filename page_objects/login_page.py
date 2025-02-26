from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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