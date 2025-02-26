from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

class DriverFactory:
    @staticmethod
    def get_driver(browser_name):
        if browser_name.lower() == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        elif browser_name.lower() == "firefox":
            return webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        else:
            raise ValueError(f"Browser {browser_name} is not supported") 