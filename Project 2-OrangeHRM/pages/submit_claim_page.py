from project_orangehrm_playwright.utils.screenshots import capture_screenshot

class SubmitClaimPage:
    def __init__(self, page, logger):
        self.page = page
        self.logger = logger

        # Page header
        self.header = page.locator("h6.orangehrm-main-title:has-text('Submit Claim')")

        # Add button
        self.add_button = page.locator("button:has-text('Add')")

        # Popup header
        self.popup_header = page.locator("p.oxd-text--card-title:has-text('Add Expense')")

        # Expense popup fields
        self.expense_dropdown = page.locator("div.oxd-select-text").nth(0)
        self.date_input = page.locator("input[placeholder='yyyy-dd-mm']")
        self.amount_input = page.locator("input.oxd-input").nth(1)
        self.note_input = page.locator("textarea.oxd-textarea")

        #  Save button inside popup
        save_button = self.page.locator("button[type='submit'].orangehrm-left-space:has-text('Save')")

    def validate_submit_claim_page(self):
        """Validates that the Submit Claim page is loaded using the Reference Id label."""
        self.logger.info(" Validating Submit Claim page via Reference Id label")
        try:
            self.page.wait_for_load_state("networkidle", timeout=7000)
            self.page.wait_for_timeout(1000)

            reference_label = self.page.locator("label.oxd-label:has-text('Reference Id')")
            reference_label.wait_for(state="visible", timeout=5000)

            assert reference_label.is_visible(), " Reference Id label not visible — Submit Claim page may not have loaded"
            self.logger.info(" Submit Claim page loaded and Reference Id is visible")
        except Exception as e:
            self.logger.error(f" Submit Claim page validation failed — {e}")
            capture_screenshot(self.page, "submit_claim_reference_id_failure.png")
            raise

    def click_add_expense_button(self):
        """Clicks the correct Add button that opens the Add Expense popup."""
        try:
            self.logger.info(" Attempting to click Add button to open Add Expense popup")

            # Locate all Add buttons
            add_buttons = self.page.locator("button.oxd-button--text:has-text('Add')")
            total = add_buttons.count()
            self.logger.info(f" Found {total} Add buttons on page")

            for i in range(total):
                label = add_buttons.nth(i).text_content().strip()
                self.logger.info(f" Add button {i}: {label}")

            # Try each Add button until popup appears
            popup_header = self.page.locator("p.oxd-text--card-title:has-text('Add Expense')")

            for i in range(total):
                try:
                    self.logger.info(f" Attempting Add button {i}")
                    add_buttons.nth(i).wait_for(state="visible", timeout=5000)
                    add_buttons.nth(i).click(force=True)

                    self.page.wait_for_timeout(1000)
                    popup_header.wait_for(state="visible", timeout=5000)
                    self.logger.info(f" Add Expense popup loaded via button {i}")
                    return

                except Exception as inner_e:
                    self.logger.warning(f"️ Button {i} failed — {inner_e}")
                    self.page.wait_for_timeout(1000)

            raise Exception(" None of the Add buttons triggered the popup")

        except Exception as e:
            self.logger.error(f" Failed to open Add Expense popup — {e}")
            capture_screenshot(self.page, "add_expense_popup_failure.png")
            raise

    def add_expense_popup_entry(self, expense_type="Accommodation", date="2025-09-09", amount="50000",
                                note="Accommodation Expense"):
        """Fills the Add Expense popup and clicks Save."""
        try:
            self.logger.info(f" Filling expense: {expense_type}, ₹{amount}, {date}")

            # Select Expense Type
            expense_dropdown = self.page.locator("div.oxd-select-text").nth(0)
            expense_dropdown.wait_for(state="visible", timeout=5000)
            expense_dropdown.click(force=True)
            expense_option = self.page.locator(f"div[role='option']:has-text('{expense_type}')")
            expense_option.wait_for(state="visible", timeout=5000)
            expense_option.click(force=True)

            # Fill Date (scoped to dialog)
            date_input = self.page.locator("div[role='dialog'] input[placeholder='yyyy-dd-mm']")
            date_input.wait_for(state="visible", timeout=5000)
            date_input.fill(date, force=True)

            # Fill Amount (scoped to dialog, excludes placeholder)
            amount_input = self.page.locator("div[role='dialog'] input.oxd-input--active:not([placeholder])").first
            amount_input.wait_for(state="visible", timeout=5000)
            amount_input.fill(amount, force=True)

            # Fill Note (strict mode fix)
            note_input = self.page.locator("div[role='dialog'] textarea.oxd-textarea--active:not([disabled])")
            note_input.wait_for(state="visible", timeout=5000)
            note_input.fill(note, force=True)

            # Click Save
            save_button = self.page.locator("button[type='submit'].orangehrm-left-space:has-text('Save')")
            save_button.wait_for(state="visible", timeout=5000)
            save_button.click(force=True)

            self.page.wait_for_load_state("networkidle", timeout=7000)
            self.page.wait_for_timeout(3000)

            self.logger.info(" Expense saved successfully")

        except Exception as e:
            self.logger.error(f" Failed to fill and save expense — {e}")
            capture_screenshot(self.page, "add_expense_entry_failure.png")
            raise

    def validate_autofilled_currency_with_total(self, expected_currency="Albanian Lek", expected_amount="50,000.00"):
        """Strictly validates autofilled currency and total amount label after expense is added."""
        try:
            self.logger.info(" Validating autofilled currency against total amount label")

            # Step 1: Extract currency from the correct disabled input
            currency_input = self.page.locator("form").locator("input[disabled]").nth(1)
            currency_input.wait_for(state="visible", timeout=5000)
            autofilled_currency = currency_input.input_value().strip()
            self.logger.info(f" Autofilled currency: {autofilled_currency}")

            # Step 2: Wait for UI to settle after expense save
            self.page.wait_for_load_state("networkidle", timeout=7000)
            self.page.wait_for_timeout(1500)

            # Step 3: Extract total amount label
            total_label = self.page.locator("p.oxd-text--p:has-text('Total Amount')")
            total_label.wait_for(state="visible", timeout=5000)
            total_text = total_label.text_content().strip()
            self.logger.info(f" Total amount label: {total_text}")

            # Step 4: Normalize and validate
            normalized_total = total_text.replace(",", "")
            expected_clean = expected_amount.replace(",", "")

            assert expected_currency in total_text, f" Currency mismatch — Expected: {expected_currency}, Found: {total_text}"
            assert expected_clean in normalized_total, f" Amount mismatch — Expected: {expected_amount}, Found: {total_text}"

            self.logger.info(" Currency and amount match confirmed in total label")

        except Exception as e:
            self.logger.error(f" Currency validation failed — {e}")
            capture_screenshot(self.page, "currency_total_validation_failure.png")
            raise