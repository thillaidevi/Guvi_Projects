from playwright.sync_api import Page, expect
from project_orangehrm_playwright.pages.dashboard_page import DashboardPage
from project_orangehrm_playwright.utils.locators import LeaveReportLocators

class LeaveReportPage:
    def __init__(self, page: Page, logger):
        self.page = page
        self.logger = logger

    def navigate_to_leave_entitlement_report(self):
        """Navigates to Leave Entitlements and Usage Report via Reports tab."""

        self.logger.info(" Navigating to Leave Entitlements and Usage Report...")
        # Step 1: Click Reports tab in topbar
        reports_tab = self.page.locator("span.oxd-topbar-body-nav-tab-item", has_text="Reports").first
        reports_tab.wait_for(state="visible", timeout=5000)
        reports_tab.scroll_into_view_if_needed()
        reports_tab.click()
        self.logger.info(" Reports tab clicked")

        # Step 2: Click Leave Entitlements and Usage Report link
        report_link = self.page.locator("a.oxd-topbar-body-nav-tab-link[role='menuitem']").filter(
            has_text="Leave Entitlements and Usage Report"
        ).first
        report_link.wait_for(state="visible", timeout=5000)
        report_link.click()
        self.logger.info(" Leave Entitlements and Usage Report link clicked")

        # Step 3:  Wait for report page header to confirm navigation
        report_header = self.page.locator("h5.oxd-table-filter-title").filter(
            has_text="Leave Entitlements and Usage Report"
        )
        report_header.wait_for(state="visible", timeout=5000)
        self.logger.info(" Leave Entitlements and Usage Report page loaded successfully")

    def select_leave_type_filter(self, leave_type: str):
        """Selects Leave Type radio and dropdown filter"""
        # Select radio button
        self.page.locator("input[type='radio'][value='leave_type_leave_entitlements_and_usage']").check()
        self.logger.info(" Leave Type radio button selected")

        # Click dropdown (don't filter by text yet)
        dropdown = self.page.locator("div.oxd-select-text-input").first
        dropdown.click()
        self.logger.info(" Dropdown clicked")

        # Wait for listbox and select option
        option = self.page.locator("div[role='option']", has_text=leave_type).first
        option.wait_for(state="visible", timeout=3000)
        option.click()
        self.logger.info(f" Leave Type selected: {leave_type}")

    def validate_employee_leave_report(self, employee_name: str) -> bool:
        try:
            # Step 1: Select "Employee" radio button
            employee_radio = self.page.locator("input[type='radio'][value='employee_leave_entitlements_and_usage']")
            employee_radio.wait_for(state="visible", timeout=5000)
            employee_radio.check(force=True)
            self.logger.info(" 'Employee' radio button selected")

            # Step 2: Type employee name in autocomplete input
            name_input = self.page.locator("input[placeholder='Type for hints...']")
            name_input.wait_for(state="visible", timeout=5000)
            name_input.fill(employee_name)
            self.page.wait_for_timeout(1000)  # wait for suggestions to load

            # Step 3: Select matching suggestion
            suggestion = self.page.locator(f".oxd-autocomplete-option >> text={employee_name}").nth(0)
            suggestion.wait_for(state="visible", timeout=5000)
            suggestion.click()
            self.logger.info(f" Selected employee: {employee_name}")

            # Step 4: Click Generate to load report
            generate_btn = self.page.locator("button[type='submit']", has_text="Generate").first
            generate_btn.wait_for(state="visible", timeout=5000)
            generate_btn.scroll_into_view_if_needed()
            generate_btn.click(force=True)
            self.logger.info(" Generate button clicked")

            # Step 5: Wait for table render and validate name presence
            self.page.wait_for_timeout(2000)
            table_text = self.page.locator("table").inner_text().lower()
            self.logger.debug(f" Table text:\n{table_text}")

            if employee_name.lower() in table_text:
                self.logger.info(f" Name '{employee_name}' found in table")
                return True

            # If name not found, log and screenshot
            self.logger.warning(f" Name '{employee_name}' not found in table")
            self.page.screenshot(path="screenshots/name_not_found.png")
            return False

        except Exception as e:
            # Catch and log any unexpected errors
            self.logger.error(f" Error during leave report validation: {str(e)}")
            self.page.screenshot(path="screenshots/leave_report_validation_error.png")
            return False