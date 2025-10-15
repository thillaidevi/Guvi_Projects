from guvi_automation.pages.base_page import BasePage
import pytest

@pytest.mark.edge # Tags the test for Edge browser execution — great for cross-browser filtering.

def test_menu_items_display(driver):  # Assumes a fixture is injecting the WebDriver instance
    page = BasePage(driver) # Instantiates the page object using the shared driver.

    # Iterates through key menu items and validates both visibility and clickability.
    for item in ["Courses", "LIVE Classes", "Practice", "Resources", "Products"]:
        assert page.is_menu_item_visible_and_clickable(item), f"{item} is not visible or clickable"