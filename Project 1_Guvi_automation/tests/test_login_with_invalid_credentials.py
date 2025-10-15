from guvi_automation.pages.login_page import LoginPage
from guvi_automation.pages.base_page import BasePage
from guvi_automation.utils.data_loader import load_test_data
import pytest

# Load the valid credential from the json file
test_data = load_test_data("C:\\Users\\Rajesh C\\PycharmProjects\\Guvi_Projects\\guvi_automation\\tests\\test_data.json")

# Tags the test for firefox browser execution — great for cross-browser filtering.
@pytest.mark.firefox
def test_login_with_invalid_credentials(driver):
    # Assumes a fixture is injecting the WebDriver instance

    base = BasePage(driver)  # Instantiates the page object using the shared driver.

    base.click_base_login_button() # Click the base page's login button

    login = LoginPage(driver)  # Instantiates the page object using the shared driver.

    # Use invalid credentials from test data
    email = test_data["invalid_login"]["email"]
    password = test_data["invalid_login"]["password"]

    login.login_functionality_valid_user(email, password) # Called the login page method

    login.assert_login_failed_with_error()
    # Validation done for invalid credentials got failed for login attempt
















