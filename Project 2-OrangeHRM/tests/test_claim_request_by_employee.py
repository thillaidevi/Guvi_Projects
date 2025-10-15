import json
import pytest
from playwright.sync_api import Page, expect
from project_orangehrm_playwright.pages.dashboard_page import DashboardPage
from project_orangehrm_playwright.pages.login_page import LoginPage
from project_orangehrm_playwright.pages.create_claim_page import CreateClaimPage
from project_orangehrm_playwright.pages.submit_claim_page import SubmitClaimPage
from project_orangehrm_playwright.utils.logger import get_logger
from project_orangehrm_playwright.utils.screenshots import capture_screenshot

# Initialize logger
logger = get_logger("ClaimRequest")

# Load test data from JSON file
with open("C:\\Users\\Rajesh C\\PycharmProjects\\Guvi_Projects\\project_orangehrm_playwright\\data\\users.json") as f:
    data = json.load(f)

# Employee login credentials
employee_login_data = data["login_page"]["new_user"]

# Claim metadata
claim_data = data["claim_data"]

# Expense entry details
assign_claim_data = data["assign_claim_data"]


def test_claim_request_by_employee(page: Page):
    """Test-Case: Employee logs in and initiates a claim request with expense entry and validation."""
    login_page = LoginPage(page, logger)
    dashboard = DashboardPage(page, logger)
    create_claim_page = CreateClaimPage(page, logger)

    # Step 1: Login as employee
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    login_page.enter_credentials(employee_login_data["Username"], employee_login_data["Password"])
    login_page.submit()

    # Validate login success
    assert "dashboard" in page.url, " Login failed or unexpected landing page"
    logger.info(f" Logged in as employee: {employee_login_data['Username']}")

    # Step 2: Navigate to Claim module
    dashboard.click_claim_module()
    logger.info(" Navigated to Claim module")

    # Step 3: Validate My Claims page
    expect(page.locator("h5.oxd-table-filter-title:has-text('My Claims')")).to_be_visible(timeout=10000)
    logger.info(" My Claims page loaded successfully")

    # Step 4: Click Submit Claim tab
    submit_claim_button = page.locator("button:has-text('Submit Claim')")
    expect(submit_claim_button).to_be_visible(timeout=5000)
    submit_claim_button.click()
    logger.info(" Clicked Submit Claim button to open Create Claim form")

    # Step 5: Create Claim
    create_claim_page.initiate_claim(
        event=claim_data["Event"],
        currency=claim_data["Currency"],
        remarks=claim_data["Remarks"]
    )

    # Step 6: Submit Claim Page
    submit_claim_page = SubmitClaimPage(page, logger)

    # Step 7: Open Add Expense popup
    submit_claim_page.click_add_expense_button()

    # Step 8: Fill and save expense
    submit_claim_page.add_expense_popup_entry(
        expense_type=assign_claim_data["ExpenseType"],
        date=assign_claim_data["Date"],
        amount=assign_claim_data["Amount"],
        note=assign_claim_data["Note"]
    )

    # Step 9: Validate autofilled currency and total amount
    submit_claim_page.validate_autofilled_currency_with_total(
        expected_currency=claim_data["Currency"],
        expected_amount=f"{assign_claim_data['Amount']}.00"
    )
