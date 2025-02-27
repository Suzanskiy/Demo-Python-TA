from selenium.webdriver.common.by import By
from .base_page import BasePage

class OrderCompletePage(BasePage):
    LOCATORS = {
        "complete_header": (By.CLASS_NAME, "complete-header"),
        "complete_text": (By.CLASS_NAME, "complete-text"),
        "back_home_button": (By.ID, "back-to-products"),
        "complete_container": (By.CLASS_NAME, "checkout_complete_container")
    }

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.saucedemo.com/checkout-complete.html"

    def is_on_complete_page(self):
        return self.driver.current_url == self.url

    def get_confirmation_header(self):
        return self.find_element(self.LOCATORS["complete_header"]).text

    def get_confirmation_text(self):
        return self.find_element(self.LOCATORS["complete_text"]).text

    def click_back_home(self):
        self.click(self.LOCATORS["back_home_button"])

    def is_order_complete_container_displayed(self):
        return self.find_element(self.LOCATORS["complete_container"]).is_displayed() 