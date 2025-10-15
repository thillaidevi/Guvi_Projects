from playwright.sync_api import Page
from project_orangehrm_playwright.utils.locators import AddExpensePopupLocators as L

class AddExpensePopup:
    def __init__(self, page: Page, logger):
        self.page = page
        self.logger = logger

        #  Dropdown to select expense type (first dropdown in popup)
        self.expense_type_dropdown = page.locator(L["EXPENSE_TYPE_DROPDOWN"]).nth(0)

        #  Input field for expense date (expects format yyyy-dd-mm)
        self.date_input = page.locator(L["DATE_INPUT"])

        # Input field for amount (second active input on form)
        self.amount_input = page.locator(L["AMOUNT_INPUT"]).nth(1)

        #  Textarea for optional notes
        self.note_textarea = page.locator(L["NOTE_TEXTAREA"])

        #  Save button to submit the expense form
        self.save_button = page.locator(L["SAVE_BUTTON"], has_text="Save")

        #  Summary block shown after successful save
        self.summary_block = page.locator(L["CLAIM_SUMMARY_BLOCK"])

    def add_expense_and_save(self, expense_type: str, date: str, amount: str, note: str):
        """Fills out the expense form and saves it."""
        self.logger.info(f"Adding expense: {expense_type}, ₹{amount}, Date: {date}, Note: {note}")

        # Select expense type from dropdown
        self.expense_type_dropdown.click()
        self.page.locator(L["EXPENSE_TYPE_OPTION"](expense_type)).click()

        # Fill date, amount, and note fields
        self.date_input.fill(date)
        self.amount_input.fill(str(amount))
        self.note_textarea.fill(note)

        # Click Save and wait briefly for summary to appear
        self.save_button.wait_for(state="visible")
        self.save_button.click()
        self.page.wait_for_timeout(1000)

    @staticmethod
    def validate_claim_summary(page, logger, expected_type="Transport", expected_amount="70,000.00",
                               expected_currency="Afghanistan Afghani"):
        """Validates the summary block after expense submission."""
        logger.info("Validating claim summary...")

        # Check that exactly one record is found
        record_locator = page.locator(L["RECORD_FOUND_TEXT"])
        assert record_locator.inner_text().contains("(1) Record Found"), "Expected 1 record, but found different"

        #  Validate total amount and currency
        total_locator = page.locator(L["TOTAL_AMOUNT_TEXT"])
        total_text = total_locator.inner_text()
        assert expected_currency in total_text, f"Currency mismatch: expected {expected_currency}"
        assert expected_amount in total_text, f"Amount mismatch: expected {expected_amount}"

        #  Confirm expense type appears in the table
        table_locator = page.locator(L["EXPENSE_TABLE"])
        assert table_locator.inner_text().contains(expected_type), f"Expense type '{expected_type}' not found in table"

        logger.info(" Claim validated successfully")

    def get_reference_id_from_summary(self) -> str:
        """Extracts the reference ID from the summary block."""
        self.logger.info(" Extracting Reference ID from claim summary")

        # Wait for summary block to be visible
        self.summary_block.wait_for(state="visible")

        # Assume first div inside summary contains the reference ID
        ref_id_locator = self.page.locator(L["SUMMARY_DIV"]).first
        reference_id = ref_id_locator.inner_text().strip()

        # Validate format of reference ID
        assert reference_id.isdigit(), f" Unexpected Reference ID format: {reference_id}"
        self.logger.info(f" Reference ID extracted: {reference_id}")
        return reference_id