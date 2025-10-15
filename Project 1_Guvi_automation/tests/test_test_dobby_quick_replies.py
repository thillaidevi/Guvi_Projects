from guvi_automation.pages.base_page import BasePage
import time
import pytest

# Tags the test for chrome browser execution — great for cross-browser filtering.
@pytest.mark.chrome
def test_dobby_assistant_presence(driver):  # Assumes a fixture is injecting the WebDriver instance
    base = BasePage(driver)  # Initializes the page object model with the shared driver instance.

    time.sleep(25)

    base.click_dobby_assistant_widget_chatbot() # Triggers the chatbot widget via encapsulated page method.

    assert base.is_dobby_welcome_visible(), "Dobby welcome message not visible"
    # Verifies that the welcome message appears after interaction.




