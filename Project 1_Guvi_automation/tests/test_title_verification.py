import pytest
from guvi_automation.drivers.driver_factory import create_driver

# Tags the test for chrome browser execution — great for cross-browser filtering.
@pytest.mark.chrome
def test_guvi_title(driver):  # Assumes a fixture is injecting the WebDriver instance

    # Defines the expected title string.
    expected_title = "GUVI | Learn to code in your native language"

    #  Navigates to the GUVI homepage
    driver.get("https://www.guvi.in/")

    actual_title = driver.title #  Captures the current page title
    assert actual_title == expected_title, f"Expected '{expected_title}', but got '{actual_title}'"
    # Validates the page title against the expected value.