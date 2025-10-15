from guvi_automation.drivers.error_handler import capture_error
from guvi_automation.utils.locators import LOCATORS
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BasePage:
    # Initializes the page object with a WebDriver instance and loads locator dictionary for BasePage
    def __init__(self, driver):
        self.driver = driver
        self.locators = LOCATORS["BasePage"]  #  Centralized locator mapping for modularity

    # Navigates to a given URL
    def navigate_to(self, url):
        try:
            self.driver.get(url)   #  Direct navigation
        except Exception as e:
            capture_error(self.driver, "navigation_error")  #  Screenshot for logging on failure

            raise Exception(f"Navigation failed: {e}")

    # Checks visibility of login button
    def is_base_login_button_visible(self):
        return self.driver.find_element(*self.locators["base_login_button"]).is_displayed()

    #  Verifies login button is interactable - uses explicit wait and exception
    def is_base_login_button_clickable(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.locators["base_login_button"])
            )
            return element.is_displayed() and element.is_enabled()
        except Exception as e:
            print(f"Login button not clickable: {e}")
            capture_error(self.driver, "base_login_button_clickable_error")
            return False

    # Clicks login button only if safe. Raises exception on failure
    def click_base_login_button(self):
        if self.is_base_login_button_clickable():
            self.driver.find_element(*self.locators["base_login_button"]).click()
        else:
            capture_error(self.driver, "base_login_button_not_clickable")
            raise Exception("Login button is not clickable")

    # Signup button methods - Checks visibility of signup button. Gracefully handles missing element.
    def is_signup_button_visible(self):
        try:
            return self.driver.find_element(*self.locators["signup_button"]).is_displayed()
        except Exception as e:
            print(f"Sign-Up button not found: {e}")
            return False

    # Waits for signup button to be clickable
    def is_signup_button_clickable(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.locators["signup_button"])
            )
            return True
        except:
            return False

    # Attempts to click signup button.
    def click_signup_button(self):
        try:
            self.driver.find_element(*self.locators["signup_button"]).click()
            return True
        except Exception as e:
            print(f"Sign-Up button not found: {e}")
            return False

    # Menu item methods
    def is_menu_item_visible_and_clickable(self, item_name):
        locator = self.locators["menu_items"].get(item_name)    # Dynamically resolves locator from dictionary
        if not locator:
            raise ValueError(f"No locator defined for menu item: {item_name}")

        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(locator)
            )
            return element.is_displayed() and element.is_enabled() # Validates menu item visibility and interactivity
        except Exception as e:
            print(f"Error checking menu item '{item_name}': {e}")
            return False

    # Dobby Assistant methods
    def click_dobby_assistant_widget_chatbot(self):
        try:
            elements = WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located(self.locators["dobby_welcome"])
            )
            for el in elements:
                if el.is_displayed() and el.is_enabled(): #  Iterates through multiple Dobby elements to find a clickable one.
                    el.click()
                    print("Clicked Dobby welcome message")
                    return True
            print("No visible/clickable Dobby welcome message found")
            return False
        except Exception as e:
            print(f"Error clicking Dobby welcome message: {e}")
            return False

    #  Checks visibility of Dobby widget.
    def is_dobby_welcome_visible(self):
        try:
            element = self.driver.find_element(*self.locators["dobby_welcome"])
            return element.is_displayed()
        except Exception as e:
            print(f"Dobby welcome message not found: {e}")
            return False