import pytest
from playwright.sync_api import Page, expect
from project_orangehrm_playwright.utils.excel_login_helper import get_login_data, write_result
from project_orangehrm_playwright.utils.logger import get_logger

# NOTE: Using raw CSS locators in this test for reliability.
# These are scoped to login flow only and do not affect shared locator dictionaries.

LOGIN_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

LOGIN_LOCATORS = {
    "username_input": "input[name='username']",
    "password_input": "input[name='password']",
    "login_button": "button[type='submit']",
    "error_message": "p.oxd-alert-content-text",
    "user_dropdown": ".oxd-userdropdown-name",
    "logout_option": "text=Logout",
    "dashboard_header": "h6:has-text('Dashboard')"
}

# Logger setup for traceability
logger = get_logger("OrangeHRM login functionality with valid and invalid credentials")

@pytest.mark.chrome
@pytest.mark.parametrize("si_no, username, password, expected", get_login_data())
def test_orangehrm_login(page: Page, si_no, username, password, expected):
    """
    Data-Driven Test: Validates login functionality using credentials from Excel.
    Records pass/fail status back to Excel for each row.
    """

    # Step 1: Navigate to login page
    page.goto(LOGIN_URL)

    # Step 2: Fill in credentials using raw locators
    page.locator(LOGIN_LOCATORS["username_input"]).fill(username)
    page.locator(LOGIN_LOCATORS["password_input"]).fill(password)
    page.locator(LOGIN_LOCATORS["login_button"]).click()

    try:
        # Normalize expected value to avoid whitespace mismatch
        expected = expected.strip().lower()

        if expected == "pass":
            # Step 3a: Validate successful login
            expect(page.locator(LOGIN_LOCATORS["dashboard_header"])).to_be_visible()

            # Step 4a: Logout to reset state
            page.locator(LOGIN_LOCATORS["user_dropdown"]).click()
            page.locator(LOGIN_LOCATORS["logout_option"]).click()
            expect(page.locator(LOGIN_LOCATORS["login_button"])).to_be_visible()
            print(" Welcome Admin")

            # Step 5a: Write result to Excel
            write_result(si_no, "Passed ")
        else:
            # Step 3b: Validate error message for failed login
            expect(page.locator(LOGIN_LOCATORS["error_message"])).to_have_text("Invalid credentials")
            print(" Invalid Credentials Failed to login")

            # Step 5b: Write result to Excel
            write_result(si_no, "Passed ")

    except Exception as e:
        # Step 6: Capture screenshot and log failure
        page.screenshot(path=f"screenshots/{username}_fail.png")
        write_result(si_no, f"Failed : {str(e)}")
        raise