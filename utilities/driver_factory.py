#  © 2025 Serhii Suzanskyi
#  Open-source and awesome! Use it, modify it, share it—just don’t break it.
#  See LICENSE for details.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

class DriverFactory:
    @staticmethod
    def get_driver(browser_name):
        if browser_name.lower() == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")  # Open in maximized mode
            options.add_argument("--disable-gpu")  # Disable GPU (fixes some rendering issues)
            options.add_argument("--no-sandbox")  # Bypass OS security model (for Docker/Linux)
            options.add_argument("--disable-dev-shm-usage")  # Prevent crashes in Docker/Linux
            options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Avoid detection
            options.add_experimental_option("useAutomationExtension", False)  # Disable automation extension

            return webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )
        elif browser_name.lower() == "firefox":
            return webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        else:
            raise ValueError(f"Browser {browser_name} is not supported") 