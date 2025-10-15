LOGIN_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

# External locators for Login page
LOGIN_PAGE_LOCATORS = {
    "username_input": {"type": "placeholder", "value": "Username"},
    "password_input": {"type": "placeholder", "value": "Password"},
    "login_button": {"type": "role", "name": "Login"},
    "error_message": ".oxd-alert-content-text",
    "user_dropdown": ".oxd-userdropdown-name",
    "logout_option": {"type": "role", "name": "Logout"},
    "dashboard_header": "h6:has-text('Dashboard')",
    "forgot_password_link": "p.orangehrm-login-forgot-header",
    "reset_password_header": "h6.orangehrm-forgot-password-title",
    "success_message": "h6.orangehrm-forgot-password-title"

}

# External locators for Dashboard page
DASHBOARD_PAGE_LOCATORS = {
    "dashboard_header": "h6:has-text('Dashboard')",
    "menu_wrapper_class": ".oxd-main-menu-item-wrapper",
    "admin_tab": "a.oxd-main-menu-item:has-text('Admin')",
    "user_dropdown": "p.oxd-userdropdown-name"
}

# External locators for Forgot password page
FORGOT_PASSWORD_LOCATORS = {
    "username_input": "input[placeholder='Username']",
    "reset_button": "button:has-text('Reset Password')",
    "confirmation_message": "h6.orangehrm-forgot-password-title",
    "cancel_button": "button:has-text('Cancel')",
    "forgot_password_header": "text='Forgot Your Password?'",
    "success_message": "h6.orangehrm-forgot-password-title"

}

# External locators for Admin page
ADMIN_LOCATORS = {
    "username_input": "input[name='username']",
    "password_input": "input[name='password']",
    "login_button": "button[type='submit']",
    "dashboard_marker": "h6:has-text('Dashboard')",

    "admin_menu": "a:has-text('Admin')",
    "add_user": "button:has-text('Add')",

    "user_role_dropdown": "div.oxd-select-text-input >> nth=0",
    "user_role_option": "div[role='option']:has-text('Admin')",

    "status_dropdown": "div.oxd-select-text-input >> nth=1",
    "status_option": "div[role='option']:has-text('Enabled')",

    "employee_name": "input[placeholder='Type for hints...']",
    "employee_autocomplete": "div[role='option']",

    "username": "input.oxd-input >> nth=1",
    "password": "input[type='password'] >> nth=0",
    "confirm_password": "input[type='password'] >> nth=1",

    "save_button": "button:has-text('Save')"
}

# External locators for Pim page
PIM_LOCATORS = {
    "pim_tab": "a.oxd-main-menu-item:has-text('PIM')",
    "pim_header": "h6.oxd-topbar-header-breadcrumb-module",
    "add_btn": "button:has-text('Add')",
    "first_name": "input[name='firstName']",
    "last_name": "input[name='lastName']",
    "emp_id": "input.oxd-input.oxd-input--active >> nth=1",
    "save_btn": "button:has-text('Save')"
}

# External locators for AdminUserManagementPage
ADMIN_USER_LOCATORS = {
    "username_input": "input[name='username']",
    "user_role_dropdown": "label:has-text('User Role') + div",
    "user_role_option": lambda role: f"div[role='option']:has-text('{role}')",
    "employee_name_input": "input[placeholder='Type for hints...']",
    "employee_name_option": lambda name: f"div[role='option']:has-text('{name}')",
    "status_dropdown": "label:has-text('Status') + div",
    "status_option": lambda status: f"div[role='option']:has-text('{status}')",
    "search_button": "button:has-text('Search')",
    "user_table_row": "div.oxd-table-row",
    "error_message": "span.oxd-input-field-error-message"
}

# Navigation locator for My_info page
MY_INFO_NAV = {
   # "my_info_tab": "nav.oxd-sidepanel span.oxd-main-menu-item--name:has-text('My Info')"
       "my_info_tab": "text=My Info"
}

#  # External locators and tab locators inside My Info page
MY_INFO_LOCATORS = {
     "personal_details": {
        "menu": "a.orangehrm-tabs-item[href*='viewPersonalDetails']",
        "header": "h6.orangehrm-main-title:has-text('Personal Details')"
    },
    "contact_details": {
        "menu": "a.orangehrm-tabs-item[href*='contactDetails']",
        "header": "h6.orangehrm-main-title:has-text('Contact Details')"
    },
    "emergency_contacts": {
        "menu": "a.orangehrm-tabs-item:has-text('Emergency Contacts')",
        "header": "h6.orangehrm-main-title:has-text('Emergency Contacts')"
    },
    "dependents": {
        "menu": "a.orangehrm-tabs-item:has-text('Dependents')",
        "header": "h6.orangehrm-main-title:has-text('Assigned Dependents')"
    },
    "immigration": {
        "menu": "a.orangehrm-tabs-item:has-text('Immigration')",
        "header": "h6.orangehrm-main-title:has-text('Immigration Records')"
    },
    "job": {
        "menu": "a.orangehrm-tabs-item:has-text('Job')",
        "header": "h6.orangehrm-main-title:has-text('Job Details')"
    },
   "salary": {
        "menu": "a.orangehrm-tabs-item[href*='viewSalaryList']",
        "header": "h6.orangehrm-main-title:has-text('Assigned Salary Components')"
    },
    "report_to": {
        "menu": "a.orangehrm-tabs-item[href*='viewReportToDetails']",
        "header": "h6.orangehrm-main-title:has-text('Report to')"
    },
    "qualifications": {
        "menu": "a.orangehrm-tabs-item[href*='viewQualifications']",
        "header": "h6.orangehrm-main-title:has-text('Qualifications')"
    },

    "memberships": {
        "menu": "a.orangehrm-tabs-item:has-text('Memberships')",
        "header": "h6.orangehrm-main-title:has-text('Memberships')"
    }
}

# External locators for main menu
MENU_LOCATORS = {
    "Admin": {
        "role": "menuitem",
        "name": "Admin"
    },
    "PIM": {
        "role": "menuitem",
        "name": "PIM"
    },
    "Leave": {
        "role": "menuitem",
        "name": "Leave"
    },
    "Time": {
        "role": "menuitem",
        "name": "Time"
    },
    "Recruitment": {
        "role": "menuitem",
        "name": "Recruitment"
    },
    "My Info": {
        "role": "menuitem",
        "name": "My Info"
    },
    "Performance": {
        "role": "menuitem",
        "name": "Performance"
    },
    "Dashboard": "h6:has-text('Dashboard')"  # fallback string selector
}

# # External shared locators for leave page
shared_locators = {
    "employee_input": "input[placeholder='Type for hints...']",
    "toast_message": "div.oxd-toast-content",
    "error_alert": "div.oxd-alert-content"
}

# External locators for Leave page
LeavePageLocators = {
    **shared_locators,
    "leave_type_dropdown": "div.oxd-select-wrapper:has(label:has-text('Leave Type'))",
    "leave_type_option": lambda text: f"div[role='option']:has-text('{text}')",
    "from_date_input": "input[name='fromDate']",
    "to_date_input": "input[name='toDate']",
    "comment_textarea": "textarea.oxd-textarea",
    "assign_button": "button:has-text('Assign')",
    "leave_balance_text": "p.orangehrm-leave-balance-text"
}

# External locators for success message selectors in leave page
success_message_selectors = {
    **shared_locators,
    "entitlement_leave_type_dropdown": "div.oxd-select-text:has-text('Select')",
    "entitlement_leave_type_option": lambda text: f"div.oxd-select-option:has-text('{text}')",
    "entitlement_input": "input.oxd-input--active",
    "save_button": "button:has-text('Save')",
    "success_message": "div.oxd-toast-content:has-text('Entitlement updated successfully')"
}

# External locators for Leave Entitlement
LeaveEntitlementLocators = {
    "page_title": "p.orangehrm-main-title:has-text('Add Leave Entitlement')",
    "leave_tab": "text='Leave'",
    "entitlements_tab": "span.oxd-topbar-body-nav-tab-item:has-text('Entitlements')",
    "add_entitlements_link": "a.oxd-topbar-body-nav-tab-link:has-text('Add Entitlements')",
    "employee_suggestion": lambda name: f"div[role='listbox'] div:has-text('{name}')",
    "leave_type_dropdown": "div.oxd-select-text-input",
    "leave_type_option": "div[role='option']",
    "entitlement_input": "label:has-text('Entitlement') >> xpath=../..//input",
    "save_button": "button:has-text('Save')",
    "invalid_error": "span.oxd-input-field-error-message:has-text('Invalid')",
    "modal_title": "p:has-text('Updating Entitlement')",
    "modal_button": lambda text: f"button:has-text('{text}')",
    "entitlement_page_header": "h5.oxd-table-filter-title:has-text('Leave Entitlements')",
    "record_found_text": "span.oxd-text--span:has-text('(1) Record Found')",
    "summary_total_text": "span.oxd-text--span",
    "assign_leave_button": "a.oxd-topbar-body-nav-tab-item:has-text('Assign Leave')"
}

# External locators for Assign Leave Page
AssignLeaveLocators = {
    "employee_input": "input[placeholder='Type for hints...']",
    "employee_dropdown": lambda name: f".ac_results >> text={name}",
    "assign_leave_tab": "a.oxd-topbar-body-nav-tab-item",
    "assign_leave_input": "input[placeholder='Type for hints...']",
    "leave_type_dropdown": "div.oxd-select-text:has-text('Leave Type')",
    "leave_period_dropdown": "div.oxd-select-text:has-text('Leave Period')",
    "dropdown_options": "div[role='listbox'] > div",
    "comment_textarea": "textarea.oxd-textarea",
    "assign_button": "button:has-text('Assign')",
    "date_input": lambda field: f"input[name='{field}']",
    "toast_container": "div.oxd-toast",
    "toast_message": "div.oxd-toast-content",
    "selected_employee": "div.selected-employee-name"
}
# External locators for Leave Report Page
LeaveReportLocators= {
    "REPORTS_TAB" : "span.oxd-topbar-body-nav-tab-item",
    "REPORT_LINK" : "a.oxd-topbar-body-nav-tab-link[role='menuitem']",
    "REPORT_HEADER" :"h5.oxd-table-filter-title",

    "RADIO_LEAVE_TYPE" : "input[type='radio'][value='leave_type_leave_entitlements_and_usage']",
    "RADIO_EMPLOYEE" : "input[type='radio'][value='employee_leave_entitlements_and_usage']",

    "LEAVE_TYPE_DROPDOWN" : "div.oxd-select-text-input",
    "LEAVE_TYPE_OPTION" : "div[role='option']",

    "EMPLOYEE_INPUT" : "input[placeholder='Type for hints...']",
    "EMPLOYEE_SUGGESTION" : ".oxd-autocomplete-option",

    "GENERATE_BUTTON" : "button[type='submit']",
    "REPORT_TABLE" : "table"
}
# External locators for Claim Page
ClaimPageLocators = {
    "claim_section_url": "https://opensource-demo.orangehrmlive.com/web/index.php/claim/viewClaim",
    "claim_history_url": "https://opensource-demo.orangehrmlive.com/web/index.php/claim/viewMyClaims",
    "claim_type_dropdown": "select[name='claimType']",
    "claim_amount_input": "input[name='amount']",
    "claim_reason_textarea": "textarea[name='reason']",
    "submit_button": "button:has-text('Submit')",
    "toast_message": ".oxd-toast-content",
    "claim_row": lambda claim_type, amount: f"text={claim_type} >> text=₹{amount}"
}

# External locators for Add expense popup window
AddExpensePopupLocators = {
    "EXPENSE_TYPE_DROPDOWN" : "div.oxd-select-text-input",
    "EXPENSE_TYPE_OPTION" : lambda expense_type: f"div[role='option']:has-text('{expense_type}')",
    "DATE_INPUT" : "input[placeholder='yyyy-dd-mm']",
    "AMOUNT_INPUT" : "input.oxd-input--active",
    "NOTE_TEXTAREA" : "textarea.oxd-textarea--active",
    "SAVE_BUTTON" : "button[type='submit']",
    "CLAIM_SUMMARY_BLOCK" : "div.claim-summary",
    "RECORD_FOUND_TEXT" : "div:has-text('Record Found')",
    "TOTAL_AMOUNT_TEXT" : "div:has-text('Total Amount')",
    "EXPENSE_TABLE" : "table",
    "SUMMARY_DIV" : "div.claim-summary div"
}