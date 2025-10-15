import pytest
from guvi_automation.pages.base_page import BasePage

# Smoke test fixtures - test as part of the smoke suite — ideal for quick validation
@pytest.mark.smoke
@pytest.mark.chrome
# Tags the test for chrome browser execution — great for cross-browser filtering.

def test_url_is_valid(driver):  # Assumes a fixture is injecting the WebDriver instance

    url = "https://www.guvi.in"  # Target URL for validation

    base_page = BasePage(driver) # Initializes the page object model with the shared driver instance.

    base_page.navigate_to(url)  # Encapsulated navigation method.

    assert "GUVI" in driver.title or driver.current_url.startswith(url), "URL did not load correctly"
    # Validates that the page loaded successfully by checking title or URL.