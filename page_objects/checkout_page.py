#  © 2025 Serhii Suzanskyi
#  Open-source and awesome! Use it, modify it, share it—just don’t break it.
#  See LICENSE for details.

from selenium.webdriver.common.by import By
from .base_page import BasePage
from decimal import Decimal

class CheckoutPage(BasePage):
    LOCATORS = {
        "first_name": (By.ID, "first-name"),
        "last_name": (By.ID, "last-name"),
        "postal_code": (By.ID, "postal-code"),
        "continue_button": (By.ID, "continue"),
        "finish_button": (By.ID, "finish"),
        "item_total": (By.CLASS_NAME, "summary_subtotal_label"),
        "tax": (By.CLASS_NAME, "summary_tax_label"),
        "total": (By.CLASS_NAME, "summary_total_label"),
        "cancel_button": (By.ID, "cancel")
    }

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.saucedemo.com/checkout-step-one.html"

    def enter_shipping_info(self, first_name, last_name, postal_code):
        self.input_text(self.LOCATORS["first_name"], first_name)
        self.input_text(self.LOCATORS["last_name"], last_name)
        self.input_text(self.LOCATORS["postal_code"], postal_code)

    def click_continue(self):
        self.click(self.LOCATORS["continue_button"])

    def click_finish(self):
        self.click(self.LOCATORS["finish_button"])

    def get_item_total(self):
        item_total_text = self.find_element(self.LOCATORS["item_total"]).text
        return Decimal(item_total_text.split("$")[1])

    def get_tax(self):
        tax_text = self.find_element(self.LOCATORS["tax"]).text
        return Decimal(tax_text.split("$")[1])

    def get_total(self):
        total_text = self.find_element(self.LOCATORS["total"]).text
        return Decimal(total_text.split("$")[1])

    def is_on_checkout_page(self):
        return "checkout" in self.driver.current_url 