#  © 2025 Serhii Suzanskyi
#  Open-source and awesome! Use it, modify it, share it—just don’t break it.
#  See LICENSE for details.

from selenium.webdriver.common.by import By
from .base_page import BasePage

class ProductDetailsPage(BasePage):
    LOCATORS = {
        "product_name": (By.CLASS_NAME, "inventory_details_name"),
        "product_description": (By.CLASS_NAME, "inventory_details_desc"),
        "product_price": (By.CLASS_NAME, "inventory_details_price"),
        "add_to_cart_button": (By.CSS_SELECTOR, "button.btn_inventory"),
        "back_button": (By.ID, "back-to-products")
    }

    def __init__(self, driver):
        super().__init__(driver)
        self.base_url = "https://www.saucedemo.com/inventory-item.html?id="

    def open_product(self, product_id):
        self.driver.get(f"{self.base_url}{product_id}")

    def get_product_name(self):
        return self.find_element(self.LOCATORS["product_name"]).text

    def get_product_price(self):
        return self.find_element(self.LOCATORS["product_price"]).text

    def add_to_cart(self):
        self.click(self.LOCATORS["add_to_cart_button"])

    def click_back_to_products(self):
        self.click(self.LOCATORS["back_button"]) 