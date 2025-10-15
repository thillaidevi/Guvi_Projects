import pytest
from guvi_automation.pages.base_page import BasePage

# Tags the test for firefox browser execution — great for cross-browser filtering.
@pytest.mark.firefox
def test_signup_button_visibility_and_clickability(driver):

    base = BasePage(driver)  # Instantiates the page object using the shared driver.

    assert base.is_signup_button_visible(), "Signup button is not visible" # Confirms the Signup button is visible
    assert base.is_signup_button_clickable(), "Signup button is not clickable" # Confirms the Signup button is clickable

    base.click_signup_button() # Click the base page's signup button

    EXPECTED_LOGIN_URL = "https://www.guvi.in/register/"

    assert EXPECTED_LOGIN_URL in driver.current_url.lower(), "Did not navigate to login page"
    # Validated signup button visibility and clickability asserted with URL

