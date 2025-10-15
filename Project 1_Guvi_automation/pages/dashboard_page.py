from guvi_automation.pages.login_page import LoginPage
from guvi_automation.pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from guvi_automation.utils.locators import LOCATORS


class DashboardPage:
    #  Initializes the page object with WebDriver and scoped locators.
    def __init__(self, driver):
        self.driver = driver
        self.locators = LOCATORS["DashboardPage"]

    #  Waits for the profile menu to be clickable before initiating logout flow.
    def logout(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.locators["profile_menu"])
            ).click() #  Ensures profile menu is interactable before clicking

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.locators["logout_button"])
            ).click()  #  Explicit wait for logout button

            # Wait for redirect to complete
            WebDriverWait(self.driver, 10).until(EC.url_changes(self.driver.current_url))
            return True
        # Exception arises when logout got failed
        except Exception as e:
            print(f"Logout failed: {e}")
            return False

    # Validates the logout by checking URL.
    def is_logged_out(self):
        def is_logged_out(self):
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.url_to_be("https://www.guvi.in/")
                )
                # Optional DOM check for login button
                return self.driver.find_element(*self.locators["login_button"]).is_displayed()
            except TimeoutException:
                print(f"Post-logout URL mismatch: {self.driver.current_url}")
                return False










