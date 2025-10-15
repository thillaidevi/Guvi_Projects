import pytest
from guvi_automation.pages.base_page import BasePage

@pytest.mark.edge
# Tags the test for Edge browser execution — great for cross-browser filtering.

def test_login_button_visibility_and_clickability(driver):
    # Assumes a fixture is injecting the WebDriver instance

    base = BasePage(driver) # Instantiates the page object using the shared driver.

    assert base.is_base_login_button_visible(), "Login button is not visible"
    # Confirms the login button is visible

    assert base.is_base_login_button_clickable(), "Login button is not clickable"
    # Confirms the login button is clickable

    base.click_base_login_button()
    # Executes the click action using your page object method

    EXPECTED_URL = "https://www.guvi.in/sign-in/" # Given for assertion
    assert EXPECTED_URL in driver.current_url.lower(), "Did not navigate to login page"
    # Validates post-click navigation

