from guvi_automation.pages.base_page import BasePage
from guvi_automation.pages.dashboard_page import DashboardPage
from guvi_automation.pages.login_page import LoginPage
from guvi_automation.utils.data_loader import load_test_data
import pytest

test_data = load_test_data("C:\\Users\\Rajesh C\\PycharmProjects\\Guvi_Projects\\guvi_automation\\tests\\test_data.json")
# Load the valid credential from the json file

@pytest.mark.edge
# Tags the test for Edge browser execution — great for cross-browser filtering.

# Method is for Login-logout flow and its validation
def test_login_logout_flow(driver):
    # Assumes a fixture is injecting the WebDriver instance

    base= BasePage(driver)  # Instantiates the page object using the shared driver.
    base.click_base_login_button()  # Click the base page's login button

    login = LoginPage(driver) # Instantiates the page object using the shared driver.

    # Extract credentials from test data
    email = test_data["valid_login"]["email"]
    password = test_data["valid_login"]["password"]

    assert login.login_functionality_valid_user(email, password), "Login failed"
    # Validates login functionality using valid credential

    dashboard = DashboardPage(driver) # Instantiates the page object using the shared driver.
    dashboard.logout() # Perform Logout

    expected_logout_url = "https://www.guvi.in/"
    actual_url = driver.current_url

    assert actual_url == expected_logout_url, f"Expected logout URL: {expected_logout_url}, but got: {actual_url}"
    # Validates URL after proper logout and navigate to the base page



