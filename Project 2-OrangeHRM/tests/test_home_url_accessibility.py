import pytest
from project_orangehrm_playwright.pages.login_page import LoginPage
from project_orangehrm_playwright.utils.logger import get_logger

# Logger setup for traceability
logger = get_logger("Home URL Accessibility")

@pytest.mark.chrome
def test_home_url_accessibility(page):
    """
        Smoke Test: Verifies that the OrangeHRM home/login page is accessible and loads with the correct title.
    """
    #  Step 1: Initialize login page and navigate to home URL
    login = LoginPage(page, logger)
    login.load()

    #  Step 2: Validate page title to confirm successful load
    assert page.title() == "OrangeHRM"

