import pytest
import json
from project_orangehrm_playwright.pages.login_page import LoginPage
from project_orangehrm_playwright.pages.dashboard_page import DashboardPage
from project_orangehrm_playwright.pages.pim_page import PIMPage
from project_orangehrm_playwright.pages.admin_page import AdminPage
from project_orangehrm_playwright.pages.admin_user_management_page import AdminUserManagementPage
from project_orangehrm_playwright.utils.logger import get_logger

# Logger setup for traceability
logger = get_logger("New User Validation in Admin list")

# Load test data from JSON file
with open("C:\\Users\\Rajesh C\\PycharmProjects\\Guvi_Projects\\project_orangehrm_playwright\\data\\users.json") as f:
    data = json.load(f)

# Admin credentials
admin_data = data.get("login_page", {}).get("admin", {})

# New employee details for creation and login
user_data =  data["admin_page"]["new_user"]
employee_admin_data = data["admin_page"]["new_user"]
employee_login_data = data["login_page"]["new_user"]

@pytest.mark.smoke
@pytest.mark.edge
def test_validate_created_user_in_admin_list(edge_page, logger):
    """
        Smoke Test: Validates that a newly created employee and user account appears in the Admin user list.
        Performs soft validation via search filters.
    """
    # Initialize page objects
    page = edge_page
    logger = get_logger("AdminTest")
    login = LoginPage(page, logger)
    admin = AdminPage(page)
    dashboard = DashboardPage(page, logger)
    pim = PIMPage(page, logger)
    admin_mgt = AdminUserManagementPage(page)

    # Step 1: Login as Admin
    logger.info(" Logging in as Admin")
    login.enter_credentials(admin_data["Username"], admin_data["Password"])
    login.submit()

    # Step 2: Add Employee via PIM
    logger.info(f" Adding new employee: {user_data['Employee']}")
    first_name, last_name = user_data["Employee"].split(" ", 1)
    pim.add_employee(first_name, last_name)

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

    # Step 4: Verify User appears in Admin list (soft validation)
    admin.search_user_by_filters(
        username=employee_admin_data["Username"],
        role=employee_admin_data["Role"],
        employee_name=employee_admin_data["Employee"],
        status=employee_admin_data["Status"]
    )

    # Log confirmation
    logger.info(f" New employee '{employee_admin_data['Username']}' confirmed in system users list via soft validation")