import logging, json, re
from playwright.sync_api import Page, expect
from project_orangehrm_playwright.utils.locators import LeavePageLocators as L, success_message_selectors, LeaveEntitlementLocators as E

logger = logging.getLogger(__name__)

class LeaveEntitlementPage:
    def __init__(self, page: Page, logger=logger):
        self.page = page
        self.logger = logger

    def normalize_name(self, name: str) -> str:
        """
            Normalizes employee names by trimming and collapsing whitespace.
            Useful for comparing input vs. resolved values from dropdowns.
        """
        return re.sub(r"\s+", " ", name.strip())

    def go_to_add_entitlement(self):
        """
            Navigates to the 'Add Leave Entitlement' page via sidebar and dropdown.
            Skips navigation if already on the target page.
        """
        self.page.wait_for_load_state("networkidle", timeout=7000)
        self.page.wait_for_timeout(1500)

        if self.page.locator(E["page_title"]).is_visible():
            self.logger.info("Already on 'Add Leave Entitlement' page — skipping navigation")
            return

        self.logger.info("Navigating to 'Add Leave Entitlement' page")

        try:
            # Click sidebar Leave tab
            leave_tab = self.page.locator("a.oxd-main-menu-item:has-text('Leave')")
            leave_tab.scroll_into_view_if_needed()
            leave_tab.click(force=True)
            self.logger.info(" Clicked Leave tab from sidebar")
        except Exception as e:
            self.logger.error(f" Failed to click Leave tab: {e}")
            self.page.screenshot(path="leave_tab_click_failure.png")
            raise

        try:
            #  Expand Entitlements dropdown
            entitlements_dropdown = self.page.locator("li:has-text('Entitlements') i.oxd-icon.bi-chevron-down")
            entitlements_dropdown.scroll_into_view_if_needed()
            entitlements_dropdown.click(force=True)
            self.logger.info(" Opened Entitlements dropdown")

            #  Click 'Add Entitlements' link
            add_entitlements_link = self.page.locator("a.oxd-topbar-body-nav-tab-link:has-text('Add Entitlements')")
            add_entitlements_link.click(force=True)
            self.logger.info(" Clicked 'Add Entitlements' link")
        except Exception as e:
            self.logger.error(f" Failed to open Entitlements dropdown or click link: {e}")
            self.page.screenshot(path="entitlement_dropdown_failure.png")
            raise

        # Confirm page load
        self.page.wait_for_selector(E["page_title"], timeout=7000)
        self.logger.info(" 'Add Leave Entitlement' page loaded successfully")

    def select_employee(self, employee_name: str, max_retries: int = 3):
        """
            Selects an employee from the autocomplete dropdown.
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

                # Validate resolved name
                resolved = self.normalize_name(input_box.input_value())
                expected = self.normalize_name(employee_name)
                if expected in resolved and "Invalid" not in resolved:
                    self.logger.info(f" Employee resolved: {resolved}")
                    return
            except Exception as e:
                self.logger.warning(f" Suggestion click failed: {e}")
        raise Exception(f" Failed to select employee '{employee_name}' after {max_retries} attempts")

    class LeaveTypeNotFoundError(Exception):
        """Raised when the desired leave type is not found in the dropdown."""
        pass

    def select_leave_type(self, leave_type: str):
        """
        Selects a leave type from the dropdown.
        Normalizes input and matches against available options.
        """
        self.logger.info(f"Raw leave type input: {leave_type}")
        normalized = leave_type.replace("â€“", "-").replace("–", "-").strip().lower()
        self.logger.info(f"Normalized leave type: {normalized}")

        try:
            # Capture screenshot before interacting with dropdown
            self.page.screenshot(path="before_leave_type_dropdown_click.png")

            # Scope the dropdown using label context
            dropdown = self.page.locator("label:has-text('Leave Type')").locator(
                "xpath=../following-sibling::div//div[contains(@class, 'oxd-select-text-input')]")
            dropdown.first.click(force=True)
            self.logger.info("Clicked Leave Type dropdown")

            # Iterate through options and match normalized text
            options = self.page.locator("div[role='listbox'] div")
            for i in range(options.count()):
                option_text = options.nth(i).inner_text().strip().lower()
                if normalized in option_text or ("can" in option_text and "vacation" in option_text):
                    options.nth(i).click(force=True)
                    self.logger.info(f"Selected leave type: {option_text}")
                    return

            # Fallback: try direct match using has_text
            fallback_option = options.filter(has_text=leave_type).first
            if fallback_option.is_visible():
                fallback_option.click(force=True)
                self.logger.info(f"Fallback selected leave type: {leave_type}")
                return

            raise self.LeaveTypeNotFoundError(f"Leave type '{leave_type}' not found in dropdown")

        except Exception as e:
            self.logger.error(f"Failed to select leave type: {e}")
            self.page.screenshot(path="leave_type_selection_failure.png")
            raise

    def assign_leave_period_entitlement_and_save(self, entitlement_value="20", max_retries=2):
        """
            Fills the entitlement value and clicks Save.
            Retries if input fails or validation checks don't pass.
        """
        for attempt in range(max_retries + 1):
            try:
                self.logger.info(f"Attempt {attempt + 1}: Filling entitlement value '{entitlement_value}'")

                # Scoped locator: input field next to 'Entitlement' label
                input_box = self.page.locator("label:has-text('Entitlement')").locator(
                    "xpath=../following-sibling::div//input[contains(@class, 'oxd-input')]")
                input_box.wait_for(state="visible", timeout=5000)
                input_box.scroll_into_view_if_needed()
                input_box.fill(entitlement_value, force=True)

                #  Confirm value
                filled_value = input_box.input_value().strip()
                assert filled_value == entitlement_value, f"Entitlement mismatch: expected {entitlement_value}, got {filled_value}"
                self.logger.info(f" Entitlement value confirmed: {filled_value}")

                # Validate all required fields before saving
                assert self.page.locator(
                    "input[placeholder='Type for hints...']").input_value().strip() != "", "Employee name is empty"
                assert self.page.locator("div.oxd-select-text-input").nth(
                    0).inner_text().strip() != "", "Leave type not selected"
                assert self.page.locator("div.oxd-select-text-input").nth(
                    1).inner_text().strip() != "", "Leave period not selected"
                assert self.page.locator("label:has-text('Entitlement')").locator(
                    "xpath=../following-sibling::div//input").input_value().strip() != "", "Entitlement value is empty"

                #  Click Save button
                save_button = self.page.locator("button:has-text('Save')").first
                save_button.wait_for(state="visible", timeout=3000)
                save_button.scroll_into_view_if_needed()
                save_button.click(force=True)
                self.logger.info(" Save button clicked")

                #  Handle confirmation modal
                self.confirm_entitlement_update()

                #  Check for success toast
                if self.page.locator("div.oxd-toast").is_visible():
                    self.logger.info("Success toast confirmed — entitlement updated")

                return

            except Exception as e:
                self.logger.warning(f"Entitlement fill attempt {attempt + 1} failed: {e}")
                if attempt == max_retries:
                    self.logger.error(" All attempts to fill entitlement failed")
                    self.page.screenshot(path="entitlement_fill_failure.png")
                    raise

    def assign_entitlement_for_employee(self, employee_name, leave_type, leave_period, days):
        """
            High-level wrapper to assign entitlement for a specific employee.
            Calls individual steps in sequence.
        """
        self.logger.info(
            f"Assigning entitlement for {employee_name} | Type: {leave_type} | Period: {leave_period} | Days: {days}")

        self.go_to_add_entitlement()
        self.select_employee(employee_name)
        self.select_leave_type(leave_type)
        self.assign_leave_period_entitlement_and_save(entitlement_value=days)

    def load_entitlement_data(self, json_path="testdata/entitlement_data.json"):
        """
            Loads entitlement data from a JSON file and triggers assignment.
            Useful for data-driven tests or CI pipelines.
        """
        with open(json_path, "r") as f:
            data = json.load(f)
        ent = data["leave_entitlements"]
        self.assign_entitlement_for_employee(
            employee_name=ent["Employee"],
            leave_type=ent["leave_type"],
            leave_period=ent["leave_period"],
            days=ent["entitlement"]
        )

    def submit_entitlement_form(self, expected_employee_name: str, max_retries: int = 1):
        """
            Validates employee name before submitting the form.
            Retries if name is marked invalid or mismatched.
        """
        for attempt in range(max_retries + 1):
            error_locator = self.page.locator(E["invalid_error"])
            if error_locator.is_visible():
                self.logger.warning(f"Attempt {attempt + 1}: Employee name marked as 'Invalid'")
                if attempt < max_retries:
                    self.select_employee(expected_employee_name)
                    continue
                raise ValueError("Employee name is invalid after retries. Cannot proceed.")

            # Validate resolved name matches expected
            employee_input = self.page.locator(success_message_selectors["employee_input"])
            resolved_name = self.normalize_name(employee_input.input_value())
            expected_name = self.normalize_name(expected_employee_name)

            if resolved_name != expected_name:
                self.logger.warning(f"Name mismatch: expected '{expected_name}', got '{resolved_name}'")
                if attempt < max_retries:
                    self.select_employee(expected_employee_name)
                    continue
                raise ValueError("Employee name mismatch after retries. Cannot proceed.")

            self.logger.info("Ready to click Save after successful validation")

            # Submit form
            save_button = self.page.locator(E["save_button"])
            save_button.wait_for(state="visible", timeout=5000)
            assert save_button.is_enabled(), "Save button not enabled"
            save_button.click(force=True)
            try:
                self.page.wait_for_url("**/leave/viewLeaveEntitlements**", timeout=10000)
                self.logger.info(f"Redirected to: {self.page.url}")
            except Exception:
                self.logger.warning("No redirect — checking for entitlement modal")
                self.handle_entitlement_modal(confirm=True)
            return

    def handle_entitlement_modal(self, confirm=True):
        """
            Handles confirmation modal after Save.
            Can either confirm or cancel based on flag.
        """
        try:
            self.page.wait_for_selector(E["modal_title"], timeout=5000)
            button_text = "Confirm" if confirm else "Cancel"
            self.page.locator(E["modal_button"](button_text)).click()
            self.logger.info(f"{button_text}ed entitlement update")
        except Exception:
            self.logger.warning("Modal not found")

    def validate_entitlement_record(self, employee_name, leave_type, expected_days):
        """
            Searches for entitlement record and validates the number of days.
            Uses table row matching based on leave type.
        """
        self.page.wait_for_selector("input[placeholder='Type for hints...']", timeout=5000)
        self.page.locator("input[placeholder='Type for hints...']").fill(employee_name)
        self.page.wait_for_timeout(1000)
        self.page.locator(".ac_results >> text=" + employee_name).click()

        self.page.locator("button:has-text('Search')").click()
        self.page.wait_for_timeout(2000)

        #  Locate row and extract entitlement value
        row = self.page.locator(f"tr:has-text('{leave_type}')")
        actual_days = row.locator("td").nth(3).inner_text().strip()

        assert actual_days == expected_days, f" Entitlement mismatch: expected {expected_days}, got {actual_days}"
        self.logger.info(f" Entitlement verified: {actual_days} days for {leave_type}")

    def get_total_days_from_summary(self):
        """
          Extracts the total entitlement days from the summary section.
          If the Assign Leave button is enabled, clicks it to proceed.
        """
        self.logger.info("Fetching total days from summary text")
        try:
            # Locate and extract 'Total' value from summary text
            total_text = self.page.locator(E["summary_total_text"], has_text="Total").inner_text().strip()
            match = re.search(r"Total\s+([\d.]+)", total_text)
            total_days = match.group(1) if match else "0.00"
            print(f"Total Days from summary: {total_days}")
            self.logger.info(f" Total Days extracted: {total_days}")

            # Click Assign Leave button if enabled
            assign_button = self.page.locator(E["assign_leave_button"])
            if assign_button.is_enabled():
                assign_button.click()
                self.logger.info("Assign Leave button enabled and clicked after summary extraction")
            else:
                self.logger.warning("Assign button not enabled — check form validation or page state")
        except Exception as e:
            self.logger.error(f" Failed to extract total days or click Assign: {e}")

    def validate_entitlement_summary(self, expected_days: str) -> bool:
        """
            Compares extracted total days from summary against expected value.
            Returns True if matched, False otherwise.
        """
        try:
            total_text = self.page.locator(E["summary_total_text"], has_text="Total").inner_text().strip()
            match = re.search(r"Total\s+([\d.]+)", total_text)
            total_days = match.group(1) if match else "0.00"
            self.logger.info(f" Total Days extracted: {total_days}")
            return total_days == expected_days
        except Exception as e:
            self.logger.error(f" Failed to validate entitlement summary: {e}")
            return False

    def confirm_entitlement_update(self):
        """
            Handles the confirmation modal after saving entitlement.
            Verifies success toast and navigates to Assign Leave tab.
        """
        try:
            #  Buffer wait before modal appears
            self.page.wait_for_timeout(1500)

            #  Wait for confirmation message
            modal_message = self.page.locator("p.oxd-text--card-body:has-text('Existing Entitlement value')")
            modal_message.wait_for(state="visible", timeout=5000)
            self.logger.info(f" Confirmation modal: {modal_message.inner_text().strip()}")

            # Click Confirm button
            confirm_button = self.page.locator("button:has-text('Confirm')").first
            confirm_button.wait_for(state="visible", timeout=3000)
            confirm_button.scroll_into_view_if_needed()
            confirm_button.click(force=True)
            self.logger.info(" Confirm button clicked")

            #  Buffered wait for page transition
            self.page.wait_for_timeout(2000)

            #  Wait for entitlement record to load (soft assert)
            try:
                entitlement_summary = self.page.locator("div:has-text('Total')").first
                expect(entitlement_summary).to_be_visible(timeout=8000)
                text = entitlement_summary.inner_text().strip()
                self.logger.info(f" Entitlement record confirmed — {text}")
            except Exception as e:
                self.logger.warning(f" Soft assert: entitlement record not confirmed — {e}")
                self.page.screenshot(path="entitlement_soft_assert_failure.png")

            # Check for success toast
            if self.page.locator("div.oxd-toast").is_visible():
                self.logger.info(" Success toast confirmed — entitlement updated")

            #  Navigate to Assign Leave tab
            try:
                assign_leave_tab = self.page.locator("a.oxd-topbar-body-nav-tab-item:has-text('Assign Leave')")
                assign_leave_tab.wait_for(state="visible", timeout=5000)
                assign_leave_tab.scroll_into_view_if_needed()
                assign_leave_tab.click(force=True)
                self.logger.info(" Navigated to Assign Leave tab")
            except Exception as e:
                self.logger.error(f" Failed to click Assign Leave tab: {e}")
                self.page.screenshot(path="assign_leave_tab_failure.png")
                raise

        except Exception as e:
            self.logger.error(f" Failed to confirm entitlement update or load record: {e}")
            self.page.screenshot(path="entitlement_confirm_failure.png")
            raise

    def validate_total_entitlement(self, expected_total="20.00"):
        """
            Hard assertion to verify total entitlement value in summary.
        """
        total_text = self.page.locator("div:has-text('Total')").inner_text().strip()
        self.logger.info(f" Total entitlement displayed: {total_text}")
        assert expected_total in total_text, f" Total entitlement mismatch: expected {expected_total}, got {total_text}"
        self.logger.info(" Total entitlement verified")

    def validate_leave_balance_soft(self, expected_balance="20.00"):
        """
            Soft assertion to verify leave balance.
            Logs warning and captures screenshot if mismatch occurs.
        """
        try:
            balance_text = self.page.locator("div:has-text('Leave Balance')").inner_text().strip()
            self.logger.info(f" Leave Balance displayed: {balance_text}")
            assert expected_balance in balance_text, f"Soft assert: expected {expected_balance}, got {balance_text}"
            self.logger.info(" Leave balance verified")
        except Exception as e:
            self.logger.warning(f"️ Soft assert: Leave balance not confirmed — {e}")
            self.page.screenshot(path="leave_balance_soft_assert.png")