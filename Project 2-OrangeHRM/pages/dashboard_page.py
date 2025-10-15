from playwright.sync_api import Page
from guvi_automation.utils.logger import logger
from project_orangehrm_playwright.utils.locators import DASHBOARD_PAGE_LOCATORS
from project_orangehrm_playwright.utils.locators import MY_INFO_NAV
from playwright.sync_api import expect


class DashboardPage:
    def __init__(self, page: Page,logger):
        self.logger = logger
        self.page = page

        #  Wrapper class used to locate sidebar menu items
        self.menu_wrapper_class = DASHBOARD_PAGE_LOCATORS["menu_wrapper_class"]

        # Admin tab locator from external dictionary
        self.admin_tab = page.locator(DASHBOARD_PAGE_LOCATORS["admin_tab"])

        #Claim module tab
        self.claim_module = page.locator("span.oxd-main-menu-item--name", has_text="Claim")

    def wait_until_loaded(self, timeout=5000):
        """"Waits for dashboard header to confirm page load"""
        self.page.wait_for_selector(DASHBOARD_PAGE_LOCATORS["dashboard_header"], timeout=timeout)

    def get_menu_item(self, name: str):
        """Returns locator for a sidebar menu item by visible text"""
        return self.page.locator(f"{self.menu_wrapper_class}:has-text('{name}')")

    def validate_menu_items(self, expected_items: list[str]):
        """
            Validates visibility and clickability of expected dashboard menu items.
            Logs failures and captures screenshots for missing or broken items.
        """
        self.page.wait_for_selector(f"{self.menu_wrapper_class} >> nth=5", timeout=10000)
        menu_items = self.page.locator(self.menu_wrapper_class)
        print(f" Dashboard menu appears stable with {menu_items.count()} items")

        try:
            visible_texts = menu_items.all_inner_texts()
            print(f"[DEBUG] Visible menu items: {visible_texts}")
        except Exception as e:
            print(f"[WARN] Could not fetch menu texts: {e}")

        failed_items = []

        for item in expected_items:
            try:
                print(f" Validating menu item: {item}")
                locator = self.get_menu_item(item)

                locator.wait_for(state="visible", timeout=5000)
                assert locator.is_visible(), f"{item} menu is not visible"
                assert locator.is_enabled(), f"{item} menu is not clickable"

                locator.hover()
                locator.click()
                self.page.wait_for_timeout(500)
                print(f" {item} menu validated successfully")

            except Exception as e:
                self.page.screenshot(path=f"screenshots/{item}_failure.png")
                print(f" Validation failed for {item}: {e}")
                failed_items.append(item)

        if failed_items:
            raise AssertionError(f"Menu validation failed for: {', '.join(failed_items)}")

    def get_logged_in_user(self):
        """Returns the currently logged-in username from the top-right dropdown"""
        user_locator = self.page.locator(DASHBOARD_PAGE_LOCATORS["user_dropdown"])
        return user_locator.text_content().strip()

    def click_pim_module(self):
        """Clicks the PIM module from the sidebar menu."""
        try:
            pim_menu = self.page.get_by_role("link", name="PIM")
            expect(pim_menu).to_be_visible(timeout=5000)
            pim_menu.scroll_into_view_if_needed()
            pim_menu.click()
            expect(self.page.locator("h6:has-text('PIM')")).to_be_visible(timeout=5000)
        except Exception as e:
            self.page.screenshot(path="screenshots/pim_module_click_failed.png")
            raise Exception(f" Failed to click PIM module: {e}")

    def click_admin_tab(self):
        """Clicks the Admin tab and waits for expected URL"""
        self.admin_tab.click()
        self.page.wait_for_url("**/admin/viewSystemUsers")

    def click_my_info_tab(self):
        """Clicks the My Info tab using external locator"""
        try:
            locator = self.page.locator(MY_INFO_NAV["my_info_tab"])
            locator.wait_for(state="visible", timeout=5000)
            locator.click()
            logger.info("Clicked My Info tab")
        except Exception as e:
            logger.error(f"Failed to click My Info tab: {e}")
            self.page.screenshot(path="screenshots/my_info_tab_error.png")

    def click_claim_module(self):
        """Clicks the Claim module tab and waits for page to settle"""

        expect(self.claim_module).to_be_visible(timeout=5000)
        expect(self.claim_module).to_be_enabled()
        self.claim_module.click()
        self.page.wait_for_load_state("networkidle")  # Wait for page to settle
        print(" Claim Tab clicked")

    def click_leave_tab_from_dashboard(self):
        """
        Clicks the Leave tab from the dashboard and waits for the Leave page to load.
        Uses soft validation to avoid brittle URL-based timeouts.
        """
        try:
            leave_tab = self.page.locator("a.oxd-main-menu-item:has-text('Leave')")
            expect(leave_tab).to_be_visible(timeout=5000)
            leave_tab.click()
            self.logger.info(" Leave tab clicked")

            # Soft wait: look for filter form or table to confirm page load
            self.page.wait_for_selector("form.oxd-form", timeout=5000)
            self.logger.info(" Leave page loaded successfully")

        except Exception as e:
            self.logger.error(f" Failed to click Leave tab or load page: {e}")
            self.page.screenshot(path="leave_tab_click_failed.png")
            raise