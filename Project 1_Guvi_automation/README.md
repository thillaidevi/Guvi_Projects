 # Automated Testing Framework for GUVI Web Application https://www.guvi.in
 
##  Project Overview
This project automates UI testing for [GUVI](https://www.guvi.in), an EdTech platform, 
using **Selenium**, **Pytest**, and **Object-Oriented Programming (OOP)** principles. 
It validates core functionalities like login, navigation, and UI elements across multiple browsers.

##  Objectives
- Simulate real user interactions and validate UI behavior
- Ensure cross-browser compatibility (Chrome, Firefox, Edge, Safari)
- Log results, capture screenshots, and generate HTML reports
- Maintain modular, scalable, and reusable test architecture

##  Folder Structure
guvi_automation                    
    |__drivers                        # Contains files for cross browser test and error handlers                     
    |    |_ driver_factory.py
    |    |_ error_handler.py
    |
    |__pages                           # Contains base_page, Login_page and dashboard_page
    |    |_ base_page.py
    |    |_ login_page.py
    |    |_ dashboard_page.py
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
    |    |_ test_execution.log
    |    |_ test_data.json              # Test data 
    |    |_ test_url_validation.py
    |    |_ test_title_verification.py
    |    |_ test_test_dobby_quick_replies.py
    |    |_ test_signup_navigation.py
    |    |_ test_signup_button.py
    |    |_ test_login_with_valid_credentials.py
    |    |_ test_login_with_invalid_credentials.py
    |    |_ test_login_logout_flow.py
    |    |_ test_login_button.py
    |    |_ test_base_page_menu_item.py
    |
    |_ utils                             # Reusable codes maintained under utils to load test data, locators and menu items
    |    |_ data_loader.py  
    |    |_ locators.py
    |    |_ logger.py
    |
    |_ conftest.py                      # Reusable setup/teardown logics, hooks for screenshots in report, methods for function and class level method
    |_ pytest.ini                       # Configuration
    |_ Readme.md                        # Readme file for detailed flow
    |_ requirements.txt                 # Requirements Configuration
    |_ run.py                           # Entry point for executing smoke tests across multiple browsers.
    


##  Key Features
- **Driver Factory**: Centralized browser initialization with support for Chrome, Firefox, Edge, Safari
- **Page Object Model (POM)**: Encapsulated page interactions for maintainability
- **Pytest Hooks**: Logging and screenshot capture for every test case
- **Cross-Browser Execution**: Marker-based test runs with browser-specific HTML reports
- **Error Handling**: Robust exception management for resilient test execution
- **Test suite**: Including both valid (positive) and invalid (negative) test scenarios.


## Test Scenarios
| Test Case   | Description                                                          |
|-------------|----------------------------------------------------------------------|
| TC1         | Validate URL accessibility                                           |
| TC2         | Verify page title                                                    |
| TC3         | Check Login button visibility and clickability                       |
| TC4         | Check Sign-Up button functionality                                   |
| TC5         | Validate Sign-Up redirection                                         |
| TC6         | Login with valid credentials                                         |
| TC7         | Login with invalid credentials                                       |
| TC8         | Validate menu items: Courses, LIVE Classes, Practice                 |
| TC9         | Check presence of Dobby Assistant                                    |
| TC10        | Logout functionality                                                 |


**Virtual Environment Setup**
- Create and Activate Virtual Environment
To isolate dependencies and avoid conflicts with global packages, 
    python -m venv venv  # create a virtual environment
    source venv/bin/activate  # On Windows: venv\Scripts\activate

**Pytest Configuration**
pytest.ini
The pytest.ini file defines global settings for test discovery and marker registration.

**Requirements**
pip install -r requirements.txt
- This ensures an environment is set up with the exact versions used during development and testing.

** Conftest.py Highlights**

🔹 Browser Parameterization
🔹 Driver Fixture
🔹 Screenshot & HTML Report Integration
🔹 Logging Test Results

**### Reporting & Logging**
•	Screenshots captured for both passed and failed tests
•	Logs stored per test case for debugging
•	HTML reports generated with browser-specific details

**##  How to Run Tests**

Smoke Test (Chrome) 

pytest tests/ -m smoke --browser=chrome --html=report_smoke_chrome.html --self-contained-html -v

**Full Test Suite (Chrome)**

pytest tests/ --browser=chrome --html=report_chrome.html --self-contained-html -v 

**Cross-Browser Execution**

 pytest tests/ -m firefox --browser=firefox --html=report_firefox.html --self-contained-html
 pytest tests/ -m edge --browser=edge --html=report_edge.html --self-contained-html

**Test Report in google drive**
 
   Uploaded all the reports in google drive 
   link: https://drive.google.com/drive/u/1/folders/1HtwQfRqK3TmDR7VA2Sahg34OIZBKbiDT



