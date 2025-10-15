from guvi_automation.utils.logger import logger,log_result_json
from guvi_automation.drivers.driver_factory import create_driver
import pytest,pytest_html,os,json
from datetime import datetime
from selenium import webdriver
from pytest_html import extras

# Initialize pytest-html plugin
def pytest_configure(config):
    global pytest_html
    pytest_html = config.pluginmanager.getplugin("html")

#  Enables flexible cross-browser execution
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests on")

# Session-scoped fixture that retrieves the browser name from CLI options
@pytest.fixture(scope="session")
def browser_name(request):
    return request.config.getoption("--browser")

# Function-based driver fixture
@pytest.fixture(scope="function")
def driver(request, browser_name): # Initializes a new browser instance for each test function

    driver = create_driver(browser_name)
    # Dynamically creates the WebDriver based on the CLI --browser option

    driver.get("https://www.guvi.in/") # Navigates to the base URL
    driver.maximize_window()

    yield driver #  Yields control to the test function. Keeps setup and teardown cleanly separated
    driver.quit()  # Gracefully shuts down the browser after test execution


"""- Pytest hook that intercepts the test report generation phase.
 The hookwrapper=True allows you to wrap the default behavior and inject custom logic — 
 perfect for post-test actions like screenshot capture.
"""

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        screenshot_path = None
        driver = item.funcargs.get("driver", None)

        if driver:
            os.makedirs("screenshots", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            status = "PASSED" if report.passed else "FAILED"
            screenshot_path = f"screenshots/{item.name}_{status}_{timestamp}.png"
            driver.save_screenshot(screenshot_path)

        # Log to JSON and rotating log
        log_result_json(report.nodeid, report.outcome, screenshot_path)
        logger.info(f"{report.nodeid} - {report.outcome} - Screenshot: {screenshot_path}")

        # Attach to HTML report
        try:
            if screenshot_path and os.path.exists(screenshot_path):
                extra = getattr(report, "extra", [])
                extra.append(extras.image(screenshot_path, name="Image"))
                report.extra = extra
        except Exception as e:
            logger.error(f"Error attaching screenshot to report: {e}")


# Adds a custom column header titled “Screenshot” to the HTML report table.
def pytest_html_results_table_header(cells):
    cells.insert(2, '<th>Screenshot</th>')

# Embed screenshot thumbnail in HTML report row
def pytest_html_results_table_row(report, cells):
    if hasattr(report, "extra"):
        for extra in report.extra:
            if isinstance(extra, dict) and extra.get("name") == "Image":
                img_html = f'<a href="{extra["content"]}" target="_blank"><img src="{extra["content"]}" width="200"/></a>'
                cells.insert(2, img_html)


# Log to plain text file
def pytest_runtest_logreport(report):
    if report.when == "call":
        status = "PASSED" if report.passed else "FAILED"

        # Ensure the directory exists
        os.makedirs("tests", exist_ok=True)

        with open("tests/test_execution.log", "a") as f:
            f.write(f"{report.nodeid} - {status}\n")







