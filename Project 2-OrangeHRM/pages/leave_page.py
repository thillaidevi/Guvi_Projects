from playwright.sync_api import Page
from project_orangehrm_playwright.utils.locators import LeavePageLocators as L, success_message_selectors
from datetime import datetime
import logging


logger = logging.getLogger(__name__)

class LeavePage:
    def __init__(self, page: Page, logger=logger):
        self.page = page
        self.logger = logger

    def map_leave_type(self, raw_type):
        """
            Normalizes leave type string by replacing special dashes and trimming whitespace.
            Ensures compatibility with dropdown option matching.
        """
        return raw_type.replace("–", "-").strip()

    def select_employee(self, employee_name):
        """
           Selects an employee from the autocomplete input.
           Uses keyboard navigation to confirm selection.
        """
        input_box = self.page.locator(success_message_selectors["employee_input"])
        input_box.click()
        input_box.fill(employee_name)
        self.page.keyboard.press("ArrowDown")
        self.page.keyboard.press("Enter")
        self.logger.info(f" Selected employee: {employee_name}")

    def select_leave_type(self, leave_type):
        """
            Selects a leave type from the dropdown using normalized label.
        """
        mapped_type = self.map_leave_type(leave_type)
        self.page.locator(success_message_selectors["assign_leave_type_dropdown"]).click()
        self.page.locator(success_message_selectors["assign_leave_type_option"](mapped_type)).click()
        self.logger.info(f" Selected leave type: {mapped_type}")

    def select_leave_period(self, from_date, to_date):
        """
            Fills in the leave period using date inputs.
        """
        self.page.fill(L["from_date_input"], from_date)
        self.page.fill(L["to_date_input"], to_date)
        self.logger.info(f" Selected period: {from_date} to {to_date}")

    def assign_leave(self, employee_name, leave_type, from_date, to_date, comment):
        """
            Navigates to Assign Leave page and submits a leave request.
        """
        self.page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/leave/assignLeave")
        self.select_employee(employee_name)
        self.select_leave_type(leave_type)
        self.select_leave_period(from_date, to_date)
        self.page.fill(L["comment_textarea"], comment)
        self.page.click(L["assign_button"])
        self.logger.info(f" Leave assigned to {employee_name} from {from_date} to {to_date}")

    def get_success_message(self):
        """
           Waits for and returns the success toast message after leave assignment.
        """
        toast = self.page.locator(success_message_selectors["success_message"])
        toast.wait_for(state="visible", timeout=10000)
        message = toast.inner_text().strip()
        self.logger.info(f" Success message: {message}")
        return message

    def go_to_leave_list(self):
        """
            Navigates to the Leave List page.
        """
        self.page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/leave/viewLeaveList")
        self.logger.info(" Navigated to Leave List")

    def search_leave_record(self, employee_name, from_date, to_date):
        """
            Searches for leave records using employee name and date range.
        """
        self.page.fill(L["from_date_input"], from_date)
        self.page.fill(L["to_date_input"], to_date)
        self.select_employee(employee_name)
        self.page.click(L["search_button"])
        self.page.wait_for_selector(L["leave_table_row"])
        self.logger.info(f" Searched leave records for {employee_name} between {from_date} and {to_date}")

    def is_leave_record_present(self):
        """
            Returns True if leave records are found in the result table.
            Logs the count for diagnostics.
        """
        count = self.page.locator(L["leave_table_row"]).count()
        self.logger.info(f" Leave records found: {count}")
        return count > 0



