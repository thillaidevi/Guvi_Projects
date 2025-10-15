import time
from project_orangehrm_playwright.utils.locators import LOGIN_PAGE_LOCATORS, LOGIN_URL
from project_orangehrm_playwright.utils.screenshots import capture_screenshot
from project_orangehrm_playwright.utils.logger import get_logger
from datetime import datetime
from playwright.sync_api import expect


logger = get_logger()

class LoginPage:
    def __init__(self, page, logger):
        self.page = page
        self.logger = logger

        # Strict mode-friendly locators
        self.username_input = page.get_by_placeholder(LOGIN_PAGE_LOCATORS["username_input"]["value"])
        self.password_input = page.get_by_placeholder(LOGIN_PAGE_LOCATORS["password_input"]["value"])
        self.login_button = page.get_by_role("button", name=LOGIN_PAGE_LOCATORS["login_button"]["name"])
        self.error_message = page.locator(LOGIN_PAGE_LOCATORS["error_message"])
        self.user_dropdown = page.locator(LOGIN_PAGE_LOCATORS["user_dropdown"])
        self.logout_option = page.get_by_role("menuitem", name=LOGIN_PAGE_LOCATORS["logout_option"]["name"])
        self.forgot_password_link = page.locator(LOGIN_PAGE_LOCATORS["forgot_password_link"])
        self.reset_password_header = page.locator(LOGIN_PAGE_LOCATORS["reset_password_header"])

    def load(self):
        """
                Navigates to the login page and waits for DOM to load.
                Captures screenshot on failure.
        """
        logger.info("Navigating to login page: %s", LOGIN_URL)
        try:
            self.page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=60000)
            logger.info("Login page loaded successfully")
        except Exception as error:
            logger.error("Failed to load login page: %s", error)
            self.page.screenshot(path="screenshots/login_load_failure.png")
            raise Exception(f"LoginPage.load failed: {error}") from None

    def enter_credentials(self, username, password, retries=3, delay=2):
        """
            Fills in username and password fields with retry logic.
            Validates that values are filled correctly.
        """
        for attempt in range(retries):
            try:
                expect(self.username_input).to_be_visible(timeout=5000)
                expect(self.password_input).to_be_visible(timeout=5000)
                break
            except Exception as e:
                self.logger.warning(f"Retry {attempt + 1}: Username or Password field not visible — {e}")
                time.sleep(delay)
        else:
            raise Exception(" Login fields never became visible after retries")

        self.username_input.fill(username)
        self.password_input.fill(password)

        # Confirm values were filled
        assert self.username_input.input_value() == username, " Username not filled"
        assert self.password_input.input_value() == password, " Password not filled"
        self.logger.info(" Credentials entered successfully")

    def submit(self):
        """
            Clicks the login button and waits for dashboard header to confirm login.
        """
        logger.info("Submitting login form")
        self.login_button.click()
        self.page.wait_for_selector(LOGIN_PAGE_LOCATORS["dashboard_header"], timeout=10000)
        logger.info(f"Login successful, current URL: {self.page.url}")

    def is_logged_in(self):
        """
            Checks if login was successful by verifying URL and dashboard header visibility.
        """
        return "/dashboard" in self.page.url and self.page.locator(LOGIN_PAGE_LOCATORS["dashboard_header"]).is_visible()

    def logout(self):
        """
            Logs out from the application via user dropdown.
            Captures screenshot on failure.
        """
        try:
            logger.info("Attempting logout")
            self.user_dropdown.click()
            self.logout_option.click()
            self.page.wait_for_timeout(1000)
            logger.info("Logout successful")
        except Exception as e:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            capture_screenshot(self.page, f"logout_failure_{timestamp}.png")
            logger.error(f"Logout failed: {e}")
            raise

    def validate_login(self, expected_result: str) -> bool:
        """
            Validates login outcome against expected result ('pass' or 'fail').
            Logs outcome and returns boolean.
        """
        expected_result = expected_result.strip().lower()

        if expected_result == "pass":
            if self.is_logged_in():
                logger.info("Login succeeded as expected")
                return True
            else:
                logger.error(" Login failed unexpectedly")
                return False

        elif expected_result == "fail":
            error_text = self.get_error_text().lower()
            if "invalid credentials" in error_text:
                logger.info(" Login rejected as expected")
                return True
            else:
                logger.error(f" Unexpected error message: {error_text}")
                return False

        else:
            logger.warning(f" Unknown expected result: {expected_result}")
            return False

    def click_forgot_password(self):
        """
            Clicks the 'Forgot your password?' link.
        """
        self.forgot_password_link.click()

    def is_on_reset_password_page(self):
        """
            Checks if user is on the Reset Password page.
        """
        return self.page.url.endswith("/auth/requestPasswordResetCode") and self.reset_password_header.is_visible()

    def wait_with_retry(self, locator, retries=3, delay=2):
        """
            Waits for a locator to become visible with retry logic.
            Raises exception if not visible after retries.
        """
        for attempt in range(retries):
            try:
                locator.wait_for(state="visible", timeout=5000)
                return
            except Exception as e:
                self.logger.warning(f"Retry {attempt + 1}: {e}")
                time.sleep(delay)
        raise Exception("Element never became visible after retries")

    def get_error_text(self) -> str:
        """
            Returns error message text if login fails.
            Logs warning if error message is not found.
        """
        try:
            self.error_message.wait_for(state="attached", timeout=10000)
            return self.error_message.inner_text().strip()
        except Exception as e:
            logger.warning(f"Error message not found: {e}")
            return ""




