from behave.parser import parse_file

from utilities.driver_factory import DriverFactory
from utilities.api_client import APIClient
from config.users import Users
from behave.model import Scenario
from behave.model import Table
import os


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