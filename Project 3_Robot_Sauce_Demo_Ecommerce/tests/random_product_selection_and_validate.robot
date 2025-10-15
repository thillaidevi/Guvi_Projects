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
    ...                Add the selected products to the cart and verify the cart item count matches.
    [Tags]      Smoke      Cart

    Comment      Log in using a valid standard user and confirm successful login
    Login And Validate      standard_user      EXPECT_SUCCESS

    Comment      Wait until the inventory/product listing page is fully loaded
    Wait Until Inventory Page Is Loaded

    Comment      Randomly select 4 products from the available 6 to simulate varied user behavior
    Select Random Products      4

    Comment      Log the names and prices of the selected products for validation and reporting
    Log Selected Product Details

    Comment      Capture a screenshot of selected products for visual confirmation and debugging
    Capture page screenshot      ${TEST NAME}.png

    Comment      Add the selected products to the cart and verify that the cart count matches the selection
    Add Selected Products To Cart And Validate
    Capture page screenshot      ${TEST NAME}_with_added_products.png