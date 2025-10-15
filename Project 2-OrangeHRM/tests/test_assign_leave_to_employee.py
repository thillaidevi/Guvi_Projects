import json
import pytest
from playwright.sync_api import Page, expect
from project_orangehrm_playwright.pages.login_page import LoginPage
from project_orangehrm_playwright.pages.leave_entitlement_page import LeaveEntitlementPage
from project_orangehrm_playwright.pages.assign_leave_page import AssignLeavePage
from project_orangehrm_playwright.pages.leave_report_page import LeaveReportPage
from project_orangehrm_playwright.utils.logger import get_logger
from project_orangehrm_playwright.pages.dashboard_page import DashboardPage
from project_orangehrm_playwright.pages.pim_page import PIMPage
from project_orangehrm_playwright.pages.admin_page import AdminPage
from project_orangehrm_playwright.utils.locators import LeaveReportLocators

# Logger setup for traceability
logger = get_logger("LeaveAssignment")

# Load test data from JSON file
with open("C:\\Users\\Rajesh C\\PycharmProjects\\Guvi_Projects\\project_orangehrm_playwright\\data\\users.json") as f:
    data = json.load(f)

# Admin credentials
admin_data = data.get("login_page", {}).get("admin", {})

# Leave-related data
leave_data = data.get("leave_page", {})
entitlement_data = leave_data.get("entitlement", {})
assign_data = leave_data.get("assign_leave", {})

# Employee data for creation
employee_admin_data = data["admin_page"]["new_user"]

employee_admin_data["Username"] = "testuser"

employee_admin_data["Password"] = "secure@123"

def test_assign_leave_and_validate_report(page: Page):
    # Step 1: Login as Admin
    login = LoginPage(page, logger)
    login.enter_credentials(admin_data["Username"], admin_data["Password"])
    login.submit()
    expect(page.locator("h6:has-text('Dashboard')")).to_be_visible(timeout=5000)

    # Step 2: Add Employee via PIM
    dashboard = DashboardPage(page, logger)
    dashboard.click_pim_module()
    first_name, last_name = employee_admin_data["Employee"].split(" ", 1)
    pim = PIMPage(page, logger)
    pim.add_employee(first_name, last_name)

    # Step 3: Assign Leave Entitlement
    dashboard.click_leave_tab_from_dashboard()
    entitlement_page = LeaveEntitlementPage(page, logger)
    entitlement_page.go_to_add_entitlement()
    entitlement_page.assign_entitlement_for_employee(
        employee_name=entitlement_data["employee"],
        leave_type=entitlement_data["leaveType"],
        leave_period=entitlement_data["leavePeriod"],
        days=entitlement_data["entitlement"]
    )

    # Step 4: Assign Leave
    assign_page = AssignLeavePage(page, logger)
    assign_page.navigate_to_assign_leave()
    assign_page.assign_leave_from_json(assign_data)

    # Step 5:
    leave_report = LeaveReportPage(page, logger)
    leave_report.navigate_to_leave_entitlement_report()
    leave_report.select_leave_type_filter("CAN - Vacation")

    employee_name = "Thillai Devi K"

    leave_report.validate_employee_leave_report(employee_name)




