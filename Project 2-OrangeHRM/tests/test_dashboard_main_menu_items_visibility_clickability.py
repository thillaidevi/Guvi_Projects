import pytest
from project_orangehrm_playwright.pages.login_page import LoginPage
from project_orangehrm_playwright.pages.dashboard_page import DashboardPage
from project_orangehrm_playwright.utils.logger import get_logger

#  Logger setup for traceability
logger = get_logger("Dashboard menu items")

# Menu items expected to be visible and clickable post-login
EXPECTED_MENU_ITEMS = [
    "Admin", "PIM", "Leave", "Time",
    "Recruitment", "My Info", "Performance", "Dashboard", "Claim", "Buzz"
]

@pytest.mark.firefox
def test_dashboard_main_menu_items_visibility_clickability(page):
    """
        Smoke Test: Validates that all expected dashboard menu items are visible and clickable after login.
    """
    # Step 1: Login
    login_page = LoginPage(page, logger)
    login_page.enter_credentials("Admin", "admin123")
    login_page.submit()

    # Step 2: Validate visibility and clickability of sidebar menu items
    dashboard = DashboardPage(page, logger)
    dashboard.validate_menu_items(EXPECTED_MENU_ITEMS)

    # Step 3: Log the logged-in user
    user = dashboard.get_logged_in_user()
    print(f"[INFO] Logged in as: {user}")