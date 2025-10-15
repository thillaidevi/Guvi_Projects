#  Automated Testing of the Web Application – [saucedemo.com](https://www.saucedemo.com)

##  Project Objective

This project automates the testing of the demo e-commerce web application [SauceDemo](https://www.saucedemo.com), validating core functionalities such as login, product selection, cart operations, and checkout flow. The framework simulates real-world user interactions and ensures system behavior aligns with expected outcomes.

---

##  Scope

The automation suite is designed to:

- Simulate real-time user behavior across multiple user roles
- Validate functional flows: login, cart management, checkout
- Randomly interact with product listings to mimic diverse purchase paths
- Ensure correctness of UI content, product data, and order summary
- Generate readable execution reports for analysis

---

##  Tech Stack

- **Framework**: Robot Framework  
- **Browser Automation**: SeleniumLibrary  
- **Language**: Python  
- **Execution**: CLI / IDE / CI pipelines  
- **Reporting**: Robot Framework logs and HTML reports

---

##  Preconditions

- Positive and negative test data included
- Data-driven and keyword-driven strategies for flexibility
- Dynamic waits implemented for UI stability
- Object-oriented principles applied where applicable
- Exception handling for test resilience
- Browser teardown after test execution

---

##  Test Suite Overview

| Test Case | Scenario | Description | Expected Result |
|----------|----------|-------------|-----------------|
| TC-01 | Login with predefined users | Login with users like `standard_user`, `locked_out_user`, etc. | System responds per user role |
| TC-02 | Invalid login | Attempt login with incorrect credentials | Access denied |
| TC-03 | Logout functionality | Validate logout button and redirection | User returns to login screen |
| TC-04 | Cart icon visibility | Check cart icon post-login | Icon remains visible |
| TC-05 | Random product selection | Select 4 of 6 products and extract data | Names and prices logged |
| TC-06 | Add to cart validation | Add selected products and verify cart count | Cart shows 4 items |
| TC-07 | Cart detail accuracy | Validate cart contents match selection | Product details consistent |
| TC-08 | Checkout and order confirmation | Complete checkout and capture summary | Confirmation message shown |
| TC-09 | Sorting functionality | Change sort order and verify product list | Products sorted correctly |
| TC-10 | Reset App State | Trigger reset and validate UI state | Cart cleared, buttons reset |

---

##  Best Practices Followed

- Modular keyword design for reusability
- Inline comments for clarity
- Structured folder hierarchy for scalability
- Readable logs and screenshots for debugging
- Clean teardown and browser closure
- GitHub-ready documentation and code formatting

---

##  Repository Structure


 Robot_Sauce_Demo_Ecommerce               
    |__pages                            # Contains Login_page 
    |    |_  login_page.py
    
    |__libraries                        # Libraries contains loginLibrary and InventoryLibrary              
    |    |_  InventoryLibrary.py
    |    |_  LoginLibrary.py
    |   
    |__tests                            # Test suites contains positive and negative test case
    |    |_  cart_icon_visibility.robot
    |    |_  complete_checkout_and_validate_order.robot
    |    |_  login_invalid_credential.robot
    |    |_  login_test.robot
    |    |_  logout_functionality.robot
    |    |_  random_product_selection.robot
    |    |_  random_product_selection_and_validate.robot
    |    |_  validate_cart.robot
    |    |_  validate_product_sorting.robot
    |    |_  validate_reset_app_state.robot
    |
    |
    |_ Readme.md
    |_ requirements.txt 
    |__reports                         # Contains reports based on the browser  
    |__screenshots                     # Contains screenshots based on the browser
   

---
##  How to Run

1. **Install dependencies**  
   ```bash
   pip install -r requirements.txt

2. **Execute test suite**
   ```bash
   robot tests/

