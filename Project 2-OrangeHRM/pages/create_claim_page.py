from playwright.sync_api import Page, expect
import time
from project_orangehrm_playwright.utils.logger import get_logger
from project_orangehrm_playwright.utils.screenshots import capture_screenshot

class CreateClaimPage:
    def __init__(self, page, logger):
        self.page = page
        self.logger = logger

        # Header validation
        self.header = page.locator("h6.orangehrm-main-title", has_text="Create Claim Request")

        # Dropdowns
        self.event_dropdown = page.locator("div.oxd-select-text-input", has_text="Accommodation")
        self.currency_dropdown = page.locator("div.oxd-select-text-input", has_text="Albanian Lek")

        # Remarks textarea
        self.remarks_input = page.locator("textarea.oxd-textarea--active")

        # Create button
        self.create_button = page.locator("button.orangehrm-left-space", has_text="Create")

    def validate_header(self):
        """Ensure 'Create Claim Request' page is loaded"""
        self.logger.info(" Validating 'Create Claim Request' header")
        self.header.wait_for(state="visible", timeout=5000)
        assert self.header.is_visible(), "Header not visible — Create Claim page may not have loaded"

    def initiate_claim(self, event="Accommodation", currency="Albanian Lek", remarks="Accommodation Claim"):
        #  Select Event from dropdown
        self.logger.info(f" Selecting Event: {event}")
        event_dropdown_trigger = self.page.locator("div.oxd-select-text").nth(0)

        try:
            event_dropdown_trigger.click(force=True)
            event_option = self.page.locator(f"div[role='option']:has-text('{event}')")
            event_option.wait_for(state="visible", timeout=10000)
            event_option.click(force=True)

            # Log selected event for traceability
            selected_event = self.page.locator("div.oxd-select-text-input").nth(0).text_content()
            self.logger.info(f" Event selected: {selected_event.strip() if selected_event else '[Unknown]'}")
        except Exception as e:
            self.logger.error(f" Failed to select Event — {e}")
            capture_screenshot(self.page, "event_selection_failure.png")
            raise

        # Select Currency from second dropdown
        self.logger.info(f" Selecting Currency: {currency}")
        currency_dropdown_trigger = self.page.locator("div.oxd-select-text").nth(1)

        try:
            currency_dropdown_trigger.click(force=True)
            currency_option = self.page.locator(f"div[role='option']:has-text('{currency}')")
            currency_option.wait_for(state="visible", timeout=10000)
            currency_option.click(force=True)

            # Log selected currency for traceability
            selected_currency = self.page.locator("div.oxd-select-text-input").nth(1).text_content()
            self.logger.info(f" Currency selected: {selected_currency.strip() if selected_currency else '[Unknown]'}")
        except Exception as e:
            self.logger.error(f" Failed to select Currency — {e}")
            capture_screenshot(self.page, "currency_selection_failure.png")
            raise

       # Fill in remarks textarea
        self.logger.info(f" Entering Remarks: {remarks}")
        try:
            remarks_input = self.page.locator("textarea.oxd-textarea")
            remarks_input.wait_for(state="visible", timeout=5000)
            remarks_input.fill(remarks, force=True)
            self.logger.info(" Remarks entered successfully")
        except Exception as e:
            self.logger.error(f" Failed to enter Remarks — {e}")
            capture_screenshot(self.page, "remarks_fill_failure.png")
            raise

        #  Submit the claim by clicking 'Create' button
        self.logger.info(" Clicking Create button to submit claim")
        try:
            create_button = self.page.locator("button[type='submit'].orangehrm-left-space")
            create_button.wait_for(state="visible", timeout=5000)
            create_button.click(force=True)
            self.logger.info(" Create button clicked")

            # Wait for redirect and page stabilization
            self.page.wait_for_load_state("networkidle", timeout=7000)
            self.page.wait_for_timeout(1000)

            #  Confirm redirect by checking for 'Reference Id' label
            reference_label = self.page.locator("label.oxd-label:has-text('Reference Id')")
            reference_label.wait_for(state="visible", timeout=5000)
            self.logger.info(" Redirected to Submit Claim page — Reference Id visible")
            self.logger.info(f" Current URL: {self.page.url}")

            # Diagnostic: log all disabled inputs
            disabled_inputs = self.page.locator("input[disabled]")
            count = disabled_inputs.count()
            self.logger.info(f" Found {count} disabled inputs on Submit Claim page")

            for i in range(count):
                value = disabled_inputs.nth(i).input_value().strip()
                self.logger.info(f" Disabled input {i}: {value}")

            try:
                # Try label-based locator to extract autofilled currency
                currency_input = self.page.locator("label:has-text('Currency')").locator(
                    "xpath=following-sibling::div//input[disabled]")
                currency_input.wait_for(state="visible", timeout=5000)
                autofilled_currency = currency_input.input_value().strip()
            except Exception as e:
                self.logger.warning(f" Label-based currency locator failed — {e}")
                autofilled_currency = ""


        except Exception as e:
            self.logger.error(f" Claim submission or redirect failed — {e}")
            capture_screenshot(self.page, "submit_claim_redirect_failure.png")
            raise






