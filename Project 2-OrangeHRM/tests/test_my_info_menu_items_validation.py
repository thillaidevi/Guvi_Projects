import pytest
from project_orangehrm_playwright.pages.my_info_page import MyInfoPage
from project_orangehrm_playwright.utils.locators import MY_INFO_LOCATORS
import logging

#  Logger setup for traceability
logger = logging.getLogger("Myinfo Menu items Validation")

# Parametrize test with all valid tab keys from MY_INFO_LOCATORS
@pytest.mark.firefox
@pytest.mark.parametrize("tab_key", [key for key, val in MY_INFO_LOCATORS.items() if isinstance(val, dict)])
def test_my_info_menu_items_validation(logged_in_context, tab_key):
    """
        Regression Test: Iterates through all My Info menu tabs and validates that each one loads correctly.
        Captures screenshot on failure for diagnostics.
    """
    # Step 1: Initialize page object
    page = logged_in_context
    my_info = MyInfoPage(page)

    #  Step 2: Navigate to My Info section
    success = my_info.navigate_to_my_info()
    assert success, "Failed to navigate to My Info tab"

    # Step 3: Validate the selected tab loads correctly
    result = my_info.validate_tab(tab_key)

    # Step 4: Log and capture screenshot if validation fails
    if not result:
        logger.warning(f"Validation failed for tab: {tab_key}")
        my_info.capture_tab_screenshot(tab_key)

    # Step 5: Final assertion to mark test pass/fail
    assert result, f" Tab '{tab_key}' failed to load or validate. Screenshot captured."