import pytest
from datetime import datetime

# Entry point for executing smoke tests across multiple browsers.
# Encapsulates logic for looping through configurations

def run_smoke_browser_tests():
    # Defines a list of tuples mapping Pytest markers to browser names.
    configs = [
        ("chrome", "chrome"),
        ("edge", "edge"),
        ("firefox", "firefox")
    ]

    #  Iterates through each browser configuration and prints a status message.
    for marker, browser in configs:
        print(f"\nRunning SMOKE tests on {browser.upper()}...")

        # Generates a unique timestamped report filename per browser.
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_name = f"report_smoke_{browser}_{timestamp}.html"

        pytest.main([
            "guvi_automation/tests/",   #  Path to test directory

            "-m", f"smoke and {marker}", # Marker-based filtering for smoke + browser

            f"--browser={browser}", # Custom CLI option to select browser

            f"--html={report_name}", # Output HTML report with dynamic name

            "--self-contained-html"  # Ensures report is standalone with embedded assets
        ])



if __name__ == "__main__":
    run_smoke_browser_tests()