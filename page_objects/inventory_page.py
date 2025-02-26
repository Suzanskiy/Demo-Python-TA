from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from .base_page import BasePage

class InventoryPage(BasePage):
    # Locators
    LOCATORS = {
        "cart_badge": (By.CLASS_NAME, "shopping_cart_badge"),
        "cart_button": (By.ID, "shopping_cart_container"),
        "product_names": (By.CLASS_NAME, "inventory_item_name"),
        "product_descriptions": (By.CLASS_NAME, "inventory_item_desc"),
        "product_prices": (By.CLASS_NAME, "inventory_item_price"),
        "product_images": (By.CLASS_NAME, "inventory_item_img"),
        "add_to_cart_buttons": (By.CLASS_NAME, "btn_small"),
        "burger_menu": (By.ID, "react-burger-menu-btn"),
        "logout_link": (By.ID, "logout_sidebar_link"),
        "sort_dropdown": (By.CLASS_NAME, "product_sort_container")
    }

    SORT_OPTIONS = {
        "az": "az",  # Name (A to Z)
        "za": "za",  # Name (Z to A)
    }

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.saucedemo.com/inventory.html"

    def is_on_inventory_page(self):
        return self.driver.current_url == self.url

    def get_product_count(self):
        return len(self.find_elements(self.LOCATORS["product_names"]))

    def get_product_details(self):
        names = self.find_elements(self.LOCATORS["product_names"])
        descriptions = self.find_elements(self.LOCATORS["product_descriptions"])
        prices = self.find_elements(self.LOCATORS["product_prices"])
        images = self.find_elements(self.LOCATORS["product_images"])
        return list(zip(names, descriptions, prices, images))

    def add_to_cart(self, product_id):
        button_locator = f"add-to-cart-{product_id}"
        self.click((By.ID, button_locator))

    def remove_from_cart(self, product_id):
        self.click((By.ID, f"remove-{product_id}"))

    def get_cart_badge_count(self):
        try:
            badges = self.find_elements(self.LOCATORS["cart_badge"])
            return int(badges[0].text) if badges else 0
        except TimeoutException:
            return 0

    def click_burger_menu(self):
        self.click(self.LOCATORS["burger_menu"])

    def click_logout(self):
        self.click_burger_menu()
        self.click(self.LOCATORS["logout_link"])

    def get_add_to_cart_buttons(self):
        return self.find_elements(self.LOCATORS["add_to_cart_buttons"])

    def get_product_names(self):
        return self.find_elements(self.LOCATORS["product_names"])

    def sort_products(self, sort_option):
        """
        Sort products using the dropdown menu
        :param sort_option: One of: 'az', 'za', 
        """
        if sort_option not in self.SORT_OPTIONS:
            raise ValueError(f"Invalid sort option. Must be one of: {list(self.SORT_OPTIONS.keys())}")
        
        select = Select(self.find_element(self.LOCATORS["sort_dropdown"]))
        select.select_by_value(self.SORT_OPTIONS[sort_option])

    def get_product_names_list(self):
        """Return list of product names in current order"""
        return [name.text for name in self.find_elements(self.LOCATORS["product_names"])]
