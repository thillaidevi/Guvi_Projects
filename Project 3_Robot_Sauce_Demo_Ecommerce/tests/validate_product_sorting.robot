*** Settings ***
Library      SeleniumLibrary
Library      ../libraries/LoginLibrary.py      # Handles login-related keywords
Library      ../libraries/InventoryLibrary.py      # Handles login-related keywords

# Setup and teardown for each test suite
Suite Setup      Open Browser To Login Page      # Launches browser and navigates to login
Suite Teardown      Close Browser       # Ensures browser is closed after tests


*** Test Cases ***
Validate Product Sorting Functionality
    [Documentation]      Change the sorting option on the products page and verify that the product list updates accordingly.
    [Tags]      Sorting      UI      Smoke

    Comment      Log in as a standard user and verify successful authentication
    Login And Validate      standard_user      EXPECT_SUCCESS

    Comment      Wait until the inventory page is fully loaded and ready for interaction
    Wait Until Inventory Page Is Loaded

    Comment      Apply sorting by "Price (low to high)" and validate product order
    Validate Product Sorting      Price (low to high)
    Capture Page Screenshot      ${TEST NAME}_Price (low to high)_screenshot.png

    Comment      Apply sorting by "Name (Z to A)" and validate alphabetical order
    Validate Product Sorting      Name (Z to A)
    Capture Page Screenshot      ${TEST NAME}_Name (Z to A)_screenshot.png