*** Settings ***
Library      SeleniumLibrary
Library      ../libraries/LoginLibrary.py      # Handles login-related keywords
Library      ../libraries/InventoryLibrary.py      # Handles login-related keywords

# Setup and teardown for each test suite
Suite Setup      Open Browser To Login Page      # Launches browser and navigates to login
Suite Teardown      Close Browser       # Ensures browser is closed after tests


*** Test Cases ***
Random Product Selection And Cart Validation
    [Documentation]      Randomly select 4 out of the 6 listed products and fetch their names and prices.
    ...                  Add the selected products to the cart and verify the cart item count matches.
    ...                  Then navigate to the cart page and validate product details.

    [Tags]      Smoke      Cart      Validation

    Comment      Log in as a standard user and verify successful authentication
    Login And Validate      standard_user      EXPECT_SUCCESS

    Comment      Wait until the inventory page is fully loaded and ready for interaction
    Wait Until Inventory Page Is Loaded

    Comment      Randomly select 4 products from the available catalog
    Select Random Products      4

    Comment      Log the names and prices of the selected products for validation
    Log Selected Product Details

    Comment      Capture screenshot of selected products for reporting/debugging
    Capture Page Screenshot      ${TEST NAME}_stage1.png

    Comment      Add selected products to cart and validate that cart count matches selection
    Add Selected Products To Cart And Validate
    Capture Page Screenshot      ${TEST NAME}_stage2.png

    Comment      Navigate to cart and verify that product details match the selected items
    Validate Cart Contents Against Selected Products
    Capture Page Screenshot      ${TEST NAME}_stage3.png