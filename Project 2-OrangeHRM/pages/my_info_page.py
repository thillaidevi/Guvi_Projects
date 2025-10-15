from project_orangehrm_playwright.utils.logger import get_logger
from project_orangehrm_playwright.utils.locators import MY_INFO_LOCATORS, MY_INFO_NAV

logger = get_logger()

class MyInfoPage:
    def __init__(self, page):
        self.page = page

    def capture_tab_screenshot(self, tab_key, status="failure"):
        """
            Captures a screenshot for the given tab and status.
            Used for diagnostics when tab validation fails.
        """
        path = f"screenshots/{tab_key}_{status}.png"
        self.page.screenshot(path=path)

    def navigate_to_my_info(self):
        """
            Navigates to the 'My Info' section from the sidebar.
            Retries up to 3 times if the tab is not immediately visible.
        """
        for attempt in range(3):
            try:
                locator = self.page.get_by_text("My Info", exact=True)
                locator.wait_for(state="visible", timeout=3000)
                locator.click()
                return True
            except Exception as e:
                logger.warning(f"Retry {attempt + 1} failed: {e}")
                self.page.wait_for_timeout(1000)

    def validate_tab(self, tab_key):
        """
            Validates that a specific tab under 'My Info' is loaded.
            Checks both menu and header locators from MY_INFO_LOCATORS.
        """
        tab = MY_INFO_LOCATORS.get(tab_key)
        if not tab or not isinstance(tab, dict) or "menu" not in tab or "header" not in tab:
            logger.warning(f"Invalid locator structure for tab: {tab_key}")
            return False

        try:
            self.page.locator(tab["menu"]).click()
            self.page.wait_for_timeout(1000)
            self.page.locator(tab["header"]).wait_for(state="visible", timeout=7000)
            assert self.page.locator(tab["header"]).is_visible(), f"{tab_key} header not visible"
            logger.info(f" {tab_key} tab loaded successfully")
            return True
        except Exception as e:
            logger.error(f"[✗] Failed to validate tab '{tab_key}': {e}")
            self.capture_tab_screenshot(tab_key)
            return False

    def is_menu_item_present(self, item_key):
        """
            Checks if a specific menu item under 'My Info' is present and visible.
        """
        tab = MY_INFO_LOCATORS.get(item_key)
        if not tab or not isinstance(tab, dict):
            logger.warning(f"Locator missing or invalid for key: {item_key}")
            return False

        locator = self.page.locator(tab["menu"])
        try:
            locator.wait_for(state="visible", timeout=5000)
            return locator.is_visible()
        except Exception as e:
            logger.error(f"Error checking visibility for '{item_key}': {e}")
            return False

    def click_menu_item(self, item_key):
        """
            Clicks a menu item under 'My Info' using its locator key.
            Captures screenshot on failure.
        """
        tab = MY_INFO_LOCATORS.get(item_key)
        if tab and isinstance(tab, dict):
            try:
                self.page.locator(tab["menu"]).click()
                logger.info(f"Clicked menu item: {item_key}")
            except Exception as e:
                logger.error(f"Failed to click menu item '{item_key}': {e}")
                self.capture_tab_screenshot(item_key)

    def is_section_loaded(self, item_key, retries=3):
        """
            Verifies that a section's header is visible after clicking its menu item.
            Retries up to `retries` times before failing.
        """
        tab = MY_INFO_LOCATORS.get(item_key)
        if tab and isinstance(tab, dict):
            locator = self.page.locator(tab["header"])
            for attempt in range(retries):
                try:
                    locator.wait_for(state="visible", timeout=3000)
                    if locator.is_visible():
                        logger.info(f"Section '{item_key}' loaded")
                        return True
                except:
                    self.page.wait_for_timeout(500)
            logger.warning(f"Section '{item_key}' not loaded after retries")
        return False