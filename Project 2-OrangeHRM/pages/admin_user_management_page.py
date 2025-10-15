from project_orangehrm_playwright.utils.logger import get_logger
from project_orangehrm_playwright.utils.locators import ADMIN_USER_LOCATORS

logger = get_logger()

class AdminUserManagementPage:
    """
        Page object for managing users in the Admin > User Management section.
        Supports user search, validation, and error handling.
    """

    def __init__(self, page):
        # Playwright page instance for browser interaction
        self.page = page

    def search_user_by_employee_name(
        self,
        username="",
        employee_name="",
        role="ESS",
        status="Enabled",
        timeout=5000
    ):
        """
            Searches for a user using multiple filters: username, role, employee name, and status.
            Waits for each element before interacting to ensure stability.
        """
        # Fill username input if provided
        if username:
            self.page.wait_for_selector(ADMIN_USER_LOCATORS["username_input"], timeout=timeout)
            self.page.locator(ADMIN_USER_LOCATORS["username_input"]).fill(username)

        # Select role from dropdown
        self.page.wait_for_selector(ADMIN_USER_LOCATORS["user_role_dropdown"], timeout=timeout)
        self.page.locator(ADMIN_USER_LOCATORS["user_role_dropdown"]).click()
        self.page.locator(ADMIN_USER_LOCATORS["user_role_option"](role)).click()

        # Fill and select employee name if provided
        if employee_name:
            self.page.wait_for_selector(ADMIN_USER_LOCATORS["employee_name_input"], timeout=timeout)
            self.page.locator(ADMIN_USER_LOCATORS["employee_name_input"]).fill(employee_name)
            self.page.wait_for_selector(ADMIN_USER_LOCATORS["employee_name_option"](employee_name), timeout=timeout)
            self.page.locator(ADMIN_USER_LOCATORS["employee_name_option"](employee_name)).click()

        #  Select status from dropdown
        self.page.wait_for_selector(ADMIN_USER_LOCATORS["status_dropdown"], timeout=timeout)
        self.page.locator(ADMIN_USER_LOCATORS["status_dropdown"]).click()
        self.page.locator(ADMIN_USER_LOCATORS["status_option"](status)).click()

        # Click the Search button
        self.page.wait_for_selector(ADMIN_USER_LOCATORS["search_button"], timeout=timeout)
        self.page.locator(ADMIN_USER_LOCATORS["search_button"]).click()

        # Wait for results table to appear
        self.page.wait_for_selector(ADMIN_USER_LOCATORS["user_table_row"], timeout=timeout)

    def is_username_already_taken(self):
        """
            Checks if the 'Already exists' error message is visible for the username field.
            Returns True if the error is present, False otherwise.
        """
        error_locator = self.page.locator(ADMIN_USER_LOCATORS["error_message"])
        return error_locator.is_visible() and "Already exists" in error_locator.text_content()

    def get_username_error_text(self):
        """
            Returns the full error message text from the username field.
            Useful for logging or debugging validation failures.
        """
        error_locator = self.page.locator(ADMIN_USER_LOCATORS["error_message"])
        return error_locator.text_content() or ""