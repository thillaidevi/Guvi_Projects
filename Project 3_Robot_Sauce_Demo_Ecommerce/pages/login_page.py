from robot.libraries.BuiltIn import BuiltIn

class LoginPage:

    def __init__(self, seleniumlib):
        # Initialize with SeleniumLibrary instance for browser interactions
        self.seleniumlib = seleniumlib

    def open(self):
        # Launch the SauceDemo login page in Edge browser
        self.seleniumlib.open_browser("https://www.saucedemo.com", browser="edge")

        # Maximize browser window for full visibility
        self.seleniumlib.maximize_browser_window()

        # Wait until login page is fully loaded
        self.wait_for_login_page()

    def login(self, username, password):
        # Wait for username field to be visible before interacting
        self.seleniumlib.wait_until_element_is_visible("id=user-name", timeout="10s")

        # Enter username and password
        self.seleniumlib.input_text("id=user-name", username)
        self.seleniumlib.input_text("id=password", password)

        # Click the login button
        self.seleniumlib.click_button("id=login-button")

        # Handle browser alert (if any)
        try:
            self.seleniumlib.handle_alert()
        except Exception:
            pass  # No browser alert present

        # Handle browser-level alert if it appears (e.g., password change popup)
        try:
            self.seleniumlib.wait_until_element_is_visible("css=button.cancel-button", timeout="5s")
            self.seleniumlib.click_button("css=button.cancel-button")
            print(" Modal dismissed")
        except Exception:
            print(" No modal appeared")

        # Wait for dashboard to appear
        self.seleniumlib.wait_until_page_contains_element("class=inventory_list", timeout="15s")

    def wait_for_login_page(self):
        # Wait until login page is fully loaded and username field is visible
        self.seleniumlib.wait_until_page_contains_element("id=user-name", timeout="10s")

    def is_error_visible(self):
        # Check if login error message is displayed
        self.seleniumlib.page_should_contain_element("xpath=//h3[@data-test='error']")




