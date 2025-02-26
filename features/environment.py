#  © 2025 Serhii Suzanskyi 🚀
#  Open-source and awesome! Use it, modify it, share it—just don’t break it. 😉
#  See LICENSE for details.

from selenium import webdriver
from utilities.driver_factory import DriverFactory
from utilities.api_client import APIClient

def before_all(context):
    # Load configuration
    context.config = {
        'base_url': 'https://your-application-url.com',
        'browser': 'chrome',
        "implicit_wait": 10,
        "api_base_url": "https://your-api-url.com"
    }

def before_scenario(context, scenario):
    if 'ui' in scenario.tags:
        driver_factory = DriverFactory()
        context.driver = driver_factory.get_driver(context.config['browser'])
        context.driver.maximize_window()
    if "api" in scenario.tags:
        context.api_client = APIClient(context.config["api_base_url"])

def after_scenario(context, scenario):
    if 'ui' in scenario.tags and hasattr(context, 'driver'):
        context.driver.quit()
    if "api" in scenario.tags:
        context.api_client = None