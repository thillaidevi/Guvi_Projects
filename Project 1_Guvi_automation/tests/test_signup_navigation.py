import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from guvi_automation.pages.base_page import BasePage

# Tags the test for firefox browser execution — great for cross-browser filtering.
@pytest.mark.firefox
def test_signup_redirect(driver):
    base = BasePage(driver) # Instantiates the page object using the shared driver.

    try:
        base.click_signup_button() # Click the base page's signup button

        expected_url = "https://www.guvi.in/register/"

        #  Wait until URL contains "register"
        WebDriverWait(driver, 30).until(lambda d: "register" in d.current_url)
        """ Waits for the URL to contain "register". Functional, but consider using EC.url_contains("register") 
                 for better readability and alignment with your explicit wait strategy."""

        actual_url = driver.current_url

        #  Final assertion
        assert actual_url == expected_url, f" Expected URL '{expected_url}', but got '{actual_url}'"

    except AssertionError as e:
        base.capture_screenshot("signup_redirect_failure.png")
        raise e

    except Exception as ex:
        base.capture_screenshot("signup_redirect_exception.png")
        raise ex


