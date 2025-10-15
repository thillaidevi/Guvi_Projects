from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from guvi_automation.pages.base_page import BasePage
from guvi_automation.utils.locators import LOCATORS

# Initializes the login page object with driver and locator dictionary.
class LoginPage(BasePage): # Inherits reusable methods from BasePage
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.locators = LOCATORS["LoginPage"]  # Scoped locator mapping for login page

    #  Navigates to login page via homepage.
    def open_login_page(self):
        self.driver.get("https://www.guvi.in")
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.locators["login_submit_button"])
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.url_to_be("https://www.guvi.in/sign-in/")
        )

    #  Inputs email into textbox
    def enter_email(self, email):
        self.driver.find_element(*self.locators["email_textbox"]).send_keys(email)

    # Inputs password to the textbox
    def enter_password(self, password):
        self.driver.find_element(*self.locators["password_textbox"]).send_keys(password)

    #  Submits login form
    def click_login_submit(self):
        self.driver.find_element(*self.locators["login_submit_button"]).click()

    #  Executes full login flow for valid credentials
    def login_functionality_valid_user(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        time.sleep(10)  # Static wait
        self.click_login_submit()
        return self.is_login_successful()

    # Verifies login success by checking for dashboard element.
    def is_login_successful(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.locators["my_courses_element"])
            )
            return True
        except TimeoutException:
            self.driver.save_screenshot("login_failure.png") #  Screenshot on failure
            return False

    # Validates error message for failed login
    def assert_login_failed_with_error(self):
        try:
            error_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.locators["invalid_feedback"])
            )
            assert error_element.is_displayed(), "Error message not displayed" #  Raises assertion if error message is missing
            print(f"Login failed as expected. Message: {error_element.text}")
        except Exception as e:
            self.driver.save_screenshot("invalid_login_failure.png")  #  Screenshot on failure
            raise AssertionError("Login did not fail as expected or error message missing") from e


