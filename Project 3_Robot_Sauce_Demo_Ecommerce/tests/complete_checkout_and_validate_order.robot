*** Settings ***
Library      SeleniumLibrary
Library      ../libraries/LoginLibrary.py      # Handles login-related keywords
Library      ../libraries/InventoryLibrary.py      # Handles login-related keywords

# Setup and teardown for each test suite
Suite Setup      Open Browser To Login Page      # Launches browser and navigates to login
Suite Teardown      Close Browser      # Ensures browser is closed after tests


*** Test Cases ***
Complete Checkout And Validate Order
    [Documentation]      Randomly select 4 products, add them to cart, validate cart contents,
    ...                  proceed to checkout, and confirm order completion.
    [Tags]    Smoke      Checkout      Order

    Comment      Log in as a standard user and verify successful authentication
    Login And Validate      standard_user      EXPECT_SUCCESS

    Comment      Wait until the inventory page is fully loaded and ready for interaction
    Wait Until Inventory Page Is Loaded

    Comment      Randomly select 4 products from the catalog to simulate varied user behavior
    Select Random Products      4

    Comment      Log the names and prices of the selected products for validation and reporting
    Log Selected Product Details

    Comment      Capture a screenshot of selected products for visual confirmation and debugging
    Capture Page Screenshot      ${TEST NAME}_screenshot1.png

    Comment      Add selected products to the cart and validate that the cart count matches the selection
    Add Selected Products To Cart And Validate

    Comment      Navigate to the cart and verify that product details match the selected items
    Validate Cart Contents Against Selected Products
    Capture Page Screenshot      ${TEST NAME}_screenshot2.png

    Comment      Proceed through the checkout flow and confirm that the order is successfully placed
    Complete Checkout And Validate Order
    Capture Page Screenshot      ${TEST NAME}_screenshot3.png