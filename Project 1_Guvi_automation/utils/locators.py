from selenium.webdriver.common.by import By

"""Centralized locator repository for all pages like Basepage, LoginPage and DashboardPage
 and added nested dictionary for menu items """

LOCATORS = {
    "BasePage": {
        "signup_button": (By.XPATH, "//a[text()='Sign up']"),
        "base_login_button": (By.XPATH, "//a[@id='login-btn']"),
        "dobby_welcome": (By.ID, "ym-auto-pop-up-description"),
        "menu_items": {
            "Courses": (By.XPATH, "//a[@href='/courses/' and text()='Courses']"),
            "LIVE Classes": (By.XPATH, "//p[@id='liveclasseslink']"),
            "Practice": (By.XPATH, "//p[@id='practiceslink']"),
            "Resources": (By.XPATH, "//p[@id='resourceslink']"),
            "Products": (By.XPATH, "//p[@id='solutionslink']")
        }
    },

    "LoginPage": {
        "email_textbox": (By.XPATH, "//input[@id='email']"),
        "password_textbox": (By.XPATH, "//input[@id='password']"),
        "login_submit_button": (By.XPATH, "//a[@id='login-btn']"),
        "my_courses_element": (By.XPATH, "//div[text()='My Courses']"),
        "invalid_feedback": (By.XPATH, "//div[@class='invalid-feedback']")
    },

    "DashboardPage": {
        "profile_menu": (By.ID, "dropdown_title"),
        "logout_button": (By.XPATH, "//div[text()='Sign Out']")
    }
}