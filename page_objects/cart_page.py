#  © 2025 Serhii Suzanskyi
#  Open-source and awesome! Use it, modify it, share it—just don’t break it.
#  See LICENSE for details.

from selenium.webdriver.common.by import By
from .base_page import BasePage

class CartPage(BasePage):
    LOCATORS = {
        "cart_items": (By.CLASS_NAME, "inventory_item_name"),
        "item_prices": (By.CLASS_NAME, "inventory_item_price"),
        "remove_buttons": (By.CLASS_NAME, "cart_button"),
        "continue_shopping": (By.ID, "continue-shopping"),
        "checkout_button": (By.ID, "checkout")
    }

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.saucedemo.com/cart.html"

    def is_on_cart_page(self):
        return self.driver.current_url == self.url

    def get_cart_items(self):
        return self.find_elements(self.LOCATORS["cart_items"])

    def get_item_prices(self):
        prices = self.find_elements(self.LOCATORS["item_prices"])
        return [float(price.text.replace("$", "")) for price in prices]

    def get_total_price(self):
        return sum(self.get_item_prices())

    def get_item_names(self):
        names = self.find_elements(self.LOCATORS["item_names"])
        return [name.text for name in names]

    def click_continue_shopping(self):
        self.click(self.LOCATORS["continue_shopping"])

    def click_checkout(self):
        self.click(self.LOCATORS["checkout_button"])

    def remove_item(self, item_name):
        items = self.get_item_names()
        if item_name in items:
            index = items.index(item_name)
            remove_buttons = self.find_elements(self.LOCATORS["remove_buttons"])
            remove_buttons[index].click() 