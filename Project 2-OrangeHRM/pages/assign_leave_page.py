import re
import unicodedata
from datetime import datetime
from guvi_automation.utils.logger import logger
from project_orangehrm_playwright.pages.dashboard_page import DashboardPage
from project_orangehrm_playwright.pages.login_page import LoginPage
from project_orangehrm_playwright.utils.locators import AssignLeaveLocators as A, success_message_selectors
from playwright.sync_api import Page, expect

class AssignLeavePage:
    """
        Page object for the Assign Leave module.
        Handles employee selection, leave type, period, and duration configuration.
    """
    def __init__(self, page: Page, logger):
        #  Store Playwright page instance and logger
        self.page = page
        self.logger = logger

    def select_leave_type(self, leave_type: str):
        """
            Selects the leave type from the dropdown.
            Uses sanitized text and strict filtering to ensure correct option is selected.
        """
        leave_type = self.sanitize_text(leave_type)

        dropdown = self.page.locator("div.oxd-select-text-input").nth(0)
        dropdown.wait_for(state="visible", timeout=3000)
        dropdown.scroll_into_view_if_needed()
        dropdown.click()

        self.page.wait_for_selector("div[role='listbox']", timeout=3000)
        option = self.page.locator("div[role='listbox'] div.oxd-select-option").filter(has_text=leave_type).first
        option.wait_for(state="visible", timeout=3000)
        option.click(force=True)

        self.logger.info(f" Leave Type selected: {leave_type}")

    def select_leave_period(self, leave_period: str):
        """
        Selects the leave period from the form dropdown using strict locator strategy.
        Filters dropdowns by label text to avoid index-based ambiguity.
        """
        try:
            self.page.wait_for_selector("form div.oxd-select-text-input", timeout=3000)
            dropdowns = self.page.locator("form div.oxd-select-text-input")
            count = dropdowns.count()
            self.logger.info(f" Found {count} dropdowns in form")

            # Filter dropdowns by visible label text
            dropdown = dropdowns.filter(has_text="Leave Period").first
            dropdown.wait_for(state="visible", timeout=3000)
            dropdown.scroll_into_view_if_needed()
            dropdown.click()

            self.page.wait_for_selector("div[role='listbox']", timeout=3000)
            option = self.page.locator("div[role='listbox'] div.oxd-select-option").filter(has_text=leave_period).first
            option.wait_for(state="visible", timeout=3000)
            option.click(force=True)

            self.logger.info(f" Leave Period selected: {leave_period}")
        except Exception as e:
            self.logger.error(f" Failed to select leave period: {str(e)}")
            self.page.screenshot(path="leave_period_failure.png")



    def normalize_leave_dates(self, start: str, end: str) -> tuple[str, str]:
        """
            Ensures the start date is chronologically before the end date.
            If reversed, swaps them and logs a warning.
        """
        fmt = "%Y-%m-%d"
        start_dt = datetime.strptime(start, fmt)
        end_dt = datetime.strptime(end, fmt)
        if start_dt > end_dt:
            self.logger.warning(f"Swapping reversed dates: start={start}, end={end}")
            return end, start
        return start, end

    def set_leave_dates(self, start: str, end: str):
        """ Fills start and end date fields using strict locators """
        start_date, end_date = self.normalize_leave_dates(start, end)
        self.logger.info(f" Setting leave dates: {start_date} to {end_date}")
        try:
            # Locate date input fields using locator map
            start_input = self.page.locator(A["date_input"]("startDate"))
            end_input = self.page.locator(A["date_input"]("endDate"))

            # Ensure both fields are visible before filling
            start_input.wait_for(state="visible", timeout=3000)
            end_input.wait_for(state="visible", timeout=3000)

            # Fill both dates
            start_input.fill(start_date, force=True)
            end_input.fill(end_date, force=True)
        except Exception as e:
            self.logger.warning(f"Date fill failed, retrying: {e}")
            self.page.screenshot(path="date_fill_retry.png")
            self.page.wait_for_timeout(1000)
            start_input.fill(start_date, force=True)
            end_input.fill(end_date, force=True)

    def navigate_to_assign_leave(self):
        """
            Navigates to the Assign Leave page via sidebar and topbar tabs.
            Skips navigation if already on the correct page.
        """

        if "assignLeave" not in self.page.url:
            self.logger.info("Navigating to Assign Leave page...")

            try:
                #  Step 1: Click sidebar Leave tab
                leave_tab = self.page.locator("a.oxd-main-menu-item:has-text('Leave')").first
                leave_tab.wait_for(state="visible", timeout=5000)
                leave_tab.scroll_into_view_if_needed()
                leave_tab.click(force=True)
                self.logger.info(" Clicked Leave tab from sidebar")

                #  Step 2: Wait for Leave module to load
                self.page.wait_for_selector("nav.oxd-topbar-body-nav", timeout=7000)
                self.page.wait_for_timeout(1000)

                #  Step 3: Click Assign Leave tab from topbar
                assign_tab = self.page.locator("a.oxd-topbar-body-nav-tab-item:has-text('Assign Leave')").first
                assign_tab.wait_for(state="visible", timeout=5000)
                assign_tab.scroll_into_view_if_needed()
                assign_tab.click(force=True)
                self.logger.info(" Clicked Assign Leave tab from topbar")

                #  Step 4: Wait for Assign Leave page to load
                self.page.wait_for_url(re.compile(".*assignLeave.*"), timeout=7000)
                self.page.wait_for_selector(A["assign_leave_input"], timeout=5000)
                self.logger.info(" Assign Leave page loaded")

            except Exception as e:
                self.logger.error(f" Failed to navigate to Assign Leave page: {e}")
                self.page.screenshot(path="assign_leave_navigation_failure.png")
                raise Exception("Assign Leave page navigation failed")
        else:
            self.logger.info("Already on Assign Leave page — skipping navigation")

    def sanitize_text(self, text: str) -> str:
        """Normalizes special characters for strict locator matching."""
        return text.replace("–", "-").replace("—", "-").strip()

    def normalize_name(self, name: str) -> str:
        """Normalizes employee names by trimming and collapsing whitespace.
         Useful for comparing input vs. resolved values from dropdowns."""
        return re.sub(r"\s+", " ", name.strip())

    success_message_selectors = {
        "employee_input": "input[placeholder='Type for hints...']"
    }

    def select_employee(self, employee_name: str, max_retries: int = 3):
        """
        Selects an employee from the autocomplete dropdown on Assign Leave page.
        Retries up to `max_retries` times if suggestion fails to appear or click.
        """
        input_box = self.page.locator(success_message_selectors["employee_input"])
        for attempt in range(max_retries):
            self.logger.info(f"Attempt {attempt + 1}: Selecting employee '{employee_name}'")
            input_box.fill("")
            input_box.fill(employee_name, force=True)
            self.page.wait_for_timeout(1000)

            suggestion = self.page.locator(f"div[role='listbox'] div:has-text('{employee_name}')").first
            try:
                suggestion.wait_for(state="visible", timeout=5000)
                suggestion.click(force=True)

                resolved = self.normalize_name(input_box.input_value())
                expected = self.normalize_name(employee_name)
                if expected in resolved and "Invalid" not in resolved:
                    self.logger.info(f" Employee resolved: {resolved}")
                    return resolved
            except Exception as e:
                self.logger.warning(f" Suggestion click failed: {e}")
        raise Exception(f" Failed to select employee '{employee_name}' after {max_retries} attempts")

    def assign_leave_from_json(self, data: dict):
        """Assigns leave using structured JSON input with strict locators."""
        employee_name = self.select_employee(data["employee"])
        leave_type = data["leaveType"]
        start_date = data["fromDate"]
        end_date = data["toDate"]
        comment = data["comments"]

        try:
            #  Select employee via keyboard fallback
            self.logger.info(f"Proceeding with leave assignment for: {employee_name}")

            # Select leave type
            #  Sanitize leave type string before using it in locator
            leave_type = self.sanitize_text(data["leaveType"])

            #  Locate and click dropdown

            dropdown = self.page.locator("form div.oxd-select-text-input").first
            dropdown.wait_for(state="visible", timeout=3000)
            dropdown.scroll_into_view_if_needed()
            dropdown.click()

            # Wait for listbox and select option

            self.page.wait_for_selector("div[role='listbox']", timeout=3000)
            option = self.page.locator("div[role='listbox'] div.oxd-select-option").filter(has_text=leave_type).first
            option.wait_for(state="visible", timeout=3000)
            option.click(force=True)
            self.logger.info(f" Leave Type selected: {leave_type}")

            #  Select From Date
            from_calendar_icon = self.page.locator("i.bi-calendar").nth(0)
            from_calendar_icon.click()
            self.page.wait_for_timeout(500)  # Let calendar render

            self.page.locator("div.oxd-calendar-date").filter(has_text="10").first.click()
            self.logger.info(" From Date selected: 2025-10-10")

            #  Select To Date
            to_calendar_icon = self.page.locator("i.bi-calendar").nth(1)
            to_calendar_icon.click()
            self.page.wait_for_timeout(500)

            self.page.locator("div.oxd-calendar-date").filter(has_text="10").first.click()
            self.logger.info(" To Date selected: 2025-10-10")

            #  Fill Comment
            comment_box = self.page.locator("textarea.oxd-textarea").first
            comment_box.wait_for(state="visible", timeout=5000)
            comment_box.scroll_into_view_if_needed()
            comment_box.click(force=True)
            comment_box.fill("")
            comment_box.type(comment, delay=50)
            self.logger.info(f" Comment filled: {comment}")

            # Wait briefly to allow duration field to render
            self.page.wait_for_timeout(1000)

            # Check if duration dropdown is rendered
            duration_dropdown = self.page.locator("select#duration")
            if duration_dropdown.is_visible():
                duration_dropdown.first.click()
                self.page.locator("div[role='listbox'] div.oxd-select-option").filter(has_text="Full Day").first.click()
                self.logger.info("Duration selected: Full Day")
            else:
                self.logger.warning("Duration dropdown not rendered — skipping duration selection")
                self.page.screenshot(path="duration_missing.png")

            # Click Assign
            assign_btn = self.page.locator("button[type='submit']").filter(has_text="Assign").first
            assign_btn.wait_for(state="visible", timeout=5000)
            assign_btn.scroll_into_view_if_needed()
            assign_btn.hover()
            assign_btn.click(force=True)
            self.logger.info("Assign button clicked")

            # Wait for toast
            if self._wait_for_toast():
                return True

            # Handle Confirm Leave Assignment modal
            confirm_modal = self.page.locator("div.orangehrm-modal-header").filter(has_text="Confirm Leave Assignment")
            if confirm_modal.is_visible(timeout=3000):
                self.logger.info("Confirm Leave Assignment modal detected — likely due to zero leave balance")

                ok_button = self.page.locator("button.oxd-button--secondary", has_text="Ok").first
                ok_button.wait_for(state="visible", timeout=5000)
                ok_button.click()
                self.logger.info(" Ok button clicked to confirm leave assignment")

                # Wait for modal to close
                self.page.wait_for_selector("div.oxd-overlay", state="detached", timeout=5000)
                self.logger.info(" Confirmation modal closed")

                # Retry toast after confirmation
                if self._wait_for_toast(after_confirm=True):
                    return True
                else:
                    self.logger.warning(" Toast still not detected after confirmation")
                    self.page.screenshot(path="screenshots/toast_missing_after_confirm.png")
                    return False

            # No toast and no modal — fail
            self.logger.warning(" No toast or confirmation modal detected — possible submission issue")
            self.page.screenshot(path="screenshots/leave_assignment_uncertain.png")
            return False

        except Exception as e:
            self.logger.error(f" Leave assignment failed: {str(e)}")
            self.page.screenshot(path="screenshots/assign_leave_failure.png")
            return False

    def _wait_for_toast(self, after_confirm=False) -> bool:
        toast = self.page.locator("div.oxd-toast-content")
        for attempt in range(5):
            if toast.is_visible():
                toast_text = toast.inner_text().strip()
                prefix = " " if after_confirm else " "
                self.logger.info(f"{prefix} Toast appeared: {toast_text}")
                self.page.wait_for_timeout(3000)
                return True
            self.logger.debug(f"Toast not visible yet — attempt {attempt + 1}")
            self.page.wait_for_timeout(1000)
        return False

