from playwright.sync_api import Page, expect
from datetime import datetime
from project_orangehrm_playwright.utils.logger import get_logger
from project_orangehrm_playwright.utils.screenshots import capture_screenshot
from project_orangehrm_playwright.utils.locators import PIM_LOCATORS

logger = get_logger()

class PIMPage:
    def __init__(self, page: Page, logger):
        self.page = page
        self.logger = logger

    def add_employee(self, first_name: str, last_name: str):
        """
            Adds a new employee via the PIM module.
            Captures employee ID if available and returns a summary dict.
        """
        try:
            # Navigate to PIM tab
            self.page.locator(PIM_LOCATORS["pim_tab"]).click()

            # Validate PIM header is visible
            pim_header = self.page.locator(PIM_LOCATORS["pim_header"])
            expect(pim_header).to_have_text("PIM")
            expect(pim_header).to_be_visible()

            logger.info("Clicking Add Employee")
            self.page.locator(PIM_LOCATORS["add_btn"]).click()

            #  Fill employee details
            logger.info(f"Filling employee details: {first_name} {last_name}")
            self.page.locator(PIM_LOCATORS["first_name"]).fill(first_name)
            self.page.locator(PIM_LOCATORS["last_name"]).fill(last_name)

            # Capture auto-generated Employee ID
            emp_id_locator = self.page.locator(PIM_LOCATORS["emp_id"])
            emp_id_locator.wait_for(state="visible")

            emp_id_value = None
            for _ in range(30):
                value = emp_id_locator.input_value()
                if value:
                    emp_id_value = value
                    print(f"Captured Employee ID: {emp_id_value}")
                    break
                self.page.wait_for_timeout(100)

            if emp_id_value is None:
                print("Employee ID not found — skipping capture.")

            # Save employee record
            logger.info("Saving employee record")
            self.page.locator(PIM_LOCATORS["save_btn"]).click()
            self.page.wait_for_timeout(1000)
            logger.info(f" Employee {first_name} {last_name} added successfully")

            return {
                "employee_id": emp_id_value,
                "first_name": first_name,
                "last_name": last_name
            }

        except Exception as e:
            # Capture screenshot on failure
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            screenshot_name = f"add_employee_failure_{timestamp}.png"
            capture_screenshot(self.page, screenshot_name)
            logger.error(f" Failed to add employee: {e}")
            raise

    def click_admin_tab(self):
        """
            Navigates to the Admin tab from the sidebar.
            Validates that the Admin header is visible.
        """

        try:
            self.logger.info(" Navigating to Admin tab from PIM")
            self.page.locator("a.oxd-main-menu-item:has-text('Admin')").click()
            expect(self.page.locator("h6.oxd-text--h6", has_text="Admin"))
            self.logger.info(" Admin tab loaded successfully")
        except Exception as e:
            capture_screenshot(self.page, "admin_tab_navigation_failed.png")
            self.logger.error(f" Failed to navigate to Admin tab: {e}")
            raise