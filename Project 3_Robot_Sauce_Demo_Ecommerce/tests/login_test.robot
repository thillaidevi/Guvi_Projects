*** Settings ***
Library      SeleniumLibrary
Library      ../libraries/LoginLibrary.py      # Handles login-related keywords

Suite Setup      Open Browser To Login Page      # Launches browser and navigates to login
Suite Teardown   Close Browser                   # Ensures browser is closed after tests


*** Variables ***
${URL}      https://www.saucedemo.com
${PASSWORD}      secret_sauce
${BROWSER}    Chrome


*** Test Cases ***
Login – standard_user should succeed
    [Documentation]      Validate login for standard_user with expected success
    [Tags]      login      standard_user      smoke


    Comment      Validate login for standard_user (expected to succeed)
    ${username}=      Set Variable      standard_user
    ${expectation}=      Set Variable      EXPECT_SUCCESS
    Login And Validate      ${username}      ${expectation}

    Comment      Dismiss any unexpected alert that may appear post-login
    Run Keyword And Ignore Error      Handle Alert      action=DISMISS

    Comment      Confirm dashboard visibility based on expected login outcome and take screenshot
    Validate Dashboard If Expected Success      ${username}      ${expectation}

    Capture Page Screenshot      ${TEST NAME}_${username}_${expectation}_screenshot.png

    Log      ${username} login validated with ${expectation}

Login – performance_glitch_user should succeed
    [Documentation]      Validate login for performance_glitch_user with expected success and slow load
    [Tags]      login      performance_glitch_user      regression


    Comment      Reset to login page before testing next user
    Reset To Login Page

    Comment      Validate login for performance_glitch_user (expected to succeed but may load slowly)
    ${username}=      Set Variable      performance_glitch_user
    ${expectation}=      Set Variable      EXPECT_SUCCESS

    Login And Validate      ${username}      ${expectation}

    Comment      Dismiss any unexpected alert that may appear post-login
    Run Keyword And Ignore Error      Handle Alert      action=DISMISS

    Comment      Wait for inventory page to load due to potential performance delays
    Wait Until Page Contains Element      class=inventory_list      timeout=10s

    Comment      Confirm dashboard visibility based on expected login outcome and take screenshot
    Validate Dashboard If Expected Success      ${username}      ${expectation}

    Capture Page Screenshot      ${TEST NAME}_${username}_${expectation}_screenshot.png
    Log      ${username} login validated with ${expectation}

Login – locked_out_user should fail
    [Documentation]      Validate login for locked_out_user with expected failure
    [Tags]      login      locked_out_user      negative


    Comment      Reset to login page before testing next user
    Reset To Login Page

    Comment       Validate login for locked_out_user (expected to fail)
    ${username}=      Set Variable      locked_out_user
    ${expectation}=      Set Variable      EXPECT_ERROR

    Login And Validate      ${username}      ${expectation}

    Comment      Dismiss any unexpected alert that may appear post-login
    Run Keyword And Ignore Error      Handle Alert      action=DISMISS

    Comment      Confirm dashboard is not accessible due to login restriction
    Validate Dashboard If Expected Success      ${username}      ${expectation}

    Capture Page Screenshot      ${TEST NAME}_${username}_${expectation}_screenshot.png
    Log      ${username} login validated with ${expectation}