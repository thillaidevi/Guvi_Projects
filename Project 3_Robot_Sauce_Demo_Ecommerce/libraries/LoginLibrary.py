from robot.api.deco import keyword
from pages.login_page import LoginPage
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.by import By
from random import sample

class LoginLibrary:
    def __init__(self):
        # Initialize SeleniumLibrary and bind it to the LoginPage object
        self.seleniumlib = BuiltIn().get_library_instance('SeleniumLibrary')
        self.page = LoginPage(self.seleniumlib)

    @keyword(name="Open Browser To Login Page")
    def open_browser_to_login_page(self):
        # Launch the browser and navigate to the login page
        self.page.open()

    @keyword(name="Login And Validate")
    def login_and_validate(self, username, expectation):

        # Step 1: Enter credentials
        self.seleniumlib.wait_until_element_is_visible("id=user-name", timeout="10s")
        self.seleniumlib.input_text("id=user-name", username)
        self.seleniumlib.input_text("id=password", "secret_sauce")
        self.seleniumlib.click_button("id=login-button")

        # Step 2: Handle browser alert (if any)
        try:
            self.seleniumlib.handle_alert(action="DISMISS")
            print(f" Alert dismissed for user: {username}")
        except Exception:
            print(f" No alert for user: {username}")

        # Step 3: Handle modal (if any)
        try:
            self.seleniumlib.wait_until_element_is_visible("css=button.cancel-button", timeout="5s")
            self.seleniumlib.click_button("css=button.cancel-button")
            print(f" Modal dismissed for user: {username}")
        except Exception:
            print(f" No modal appeared for user: {username}")

        # Step 4: Validate outcome based on expectation
        if expectation == "EXPECT_SUCCESS":
            if username == "performance_glitch_user":

                # Retry logic for laggy user
                for attempt in range(5):
                    try:
                        self.seleniumlib.wait_until_page_contains_element("class=inventory_list", timeout="7s")
                        print(f" Dashboard appeared for user: {username} on attempt {attempt + 1}")
                        return
                    except Exception:
                        print(f" Attempt {attempt + 1} failed for user: {username}, retrying...")
                raise Exception(f" Dashboard not visible for user: {username} after retries")
            else:

                # Standard wait for other users
                self.seleniumlib.wait_until_page_contains_element("class=inventory_list", timeout="10s")
                print(f" Dashboard visible for user: {username}")

        elif expectation == "EXPECT_ERROR":

            # Validate locked-out error message
            self.seleniumlib.page_should_contain_element("css=h3[data-test='error']")
            self.seleniumlib.element_text_should_be(
                "css=h3[data-test='error']",
                "Epic sadface: Sorry, this user has been locked out."
            )
            print(f" Error message validated for locked out user: {username}")

        else:
            raise Exception(f" Unknown expectation: {expectation}")

    @keyword(name="Wait For Dashboard With Retries")
    def wait_for_dashboard_with_retries(self, username, max_attempts=5, wait_per_attempt="9s"):
        """
        Waits for dashboard visibility with retry logic.
        Useful for laggy users like 'performance_glitch_user'.
        """
        for attempt in range(max_attempts):
            try:
                self.seleniumlib.wait_until_page_contains_element("class=inventory_list", timeout=wait_per_attempt)
                print(f" Dashboard appeared for user: {username} on attempt {attempt + 1}")
                return
            except Exception:
                print(f" Attempt {attempt + 1} failed for user: {username}, retrying...")
        raise Exception(f"Dashboard not visible for user: {username} after {max_attempts} attempts")

    @keyword(name="Dashboard Should Be Visible")
    def dashboard_should_be_visible(self):
        # Check if dashboard is visible using LoginPage method
        self.wait_for_dashboard_with_retries()

    @keyword(name="Reset To Login Page")
    def reset_to_login_page(self):
        # Navigate back to login page and wait for it to load
        self.seleniumlib.go_to("https://www.saucedemo.com")
        self.page.wait_for_login_page()

    @keyword(name="Validate Dashboard If Expected Success")
    def validate_dashboard_if_expected_success(self, username, expectation):
        """
            Validates whether the dashboard is visible or an error message is shown,
            based on the expected login outcome for the given user.
        """

        if expectation == "EXPECT_SUCCESS":
            if username == "performance_glitch_user":

                # Retry logic for users with known performance delays
                self.wait_for_dashboard_with_retries(username)
            else:
                # Standard dashboard visibility check

                self.seleniumlib.wait_until_page_contains_element("class=inventory_list", timeout="10s")
                print(f" Dashboard visible for user: {username}")

        elif expectation == "EXPECT_ERROR":
            try:
                # Wait for error message to appear

                self.seleniumlib.wait_until_page_contains_element("css=h3[data-test='error']", timeout="5s")
                actual_text = self.seleniumlib.get_text("css=h3[data-test='error']")
                expected_texts = [
                    "Epic sadface: Sorry, this user has been locked out.",
                    "Epic sadface: Username and password do not match any user in this service"
                ]

                # Validate error message content
                if actual_text not in expected_texts:
                    raise Exception(f" Unexpected error message: '{actual_text}'")
                print(f" Error message validated for user: {username} → '{actual_text}'")
            except Exception as e:
                # Log current page URL for debugging if error message is missing

                current_url = self.seleniumlib.get_location()
                print(f" Error message not found for user: {username}")
                print(f" Current URL: {current_url}")
                raise Exception(f" Expected error message not found: {str(e)}")

    @keyword(name="Click Logout Button")
    def click_logout_button(self):
        """
            Opens the side menu and clicks the logout button to return to the login screen.
        """

        self.seleniumlib.click_element("id=react-burger-menu-btn")
        self.seleniumlib.wait_until_element_is_visible("id=logout_sidebar_link", timeout="5s")
        self.seleniumlib.click_element("id=logout_sidebar_link")
        print(" Logout button clicked, returning to login screen")

    @keyword(name="Get Random Products")
    def get_random_products(self, elements, count):
        """Returns a random subset of product elements."""
        if len(elements) < count:
            raise ValueError(f" Not enough elements to sample from: found {len(elements)}, need {count}")
        return sample(elements, count)






