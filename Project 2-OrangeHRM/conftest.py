import os
import pytest, re
from datetime import datetime
import json
from playwright.sync_api import sync_playwright
from project_orangehrm_playwright.utils.logger import get_logger
from project_orangehrm_playwright.pages.login_page import LoginPage
from project_orangehrm_playwright.pages.dashboard_page import DashboardPage
from project_orangehrm_playwright.pages.pim_page import PIMPage
from project_orangehrm_playwright.pages.admin_page import AdminPage
from _pytest.runner import CallInfo
from pytest_html import extras

#---------Capturing the HTML plugin for later use in screenshot reporting---------------------------------------
def pytest_configure(config):
    import os
    from datetime import datetime

    global pytest_html
    pytest_html = config.pluginmanager.getplugin('html')

    # Detect marker from CLI args
    active_markers = ["chrome", "firefox", "edge", "smoke"]
    selected_marker = next((m for m in active_markers if m in config.args), "consolidated")

    # Create directory for this marker
    report_dir = os.path.join("reports", selected_marker)
    os.makedirs(report_dir, exist_ok=True)

    # Timestamped report name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = f"{selected_marker}_{timestamp}.html"

    # Set final report path
    config.option.htmlpath = os.path.join(report_dir, report_name)

# --------------------Fixture: Shared logger --------------------------------------------------------------------------
@pytest.fixture(scope="session")
def logger():
    return get_logger("FrameworkLogger")

# -------------------- CLI Options ----------------------------------------------------------------------------
# Hook: Add custom CLI options for browser selection and headed mode

def pytest_addoption(parser):
    parser.addoption("--target-browser", default="chromium", help="Choose browser: chromium, firefox, webkit")
    parser.addoption("--run-headed", action="store_true", help="Run browser in headed mode")

# --------------------  Fixture: Playwright instance -------------------------------------------------------------------
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

# -------------------- Default Browser Fixture -----------------------------------------------------------------------
# Fixture: Launch default browser based on CLI options
@pytest.fixture(scope="session")
def browser(playwright_instance, pytestconfig, logger):
    browser_type = pytestconfig.getoption("target_browser")
    headed = pytestconfig.getoption("run_headed")
    logger.info(f"Launching browser: {browser_type}, headed mode: {headed}")
    browser = getattr(playwright_instance, browser_type).launch(headless=not headed, slow_mo=300)
    yield browser
    browser.close()

#--------------------Edge Browser Fixture-------------------------------------------------------------------------
#  Fixture: Launch Edge browser explicitly
@pytest.fixture(scope="function")
def edge_browser(playwright_instance, pytestconfig, logger):
    headed = pytestconfig.getoption("run_headed")
    logger.info(f" Launching Edge browser | Headed: {headed}")
    browser = playwright_instance.chromium.launch(channel="msedge", headless=not headed, slow_mo=300)
    yield browser
    browser.close()
    logger.info(" Edge browser closed")

#----------------------Edge page fixture----------------------------------------------------------------------
# Fixture: Create Edge browser context and navigate to login page
@pytest.fixture(scope="function")
def edge_page(edge_browser):
    # Ensure screenshot and log directories exist
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    # Create browser context with locale and clean cookies
    context = edge_browser.new_context(locale="en-US")
    context.clear_cookies()
    page = context.new_page()

    try:
        # Navigate to login page and wait for username field
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        page.wait_for_load_state("domcontentloaded")
        page.locator("input[name='username']").wait_for(state="visible", timeout=10000)

    except Exception as e:
        #  Capture screenshot and DOM dump on failure
        page.screenshot(path="screenshots/edge_login_error.png")
        with open("logs/edge_login_dom_dump.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        raise Exception(f"Edge login page setup failed: {e}")
    yield page
    context.close()

# -------------------- Page Fixture ----------------------------------------------------------------------------
@pytest.fixture(scope="function")
def page(browser):
    # Ensure screenshot and log directories exist
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    # Create a fresh browser context with English locale
    context = browser.new_context(locale="en-US")
    context.clear_cookies()
    page = context.new_page()

    try:

        # Navigate to login page and wait for username field
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        page.wait_for_load_state("domcontentloaded")  # Faster and more stable for login pages
        page.locator("input[name='username']").wait_for(state="visible", timeout=10000)

    except Exception as e:

        # Capture screenshot and DOM dump on failure
        page.screenshot(path="screenshots/login_page_error.png")
        with open("logs/login_dom_dump.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        raise Exception(f"Login page setup failed: {e}")

    yield page
    context.close()

# ------------------Logged_in_context Fixture----------------------
@pytest.fixture(scope="function")
def logged_in_context(page, logger):

    # Initialize login page object
    login = LoginPage(page, logger)

    # Load admin credentials from JSON
    with open("C:\\Users\\Rajesh C\\PycharmProjects\\Guvi_Projects\\project_orangehrm_playwright\\data\\users.json") as f:
        data = json.load(f)
    creds = data["login_page"]["admin"]

    #  Perform login
    login.load()
    login.enter_credentials(creds["Username"], creds["Password"])
    login.submit()
    assert login.is_logged_in(), " Admin login failed"
    return page

# -------------------- Test Setup & Screenshots --------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Get the test result
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    if rep.when != "call":
        return

    # Get page and logger from test context
    page = item.funcargs.get("page") or item.funcargs.get("edge_page")
    logger = item.funcargs.get("logger", None)

    if not page or not logger:
        return

    # Get pytest-html plugin
    pytest_html = item.config.pluginmanager.getplugin("html")
    if not pytest_html:
        logger.warning(" pytest-html plugin not found — cannot attach screenshot")
        return

    # Build screenshot path
    test_name = item.name
    suite_name = re.sub(r'[^\w\-_.]', '_', item.nodeid.split("::")[0])
    status = rep.outcome  # 'passed', 'failed', or 'skipped'
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    screenshot_dir = os.path.join("reports", "screenshots", suite_name)
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_filename = f"{test_name}_{status}_{timestamp}.png"
    screenshot_path = os.path.join(screenshot_dir, screenshot_filename)

    # Capture screenshot
    try:
        page.screenshot(path=screenshot_path, full_page=True)
        logger.info(f" Screenshot captured: {screenshot_path}")
    except Exception as e:
        logger.warning(f" Screenshot failed: {e}")
        return

    # Compute relative path from report location
    html_path = getattr(item.config.option, "htmlpath", "reports/report.html")
    relative_path = os.path.relpath(screenshot_path, start=os.path.dirname(html_path))

    # Attach screenshot to HTML report
    extra = getattr(rep, "extra", [])
    extra.append(extras.image(relative_path))
    rep.extras = extra

#---------------------Fixture — Full Admin Flow---------------------------------------
@pytest.fixture(scope="function")
def create_user_and_login(page, logger):
    """
    Creates a new employee and user via admin flow, logs in as the new user,
    and returns their credentials for use in dependent tests.
    """
    #  Initialize page objects
    login = LoginPage(page, logger)
    dashboard = DashboardPage(page, logger)
    pim = PIMPage(page, logger)
    admin = AdminPage(page, logger)

    # Load test data
    with open("C:\\Users\\Rajesh C\\PycharmProjects\\Guvi_Projects\\project_orangehrm_playwright\\data\\users.json") as f:
        data = json.load(f)

    admin_data = data["login_page"]["admin"]
    employee_login_data = data["login_page"]["new_user"]
    employee_admin_data = data["admin_page"]["new_user"]

    # Step 1: Admin Login
    login.load()
    login.enter_credentials(admin_data["Username"], admin_data["Password"])
    login.submit()
    assert login.is_logged_in(), " Admin login failed"

    # Step 2: Add Employee via PIM
    dashboard.click_pim_module()
    first_name, last_name = employee_admin_data["Employee"].split(" ", 1)
    pim.add_employee(first_name, last_name)
    logger.info(f" Employee '{first_name} {last_name}' added successfully")

    # Step 3: Create New User via Admin module

    dashboard.click_admin_tab()
    admin.click_add_user_button()
    admin.create_user_save(
        username=employee_admin_data["Username"],
        password=employee_admin_data["Password"],
        confirm_password=employee_admin_data["ConfirmPassword"],
        role=employee_admin_data["Role"],
        employee_name=employee_admin_data["Employee"],
        status=employee_admin_data["Status"]
    )

    # Step 4: Verify User Creation
    admin.search_user_by_filters(
        username=employee_admin_data["Username"],
        role=employee_admin_data["Role"],
        employee_name=employee_admin_data["Employee"],
        status=employee_admin_data["Status"]
    )

    # Step 5: Logout Admin
    admin.logout_user()

    # Step 6: Login as New User
    login.enter_credentials(employee_login_data["Username"], employee_login_data["Password"])
    login.submit()
    assert login.is_logged_in(), " New user login failed"
    logger.info(" New user login verified successfully")

    #  Return credentials for downstream tests
    return {
        "Username": employee_login_data["Username"],
        "Password": employee_login_data["Password"],
        "Employee": employee_admin_data["Employee"]
    }
