#  © 2025 Serhii Suzanskyi
#  Open-source and awesome! Use it, modify it, share it—just don’t break it.
#  See LICENSE for details.

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def wait_for_page_load(self):
        """Waits until the document is fully loaded (ready state = 'complete')."""
        try:
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        except TimeoutException:
            raise AssertionError("❌ Page did not load properly! Possible product defect.")

    def find_element(self, locator):
        """Finds a single element and asserts that it exists."""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            assert element is not None, f"❌ Element {locator} not found! Possible product defect."
            return element
        except TimeoutException:
            raise AssertionError(f"❌ Element {locator} NOT found within time! Possible product defect.")

    def find_elements(self, locator):
        """Finds multiple elements and asserts that at least one exists."""
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            assert len(elements) > 0, f"❌ No elements found for {locator}! Possible product defect."
            return elements
        except TimeoutException:
            raise AssertionError(f"❌ Elements {locator} NOT found within time! Possible product defect.")

    def click(self, locator):
        """Waits for an element to be clickable before clicking."""
        self.wait_for_page_load()
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            assert element.is_displayed() and element.is_enabled(), f"❌ Element {locator} is NOT clickable! Possible product defect."
            self.driver.execute_script("arguments[0].click();", element)
        except TimeoutException:
            raise AssertionError(f"❌ Element {locator} is NOT clickable within time! Possible product defect.")

    def input_text(self, locator, text):
        """Waits for an element to be visible and editable before sending text."""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            assert element.is_displayed() and element.is_enabled(), f"❌ Element {locator} is NOT editable! Possible product defect."
            element.clear()
            element.send_keys(text)
        except TimeoutException:
            raise AssertionError(f"❌ Unable to input text into {locator}! Possible product defect.")
