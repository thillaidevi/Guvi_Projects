"""
Initializes WebDriver instances for supported browsers: Chrome, Firefox, Edge, and Safari.
Includes browser-specific options and platform checks to ensure compatibility.
Used by test runner scripts to abstract browser setup logic.
"""
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

def create_driver(browser_name):
    """
        Creates and returns a WebDriver instance based on the specified browser name.

        Args:
            browser_name (str): Name of the browser to initialize ("chrome", "firefox", "edge", "safari")

        Returns:
            WebDriver: Initialized browser driver instance

        Raises:
            ValueError: If an unsupported browser name is provided
            Exception: If Safari is requested on a non-macOS system
    """

    browser = browser_name.lower()   # Normalize input for case-insensitive matching

    if browser == "chrome":
        # Configure Chrome options
        options = ChromeOptions()
        # Headed by default
        return webdriver.Chrome(service=ChromeService(), options=options)

    elif browser == "firefox":
        # Configure Firefox options
        options = FirefoxOptions()

        # Headed by default
        return webdriver.Firefox(service=FirefoxService(), options=options)

    elif browser == "edge":
        # Configure Edge options
        options = EdgeOptions()
        return webdriver.Edge(service=EdgeService(), options=options)

    elif browser == "safari":
        # Safari is only supported on macOS
        if platform.system() != "Darwin":
            raise Exception("Safari is only supported on macOS")
        return webdriver.Safari()  # Headed by default

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")