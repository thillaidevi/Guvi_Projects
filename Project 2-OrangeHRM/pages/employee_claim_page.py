from playwright.sync_api import Page

class EmployeeClaimsPage:
    def __init__(self, page: Page, logger):
        self.page = page
        self.logger = logger

        # Top navigation tab for accessing Employee Claims
        self.employee_claims_tab = page.locator("a.oxd-topbar-body-nav-tab-item", has_text="Employee Claims")
        #  Static label used to confirm page load
        self.records_found = page.locator("span.oxd-text--span", has_text="Records Found")
        # Dynamic row locator for a claim based on reference ID
        self.claim_row = lambda ref_id: page.locator(f"tr:has-text('{ref_id}')")
        # 'View' button inside the claim row
        self.view_button = lambda ref_id: self.claim_row(ref_id).locator("text=View")

    def go_to_employee_claims(self):
        """
            Navigates to the Employee Claims tab.
            Waits for tab visibility before clicking to avoid flaky navigation.
        """
        self.logger.info("Navigating to Employee Claims tab")
        self.employee_claims_tab.wait_for(state="visible")
        self.employee_claims_tab.click()
        self.page.wait_for_timeout(1000)

    def click_view_details(self, reference_id: str):
        """
            Clicks the 'View' button for a specific claim using its reference ID.
            Ensures the button is visible before interaction.
        """
        self.logger.info(f"Clicking 'View' for claim {reference_id}")
        self.view_button(reference_id).wait_for(state="visible")
        self.view_button(reference_id).click()
        self.page.wait_for_timeout(1000)

    def validate_claim_details(self, expected_details: dict):
        """
            Validates claim detail fields against expected values.
            Uses label-based sibling traversal to extract actual values.
        """
        self.logger.info("Validating claim details view")

        for label, expected_value in expected_details.items():
            # Locate the label, then traverse to its corresponding value element
            locator = self.page.locator(f"text={label}").nth(0).locator("xpath=..").locator("xpath=following-sibling::*")
            actual_value = locator.inner_text().strip()

            # Assertion with detailed mismatch message
            assert actual_value == expected_value, f" Mismatch for '{label}': expected '{expected_value}', got '{actual_value}'"
            self.logger.info(f" {label}: {actual_value}")
