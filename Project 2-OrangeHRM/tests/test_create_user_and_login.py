import pytest
import json
from project_orangehrm_playwright.pages.login_page import LoginPage
from project_orangehrm_playwright.pages.dashboard_page import DashboardPage
from project_orangehrm_playwright.pages.pim_page import PIMPage
from project_orangehrm_playwright.pages.admin_page import AdminPage
from project_orangehrm_playwright.utils.logger import get_logger

# Load test data from JSON file
with open("C:\\Users\\Rajesh C\\PycharmProjects\\Guvi_Projects\\project_orangehrm_playwright\\data\\users.json") as f:
    data = json.load(f)

# Admin credentials
admin_data = data["login_page"]["admin"]

# New employee login credentials
employee_login_data = data["login_page"]["new_user"]

# New employee details for creation
employee_admin_data = data["admin_page"]["new_user"]

@pytest.mark.smoke
@pytest.mark.edge
def test_create_user_and_login(edge_page, logger, create_user_and_login):
    """
    Validates that a newly created user can log in successfully.
    Uses the create_user_and_login fixture to provision and authenticate the user.
    """
    creds = create_user_and_login  # Fixture returns dict with Username, Password, Employee

    # Assert login was successful (already done in fixture)
    logger.info(f" User '{creds['Username']}' logged in successfully after creation")