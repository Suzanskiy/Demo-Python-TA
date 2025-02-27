#  © 2025 Serhii Suzanskyi
#  Open-source and awesome! Use it, modify it, share it—just don’t break it.
#  See LICENSE for details.

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
import os
from datetime import datetime

class TestBase:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.logger = logging.getLogger(__name__)

    def take_screenshot(self, name):
        """Take a screenshot with a given name"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_name = f"{name}_{timestamp}.png"
            screenshot_path = os.path.join('test_reports/screenshots', screenshot_name)
            self.driver.save_screenshot(screenshot_path)
            return screenshot_path
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            return None

    def log_and_take_screenshot(self, message, take_screenshot=True):
        """Log a message and optionally take a screenshot"""
        self.logger.info(message)
        if take_screenshot:
            screenshot_path = self.take_screenshot(message.replace(' ', '_'))
            if screenshot_path:
                return f"Screenshot saved: {screenshot_path}"
        return None 