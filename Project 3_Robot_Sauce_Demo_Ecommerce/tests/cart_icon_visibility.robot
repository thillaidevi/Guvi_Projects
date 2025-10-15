*** Settings ***
Library      SeleniumLibrary
Library      ../libraries/LoginLibrary.py      # Handles login-related keywords

# Setup and teardown for each test suite
Suite Setup      Open Browser To Login Page      # Launches browser and navigates to login
Suite Teardown      Close Browser       # Ensures browser is closed after tests


*** Variables ***
${VALID_USERNAME}      standard_user
${EXPECTATION}      EXPECT_SUCCESS


*** Test Cases ***
Check Cart Icon Visibility
    [Documentation]      Verify if the cart icon is visible on the product listing page post login.
    [Tags]      smoke      cart

    Comment      Log in using a valid user and confirm expected login outcome
    Login And Validate      ${VALID_USERNAME}      ${EXPECTATION}

    Comment      Validate that the dashboard is displayed if login was successful
    Validate Dashboard If Expected Success      ${VALID_USERNAME}      ${EXPECTATION}

    Comment      Check that the cart icon is present on the product listing page
    Page Should Contain Element      id=shopping_cart_container

    Capture Page Screenshot      ${TEST NAME}_${VALID_USERNAME}_${EXPECTATION}_screenshot.png

    Comment      Log confirmation that the cart icon is visible after login
    Log      Cart icon is visible after login
