from datetime import datetime
import allure
from allure_commons.types import AttachmentType
from behave.model_core import Status
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import shutil
import tempfile

from behave.parser import parse_file

from utilities.driver_factory import DriverFactory
from utilities.api_client import APIClient
from config.users import Users
from behave.model import Scenario
from behave.model import Table


def create_chrome_options():
    chrome_options = Options()
    # Add required options
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')  # Run in headless mode for CI
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    return chrome_options

def before_all(context):
    # Load configuration
    context.config = {
        'browser': 'chrome',  # Default browser
        "implicit_wait": 5,
    }
    # Make users available to all features
    context.all_users = Users.ALL_USERS.keys()
    context.valid_users = Users.VALID_USERS.keys()
    feature_dir = "features"
    for filename in os.listdir(feature_dir):
        if filename.endswith(".feature"):
            feature_path = os.path.join(feature_dir, filename)

            # Read the feature file
            with open(feature_path, "r", encoding="utf-8") as file:
                content = file.read()

            # Replace <all_users> and <valid_users> correctly
            all_users_replacement = "\n".join(f"| {user} |" for user in context.all_users)
            valid_users_replacement = "\n".join(f"| {user} |" for user in context.valid_users)

            updated_content = content.replace("| <all_users> |", all_users_replacement)
            updated_content = updated_content.replace("| <valid_users> |", valid_users_replacement)

            # Write the modified content back
            with open(feature_path, "w", encoding="utf-8") as file:
                file.write(updated_content)

    # Create reports and screenshots directories
    for dir_path in ['test_reports', 'test_reports/screenshots']:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    
    # Store the user data directory path for cleanup
    context.user_data_dir = None


def before_scenario(context, scenario):
    # Initialize WebDriver only for scenarios tagged with @ui
    if 'ui' in scenario.tags:
        driver_factory = DriverFactory()
        context.driver = driver_factory.get_driver(context.config['browser'])
        context.driver.maximize_window()
    if "api" in scenario.tags:
        context.api_client = APIClient(context.config["api_base_url"])

def after_scenario(context, scenario):
    # Cleanup WebDriver after UI scenarios
    if 'ui' in scenario.tags and hasattr(context, 'driver'):
        context.driver.quit()
    if "api" in scenario.tags:
        context.api_client = None

def before_feature(context, feature):
    """
    Reload the feature after modification to ensure Behave picks up the new values.
    """
    if not feature.filename:
        return  # Skip if there's no associated file (e.g., dynamically generated features)

    feature_file_path = feature.filename

    with open(feature_file_path, "r", encoding="utf-8") as file:
        new_content = file.read()

    # Parse and replace the existing feature with the updated version
    parsed_feature = parse_file(feature_file_path)
    feature.__dict__.update(parsed_feature.__dict__)  # Force update in place

    if 'api' in feature.tags:
        # Skip browser setup for API features
        return

    # Set up Chrome options and user data directory
    chrome_options = create_chrome_options()
    # context.user_data_dir = user_data_dir
    
    # Initialize the WebDriver
    service = Service()
    context.driver = webdriver.Chrome(service=service, options=chrome_options)
    context.driver.implicitly_wait(10)


def after_feature(context, feature):
    if hasattr(context, 'driver'):
        context.driver.quit()
    
    # Clean up the user data directory
    if context.user_data_dir and os.path.exists(context.user_data_dir):
        try:
            shutil.rmtree(context.user_data_dir)
        except Exception as e:
            print(f"Failed to remove user data directory: {e}")

def after_all(context):
    # Optionally rename the report with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if os.path.exists('test_reports/report.html'):
        os.rename(
            'test_reports/report.html',
            f'test_reports/report_{timestamp}.html'
        )

    # Clean up any remaining user data directories
    if hasattr(context, 'user_data_dir') and context.user_data_dir:
        try:
            shutil.rmtree(context.user_data_dir)
        except Exception as e:
            print(f"Failed to remove user data directory: {e}")

def after_step(context, step):
    if step.status == Status.failed and hasattr(context, 'driver'):
        # Get scenario and step names
        scenario_name = ''.join(e for e in context.scenario.name if e.isalnum() or e == '_')
        step_name = ''.join(e for e in step.name if e.isalnum() or e == '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        try:
            # Take screenshot
            screenshot_name = f"{scenario_name}_{step_name}_{timestamp}.png"
            screenshot_path = os.path.join('test_reports/screenshots', screenshot_name)
            context.driver.save_screenshot(screenshot_path)
            
            # Attach screenshot to Allure report
            allure.attach(
                context.driver.get_screenshot_as_png(),
                name="Screenshot",
                attachment_type=AttachmentType.PNG
            )
            
            # Attach page source to Allure report
            allure.attach(
                context.driver.page_source,
                name="Page Source",
                attachment_type=AttachmentType.HTML
            )
            
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")