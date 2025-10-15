import pytest
from playwright.sync_api import expect
from project_orangehrm_playwright.pages.login_page import LoginPage
from project_orangehrm_playwright.utils.logger import get_logger

# Logger setup for traceability
logger = get_logger("Login Fields Visibility")

@pytest.mark.firefox
def test_login_fields_visibility(page):
    """
        Smoke Test: Validates that the login page fields (username and password) are visible and enabled.
        Ensures basic accessibility before functional login tests are executed.
    """
    # Step 1: Load login page
    login = LoginPage(page, logger)
    login.load()

    try:
        # Step 2: Validate visibility and interactivity of username field
        expect(login.username_input).to_be_visible(timeout=5000)
        assert login.username_input.is_enabled(), "Username field is not enabled"

        # Step 3: Validate visibility and interactivity of password field
        expect(login.password_input).to_be_visible(timeout=5000)
        assert login.password_input.is_enabled(), "Password field is not enabled"

        #  Step 4: Log success
        logger.info(" Login fields are visible and enabled")

    except Exception as e:
        logger.error(f" Login field visibility test failed: {e}")
        page.screenshot(path="screenshots/login_fields_visibility_fail.png")
        raise