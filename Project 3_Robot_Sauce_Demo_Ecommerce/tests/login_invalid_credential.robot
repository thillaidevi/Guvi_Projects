*** Settings ***
Library      SeleniumLibrary
Library      ../libraries/LoginLibrary.py      # Handles login-related keywords

# Setup and teardown for each test suite
Suite Setup      Open Browser To Login Page      # Launches browser and navigates to login
Suite Teardown      Close Browser       # Ensures browser is closed after tests


*** Variables ***
${INVALID_USERNAME}      invalid_user
${INVALID_PASSWORD}      wrong_password
${EXPECTATION}      EXPECT_ERROR

*** Test Cases ***
Login With Invalid Credentials
    [Documentation]      Attempt to log in using non-standard credentials and validate the response.
    [Tags]    negative    login

    Comment       Enter an invalid username to simulate unauthorized access
    Input Text    id=user-name      ${INVALID_USERNAME}

    Comment      Enter an invalid password to complete the invalid credential pair
    Input Text    id=password      ${INVALID_PASSWORD}

    Comment      Click the login button to submit the credentials
    Click Button    id=login-button

    Comment      Dismiss any alert that may appear due to failed login attempt
    Run Keyword And Ignore Error      Handle Alert      action=DISMISS

    Comment      Validate that dashboard access is denied and login fails as expected
    Validate Dashboard If Expected Success      ${INVALID_USERNAME}      ${EXPECTATION}
    Capture Page Screenshot    ${TEST NAME}_${INVALID_USERNAME}_${expectation}_screenshot.png


