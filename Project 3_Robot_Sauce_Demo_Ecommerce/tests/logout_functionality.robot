*** Settings ***
Library      SeleniumLibrary
Library      ../libraries/LoginLibrary.py      # Handles login-related keywords

# Setup and teardown for each test suite
Suite Setup      Open Browser To Login Page      # Launches browser and navigates to login
Suite Teardown      Close Browser       # Ensures browser is closed after tests


*** Variables ***
${VALID_USERNAME}     standard_user
${EXPECTATION}        EXPECT_SUCCESS


*** Test Cases ***
Validate Logout Functionality
    [Documentation]     Check whether the logout button is visible after login and whether clicking it properly logs the user out.
    [Tags]     smoke     logout

    Comment      Log in using a valid standard user and confirm successful login
    Login And Validate      standard_user      EXPECT_SUCCESS

    Comment      Confirm that the dashboard is displayed if login was successful
    Validate Dashboard If Expected Success      ${VALID_USERNAME}      ${EXPECTATION}
    Capture Page Screenshot      ${TEST NAME}_${VALID_USERNAME}_${expectation}_screenshot.png

    Comment      Click the logout button to initiate user sign-out
    Click Logout Button

    Comment      Verify that the login page is displayed after logout
    Page Should Contain Element      id=login-button
    Capture Page Screenshot      ${TEST NAME}_screenshot.png

    Comment      Log confirmation that logout was successful and user is redirected
    Log      Logout successful, user returned to login screen
