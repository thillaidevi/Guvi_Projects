from playwright.sync_api import Page
from project_orangehrm_playwright.utils.logger import get_logger
from project_orangehrm_playwright.utils.locators import ClaimPageLocators as C

class ClaimPage:
    def __init__(self, page: Page, logger=None):
        self.page = page
        self.logger = logger or get_logger("ClaimPage")

        # Sidebar navigation item for Claim module
        self.claim_module = page.locator("span.oxd-main-menu-item--name", has_text="Claim")

        # Top navigation tab for submitting a new claim
        self.submit_claim_tab = page.locator("a.oxd-topbar-body-nav-tab-item", has_text="Submit Claim")

        # Button to initiate claim creation
        self.submit_claim_button = page.locator("button.oxd-button--secondary", has_text="Submit Claim")

        #  Header text on the Create Claim Request page
        self.create_claim_header = page.locator("h6.orangehrm-main-title", has_text="Create Claim Request")

    def go_to_claim_section(self):
        """Navigate directly to the Claim section using external locator"""

        self.logger.info("Navigating to Claim section")
        self.page.goto(C["claim_section_url"])

    def click_submit_claim(self):
        """Click the '+ Submit Claim' button after ensuring the tab is visible"""
        self.logger.info(" Waiting for 'Submit Claim' tab to be visible")
        self.submit_claim_tab.wait_for(state="visible", timeout=5000)

        self.logger.info(" Clicking '+ Submit Claim' button")
        self.submit_claim_button.click()

    def validate_create_claim_header(self):
        """Validate that the Create Claim Request page is loaded"""

        self.logger.info("Validating 'Create Claim Request' header")
        self.create_claim_header.wait_for(state="visible", timeout=5000)
        assert self.create_claim_header.is_visible(), "Create Claim Request header not visible"




