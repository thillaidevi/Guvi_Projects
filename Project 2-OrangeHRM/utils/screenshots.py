import os,re
from datetime import datetime

def capture_screenshot(page, test_name, suite_name="default_suite"):
    """
        Captures a full-page screenshot and saves it under a structured directory.
        Filenames are timestamped and sanitized to avoid filesystem issues.

        Args:
            page: Playwright Page object
            test_name: Name of the test case (used in filename)
            suite_name: Logical grouping or suite name (used as folder name)

        Returns:
            Full path to the saved screenshot file
        """
    # Generate timestamp for uniqueness
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    #  Sanitize test and suite names to ensure safe filenames
    safe_test_name = re.sub(r'[^\w\-_.]', '_', test_name)
    safe_suite_name = re.sub(r'[^\w\-_.]', '_', suite_name)

    # Construct screenshot directory path
    screenshot_dir = os.path.join("results", "screenshots", safe_suite_name)
    os.makedirs(screenshot_dir, exist_ok=True)

    # Build full file path with sanitized name and timestamp
    file_path = os.path.join(screenshot_dir, f"{safe_test_name}_{timestamp}.png")

    #  Capture screenshot
    page.screenshot(path=file_path, full_page=True)
    return file_path
