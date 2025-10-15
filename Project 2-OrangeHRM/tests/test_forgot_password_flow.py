import pytest
from project_orangehrm_playwright.pages.forgot_password_page import ForgotPasswordPage
from project_orangehrm_playwright.pages.login_page import LoginPage
from project_orangehrm_playwright.utils.logger import get_logger

#  Logger setup for traceability
logger = get_logger("Forgot Password Flow")

@pytest.mark.chrome
def test_forgot_password_flow(page):
    """
        Smoke Test: Validates the Forgot Password flow for a known user.
        Ensures reset link confirmation message appears after submission.
    """
    # Step1: Initialize login page and click 'Forgot Password'
    login = LoginPage(page, logger)
    login.click_forgot_password()

    # Step 2: Interact with Forgot Password page
    forgot_page = ForgotPasswordPage(page)

    # Step 3: Enter username
    forgot_page.enter_username("Admin")  # Replace with dynamic data if needed

    # Step 4: Submit reset request
    forgot_page.click_reset_button()

    # Step 5: Validate confirmation message
    message = forgot_page.get_confirmation_message()
    assert "Reset Password link sent successfully" in message