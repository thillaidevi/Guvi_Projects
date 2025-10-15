#  Automated Testing of HR Management Web Application

##  Application Under Test
[OrangeHRM Demo Site](https://opensource-demo.orangehrmlive.com)

---

##  Project Objective

The goal of this project is to automate the testing of the OrangeHRM web application by simulating real-world user actions and validating core functionalities. Key modules such as login, menu navigation, user management, leave assignment, and logout are tested to ensure reliability and usability.

---

##  Scope

- Simulate realistic user workflows including login, form submissions, and navigation
- Validate both positive and negative test scenarios
- Ensure cross-browser compatibility
- Use explicit waits and robust locator strategies for UI synchronization
- Log results and capture screenshots for reporting and debugging

---

##  Preconditions

- A structured test suite must be in place
- External data sources (Excel/JSON) should drive credential and user data
- Logging and screenshot capture must be integrated
- Explicit waits should be used for dynamic UI elements

---

##  Test Suite Overview

###  Test-Case-1: Login Validation
- Use multiple credential sets from external data
- Validate login success and failure
- Logout after successful login

###  Test-Case-2: Home URL Accessibility
- Launch browser and navigate to home page
- Confirm page loads without error

###  Test-Case-3: Login Field Visibility
- Check visibility and enablement of username and password fields

###  Test-Case-4: Menu Item Accessibility
- Log in and verify visibility/clickability of main menu items:
  - Admin, PIM, Leave, Time, Recruitment, My Info, Performance, Dashboard

###  Test-Case-5: User Creation and Login
- Create a new user via Admin panel
- Log out and validate login with new user

###  Test-Case-6: Admin User List Verification
- Search for newly created user in Admin > User Management
- Confirm user appears in listing

###  Test-Case-7: Forgot Password Flow
- Click “Forgot your password?” link
- Submit request with registered username/email
- Validate confirmation message and redirection

###  Test-Case-8: My Info Submenu Validation
- Navigate to “My Info” section
- Verify presence and functionality of:
  - Personal Details, Contact Details, Emergency Contacts, etc.

###  Test-Case-9: Assign Leave
- Log in as Admin/HR
- Assign leave to an employee
- Validate success message and leave record entry

###  Test-Case-10: Claim Request Submission
- Log in as employee
- Submit a new claim with required details
- Confirm success message and entry in claim history

---

##  Folder Structure


 project_orangehrm_playwright                 
    |__ data                           # Contains test datas                     
    |    |_ credentials.xlsx
    |    |_ users.json
    
    |__ logs                           # Contains logs
    |
    |__pages                           # Contains Login_page, dashboard_page, admin page, leave page, claim page and other pages associated with these pages
    |    |_ add_expense_popup_page.py
    |    |_ login_page.py
    |    |_ dashboard_page.py
    |    |_ admin_user_management_page.py
    |    |_ assign_leave_page.py	
    |    |_ claim_page.py
    |    |_ create_claim_page.py
    |    |_ employee_claim_page.py
    |    |_ forgot_password_page.py
    |    |_ leave_entitlement_page.py
    |    |_ leave_page.py
    |    |_ my_info_page.py
    |    |_ pim_page.py
    |    |_ submit_claim_page.py
    |    |_ admin_page.py
    |    |_
    |
    |__reports                         # Contains reports based on the browser
    |    |_ report_chrome.html
    |    |_ report_edge.html
    |    |_ report_firefox.html
    |    |_ results.json
    |
    |__screenshots                      # Contains screenshots based on the browser
    |    |_ chrome
    |    |_ firefox
    |    |_ MicrosoftEdge
    |
    |_ tests                            # Test suites contains positive and negative test cases
    |    |_ test_execution.log          # Test execution logs captured 
    |    |_ test_assign_leave_to_employee.py
    |    |_ test_claim_request_by_employee.py
    |    |_ test_create_user_and_login.py
    |    |_ test_dashboard_main_menu_items_visibility_clickability.py
    |    |_ test_forgot_password_flow.py
    |    |_ test_home_url_accessibility.py
    |    |_ test_login.py
    |    |_ test_login_fields_visibility.py
    |    |_ test_my_info_menu_items_validation.py
    |    |_ test_validate_created_user_in_admin_list.py

##  Tools & Technologies

- **Playwright (Python)** for browser automation
- **Pytest** for test execution and parametrization
- **pytest-html** for report generation
- **JSON/Excel** for data-driven testing
- **Custom logger** for structured logging

---
##  Virtual Environment Setup
 Create and Activate Virtual Environment
To isolate dependencies and avoid conflicts with global packages, 
    python -m venv venv  # create a virtual environment
    source venv/bin/activate  # On Windows: venv\Scripts\activate
---
##  Pytest Configuration
pytest.ini
The pytest.ini file defines global settings for test discovery and marker registration.
---
##  Requirements
pip install -r requirements.txt
This ensures an environment is set up with the exact versions used during development and testing.

---
##  Markers for cross browser support and smoke test
@pytest.mark.chrome
@pytest.mark.edge
@pytest.mark.firefox
@pytest.mark.smoke
---

##  How to Run Tests

```bash
pytest --html=reports/report.html --self-contained-html

pytest tests/ --target-browser=chromium --run-headed -m chrome
pytest tests/ --target-browser=chromium --run-headed -m edge
pytest tests/ --target-browser=firefox --run-headed -m firefox
pytest tests/ --target-browser=edge -m "smoke and edge"
pytest tests/ --html=reports/report.html --self-contained-html -m "smoke"

 Reporting & Debugging
- Screenshots are captured on failure
- HTML report includes test status and logs
- DOM dumps available for deep inspection

