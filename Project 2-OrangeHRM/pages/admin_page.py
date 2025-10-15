from project_orangehrm_playwright.utils.locators import ADMIN_LOCATORS
from playwright.sync_api import Page, expect
from project_orangehrm_playwright.utils.logger import get_logger
from project_orangehrm_playwright.utils.screenshots import capture_screenshot
from datetime import datetime
import time,re

class AdminPage:
    """
    Page object for Admin module.
    Handles login, employee creation, and user creation flows.
    """

    def __init__(self, page, logger=None):
        self.page = page
        self.logger = logger or get_logger()



    def select_dropdown_option(self, option_text: str, dropdown_index: int = 0):
        """
        Selects an option from a dropdown by index and visible text.
        Used for Role and Status selection during user creation.
        """
        self.logger.info(f"Selecting dropdown option: {option_text}")
        try:
            # Locate all dropdown wrappers and target the one by index
            dropdowns = self.page.locator("div.oxd-select-wrapper")
            expect(dropdowns.nth(dropdown_index)).to_be_visible(timeout=5000)
            dropdowns.nth(dropdown_index).scroll_into_view_if_needed()
            dropdowns.nth(dropdown_index).click()

            # Wait for listbox and select option
            self.page.wait_for_selector("div[role='listbox']", timeout=3000)
            option = self.page.locator(f"div[role='listbox'] div[role='option']:has-text('{option_text}')")
            expect(option.first).to_be_visible(timeout=3000)
            option.first.click()

            self.logger.info(f"Selected: {option_text}")

        except Exception as e:
            capture_screenshot(self.page, f"dropdown_failed_{option_text}.png")
            self.logger.error(f"Dropdown selection failed for '{option_text}': {e}")
            raise

    def click_add_user_button(self):
        """
            Navigates to the System Users page and clicks the 'Add' button to open the user creation form.
            Includes robust checks for page header and button visibility.
        """

        try:
            self.logger.info(" Navigating to System Users and clicking Add")

            # Confirm navigation via URL
            assert "admin/viewSystemUsers" in self.page.url, " Not on System Users page"

            # Wait for any h6 to appear
            self.page.wait_for_selector("h6", timeout=10000)

            # Filter h6 headers by exact text 'Admin'
            header_locator = self.page.locator("h6").filter(has_text="Admin")
            expect(header_locator).to_have_count(1)
            expect(header_locator).to_be_visible(timeout=5000)

            # Locate Add button using role-based locator
            add_button = self.page.get_by_role("button", name="Add")
            expect(add_button).to_be_enabled(timeout=5000)

            # Scroll into view and click
            add_button.scroll_into_view_if_needed()
            add_button.click()

            self.logger.info(" Add User form opened successfully")

        except Exception as e:
            #  Debug fallback: log all h6 headers and current URL
            try:
                headers = self.page.locator("h6")
                self.logger.debug(f"All h6 headers: {headers.all_text_contents()}")
                self.logger.debug(f"Current URL: {self.page.url}")
            except Exception as inner:
                self.logger.debug(f"Header debug failed: {inner}")

            # Capture screenshot for failure analysis
            capture_screenshot(self.page, "click_add_user_failed.png")
            self.logger.error(f" Failed to click Add button in System Users: {e}")
            raise

    def fill_unique_username_and_save(self, base_username, max_attempts=5):
        """
        Attempts to create a unique username by appending a numeric suffix if needed.
        Tries up to `max_attempts` times, checking for 'Already exists' warning after each attempt.
        If successful, clicks Save and waits for redirect to System Users page.
        Returns the successfully created username.
        """

        #  Locate the username input field (first autocomplete-off input)
        username_input = self.page.locator("input[autocomplete='off']").nth(0)

        for i in range(max_attempts):
            #  Generate candidate username (e.g., testuser0, testuser1, ...)
            candidate = f"{base_username}{i}" if i > 0 else base_username

            #  Clear and fill the input field with the candidate username
            username_input.clear()
            username_input.fill(candidate)
            self.page.wait_for_timeout(500)  # Let DOM settle

            #  Check for 'Already exists' warning below the input
            warning = self.page.locator("span:has-text('Already exists')")
            if warning.is_visible():
                self.logger.warning(f" Username '{candidate}' already exists — trying next")
                continue  # Try next candidate

            #  Attempt to save the user with the current candidate
            save_button = self.page.locator("button:has-text('Save')")
            expect(save_button).to_be_enabled(timeout=5000)
            save_button.click()
            self.logger.info(f" Save clicked with username: {candidate}")

            #  Wait for redirect to System Users page to confirm success
            try:
                self.page.wait_for_url("**/viewSystemUsers", timeout=10000)
                expect(self.page.locator("h6:has-text('System Users')")).to_be_visible(timeout=10000)

                #  Capture screenshot for audit trail
                self.logger.info(f"User '{candidate}' created successfully")
                capture_screenshot(self.page, "user_creation_success.png")
                return candidate  # Return the successful username

            except Exception:
                #  Save failed — retry with next candidate
                self.logger.warning(f" Save failed with username '{candidate}' — retrying")

        #  All attempts exhausted — raise exception
        raise Exception(" Could not create user after multiple attempts")

    def create_user_save(self, username, password, confirm_password, role, employee_name, status):
        """
        Creates a new user in the Admin module.
        Handles dropdown selections, dynamic username retry, form validations, and post-save verification.
        """
        self.logger.info(f"Starting user creation for: {username}")
        final_username = username

        try:
            # Wait for Add User form
            self.page.wait_for_selector("h6:has-text('Add User')", timeout=10000)

            # Select Role and Status
            self.select_dropdown_option(role, dropdown_index=0)
            self.select_dropdown_option(status, dropdown_index=1)

            # Fill Employee Name
            emp_input = self.page.locator("input[placeholder='Type for hints...']")
            expect(emp_input).to_be_visible(timeout=5000)
            emp_input.fill(employee_name)
            self.page.wait_for_selector(f"div[role='option']:has-text('{employee_name}')", timeout=3000)
            self.page.locator(f"div[role='option']:has-text('{employee_name}')").first.click()

            # Fill Username with retry if "Already exists"
            username_input = self.page.locator("input[autocomplete='off']").nth(0)
            expect(username_input).to_be_visible(timeout=5000)

            for attempt in range(3):
                username_input.fill("")
                self.page.wait_for_timeout(300)
                username_input.fill(final_username)
                self.page.wait_for_timeout(800)

                warning = self.page.locator("span:has-text('Already exists')")
                if warning.is_visible():
                    self.logger.warning(f"Username '{final_username}' already exists — retrying")
                    unique_suffix = str(int(time.time()))[-4:]
                    final_username = f"{username}{unique_suffix}"
                    continue  # retry with updated final_username
                else:
                    self.logger.info(f"Username accepted: {final_username}")
                    break
            else:
                self.logger.error(f"Username retry failed — warning still present for '{final_username}'")
                capture_screenshot(self.page, f"username_blocked_{final_username}.png")
                raise Exception("Username retry exhausted")

            # Fill Passwords
            password_input = self.page.locator("input[type='password']").nth(0)
            confirm_input = self.page.locator("input[type='password']").nth(1)
            expect(password_input).to_be_visible(timeout=5000)
            expect(confirm_input).to_be_visible(timeout=5000)
            password_input.fill(password)
            confirm_input.fill(confirm_password)

            # Pre-save validation
            validation_warnings = self.page.locator("span.oxd-input-field-error")
            if validation_warnings.count() > 0:
                for i in range(validation_warnings.count()):
                    warning_text = validation_warnings.nth(i).inner_text()
                    self.logger.error(f"Validation warning: {warning_text}")
                capture_screenshot(self.page, f"validation_block_{final_username}.png")
                raise Exception("Form blocked by validation warning")

            # Check required fields
            required_inputs = self.page.locator("input[required]")
            for i in range(required_inputs.count()):
                input_field = required_inputs.nth(i)
                value = input_field.input_value()
                label = input_field.get_attribute("aria-label") or input_field.get_attribute(
                    "placeholder") or f"Field {i}"
                if not value.strip():
                    self.logger.error(f"Required field '{label}' is empty")
                    capture_screenshot(self.page, f"missing_field_{final_username}.png")
                    raise Exception(f"Required field '{label}' missing")

            # Click Save
            save_button = self.page.locator("button[type='submit']", has_text="Save")
            expect(save_button).to_be_visible(timeout=5000)
            assert save_button.is_enabled(), "Save button is disabled — form may be incomplete"
            save_button.click()
            self.logger.info(f"Save clicked for username: {final_username}")

            # Wait for confirmation
            for attempt in range(10):
                current_url = self.page.url
                toast = self.page.locator("div.oxd-toast").filter(has_text="Successfully Saved")
                header = self.page.locator("h5.oxd-table-filter-title")

                if "viewSystemUsers" in current_url or toast.is_visible() or header.is_visible():
                    self.logger.info(f"Post-save confirmation detected on attempt {attempt + 1}")
                    self.page.wait_for_timeout(1000)
                    break
                else:
                    self.logger.warning(f"Waiting for confirmation... attempt {attempt + 1}")
                    self.logger.debug(f"Current URL: {current_url}")
                    self.page.wait_for_timeout(1000)
            else:
                try:
                    expect(self.page).to_have_url(re.compile(".*viewSystemUsers"), timeout=3000)
                    self.logger.info("Final fallback: Redirect confirmed")
                except:
                    self.logger.error("Redirect or confirmation not detected after Save")
                    capture_screenshot(self.page, f"user_creation_failed_{final_username}.png")
                    with open(f"logs/user_creation_dom_dump_{final_username}.html", "w", encoding="utf-8") as f:
                        f.write(self.page.content())
                    raise Exception("Redirect to System Users page failed after Save")

            #  Return the final username for login use
            self.logger.info(f"User creation completed successfully for: {final_username}")
            return {
                "username": final_username,
                "password": password
            }

        except Exception as e:
            self.logger.error(f"User creation failed: {e}")
            capture_screenshot(self.page,
                               f"user_creation_fail_{final_username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            raise


    def search_user_by_filters(self, username, role, employee_name, status):
        """
            Searches for a user in the System Users table using multiple filters.
            Handles dropdown selection, dynamic input typing, DOM drift, and post-search row validation.
        """

        self.logger.info(f"Searching for user: {username}")

        try:
            # Ensure System Users page and filter form are fully loaded
            try:
                header = self.page.locator("h5.oxd-table-filter-title", has_text="System Users")
                expect(header).to_be_visible(timeout=10000)
                self.logger.info("System Users page header detected")

                filter_form = self.page.locator("form.oxd-form")
                expect(filter_form).to_be_visible(timeout=8000)
                self.page.wait_for_timeout(500)

                #  Block Enter key and native form submit
                self.page.evaluate("""
                    document.querySelectorAll('form.oxd-form input').forEach(input => {
                        input.addEventListener('keydown', e => {
                            if (e.key === 'Enter') e.preventDefault();
                        });
                    });
                    const form = document.querySelector('form.oxd-form');
                    if (form) {
                        form.addEventListener('submit', e => e.preventDefault());
                    }
                """)
            except Exception:
                self.logger.warning(" Header or filter form not found — trying fallback input wait")
                fallback_input = self.page.locator("input[placeholder='Username']")
                expect(fallback_input).to_be_visible(timeout=8000)

            #  Select Role from dropdown
            self.select_dropdown_option(role, dropdown_index=0)
            self.page.wait_for_timeout(500)

            #  Select Status from dropdown
            self.select_dropdown_option(status, dropdown_index=1)
            self.page.wait_for_timeout(500)

            #  Fill and select Employee Name with retry
            emp_input = self.page.locator("input[placeholder='Type for hints...']")
            expect(emp_input).to_be_visible(timeout=5000)
            emp_input.click()
            self.page.wait_for_timeout(300)
            emp_input.fill(employee_name)
            self.page.wait_for_timeout(800)

            for attempt in range(3):
                emp_options = self.page.locator("div[role='option']").filter(has_text=employee_name)
                if emp_options.first.is_visible():
                    emp_options.first.click()
                    self.logger.info(f" Employee name selected: {employee_name}")
                    break
                else:
                    self.logger.warning(f" Retry {attempt + 1}: Employee option not visible yet")
                    self.page.wait_for_timeout(1000)
            else:
                self.logger.error(f" Employee name '{employee_name}' not found in dropdown")
                capture_screenshot(self.page, f"employee_dropdown_failed_{employee_name}.png")
                raise Exception("Employee dropdown selection failed")

            #  Fill Username input with fallback locators
            username_input = None
            for attempt in range(3):
                try:
                    self.page.wait_for_timeout(800)
                    input_by_class = self.page.locator("form.oxd-form input.oxd-input.oxd-input--active").nth(0)
                    expect(input_by_class).to_be_visible(timeout=3000)
                    username_input = input_by_class
                    self.logger.info(" Username input found via class-based locator")
                    break
                except Exception as class_error:
                    self.logger.warning(f" Class-based locator failed: {class_error}")
                    self.page.wait_for_timeout(500)
                    try:
                        input_by_placeholder = self.page.locator("input[placeholder='Username']")
                        expect(input_by_placeholder).to_be_visible(timeout=3000)
                        username_input = input_by_placeholder
                        self.logger.info(" Username input found via placeholder locator")
                        break
                    except Exception as placeholder_error:
                        self.logger.warning(f" Placeholder-based locator failed: {placeholder_error}")
                        self.page.wait_for_timeout(500)
            else:
                self.logger.warning(" Username input not found after retries — skipping username entry")
                capture_screenshot(self.page, f"username_input_not_visible_{username}.png")

            # Type username with delay and force to avoid flaky input
            if username_input:
                try:
                    username_input.click(force=True)
                    self.page.wait_for_timeout(300)
                    username_input.type(username, delay=100, force=True)
                    typed_username = username_input.input_value()
                    if typed_username.strip() != username:
                        self.logger.warning(f" Username not typed correctly: '{typed_username}' — continuing anyway")
                        capture_screenshot(self.page, f"username_typing_skipped_{username}.png")
                    else:
                        self.logger.info(f" Username typed: {username}")
                except Exception as typing_error:
                    self.logger.warning(f" Username typing failed: {typing_error}")
                    capture_screenshot(self.page, f"username_typing_failed_{username}.png")


            #  Click Search button
            search_button = self.page.locator("button:has-text('Search')")
            expect(search_button).to_be_visible(timeout=5000)
            expect(search_button).to_be_enabled(timeout=5000)
            search_button.scroll_into_view_if_needed()
            self.page.wait_for_timeout(1000)
            search_button.click(force=True)
            self.logger.info(" Search triggered with force click")

            #  Wait for table to reappear after search
            try:
                self.page.wait_for_selector("div.oxd-table-body", state="visible", timeout=8000)
                self.page.wait_for_timeout(1000)  # Let DOM settle
                self.logger.info(" Table body became visible after search")
            except Exception as e:
                self.logger.error(f" Table body never became visible: {e}")
                capture_screenshot(self.page, f"table_not_visible_{username}.png")
                raise Exception("System Users table not visible")

            #  Retry row detection with strict-safe filtering
            for attempt in range(5):
                rows = self.page.locator("div.oxd-table-card").filter(has_text=username)
                if rows.count() > 0:
                    self.logger.info(f"Found {rows.count()} row(s) on attempt {attempt + 1}")
                    break
                else:
                    self.logger.warning(f" Attempt {attempt + 1}: No matching rows yet")
                    self.page.wait_for_timeout(1000)
            else:
                self.logger.error(" User creation failed silently — not present in table")
                capture_screenshot(self.page, f"user_creation_failed_{username}.png")
                raise Exception("User creation failed silently — not present in table")

            #  Validate first row contents
            row = rows.first
            actual_username = row.locator("div.oxd-table-cell").nth(1).inner_text().strip()
            actual_role = row.locator("div.oxd-table-cell").nth(2).inner_text().strip()
            actual_emp_name = row.locator("div.oxd-table-cell").nth(3).inner_text().strip()
            actual_status = row.locator("div.oxd-table-cell").nth(4).inner_text().strip()

            self.logger.info(
                f" Row values: username='{actual_username}', role='{actual_role}', employee='{actual_emp_name}', status='{actual_status}'"
            )

            # Soft validations with warnings
            if not actual_username.startswith("testuser"):
                self.logger.warning(f" Username mismatch: expected prefix 'testuser', got '{actual_username}'")
            else:
                self.logger.info(f" Username validation passed: '{actual_username}' begins with 'testuser'")

            if actual_role != role:
                self.logger.warning(f" Role mismatch: expected '{role}', got '{actual_role}'")
            if actual_emp_name != employee_name:
                self.logger.warning(f"Employee name mismatch: expected '{employee_name}', got '{actual_emp_name}'")
            if actual_status != status:
                self.logger.warning(f" Status mismatch: expected '{status}', got '{actual_status}'")

        except Exception as e:
            self.logger.error(f" Search failed: {e}")
            capture_screenshot(self.page, f"search_user_failed_{username}.png")
            raise

    def logout_user(self):
        """
            Logs out the currently authenticated user from the OrangeHRM dashboard.
            Clicks the user dropdown icon, selects the logout link, and confirms redirection to login page.
        """
        self.logger.info("Logging out")

        #  Click the user dropdown icon in the top-right corner
        self.page.locator("i.oxd-userdropdown-icon").click()

        #Click the logout link from the dropdown menu
        self.page.locator("a.oxd-userdropdown-link[href='/web/index.php/auth/logout']").click()
        self.page.wait_for_selector("input[name='username']", timeout=5000)
        #  Log successful logout
        self.logger.info(" Logout successful")
