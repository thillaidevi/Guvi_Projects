from project_orangehrm_playwright.utils.locators import FORGOT_PASSWORD_LOCATORS
from playwright.sync_api import Page

class ForgotPasswordPage:
    def __init__(self, page: Page):
        self.page = page

        #Input field for entering the username or login ID
        self.username_input = page.locator(FORGOT_PASSWORD_LOCATORS["username_input"])

        # Button to trigger password reset request
        self.reset_button = page.locator(FORGOT_PASSWORD_LOCATORS["reset_button"])

        # Message shown after clicking reset
        self.confirmation_message = page.locator(FORGOT_PASSWORD_LOCATORS["confirmation_message"])

        self.cancel_button = page.locator(FORGOT_PASSWORD_LOCATORS["cancel_button"])

        # Header text on the Forgot Password page
        self.header = page.locator(FORGOT_PASSWORD_LOCATORS["forgot_password_header"])

        # Success message shown after reset link is sent
        self.success_message = page.locator(FORGOT_PASSWORD_LOCATORS["success_message"])

    def enter_username(self, username: str):
        """Fills in the username field with the provided value"""
        self.username_input.fill(username)

    def click_reset_button(self):
        """Clicks the Reset Password button to initiate the reset flow"""
        self.reset_button.click()

    def get_confirmation_message(self) -> str:
        """Returns the confirmation message text after clicking reset"""
        return self.confirmation_message.text_content()

    def is_reset_successful(self) -> bool:
        """
            Validates whether the password reset was successful.
            Checks for URL redirect and visibility of success message.
        """
        return (
                self.page.url.endswith("/auth/sendPasswordReset") and
                self.success_message.is_visible() and
                "Reset Password link sent successfully" in self.success_message.text_content()
        )
