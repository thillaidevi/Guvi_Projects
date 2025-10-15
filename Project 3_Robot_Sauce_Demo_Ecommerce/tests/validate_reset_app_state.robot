*** Settings ***
Library      SeleniumLibrary
Library      ../libraries/LoginLibrary.py      # Handles login-related keywords
Library      ../libraries/InventoryLibrary.py      # Handles login-related keywords

# Setup and teardown for each test suite
Suite Setup      Open Browser To Login Page      # Launches browser and navigates to login
Suite Teardown      Close Browser       # Ensures browser is closed after tests


*** Test Cases ***
Validate Reset App State Functionality
    [Documentation]      Add products to cart, navigate the site, trigger "Reset App State" from the menu,
    ...                   and confirm that cart and selections are cleared.

    [Tags]      Reset      State      Smoke

    Comment      Log in as a standard user and verify successful login
    Login And Validate      standard_user      EXPECT_SUCCESS

    Comment     Wait until product listing page is fully loaded
    Wait Until Inventory Page Is Loaded

    Comment     Randomly select 4 products from the catalog
    Select Random Products      4

    Comment    Add selected products to cart and validate cart count
    Add Selected Products To Cart And Validate
    Capture Page Screenshot      ${TEST NAME}_before_reset_with_products_screenshot.png

    Comment     Trigger reset and validate cart and product button states
    Reset App State And Validate
    Capture Page Screenshot      ${TEST NAME}_after_reset_screenshot.png