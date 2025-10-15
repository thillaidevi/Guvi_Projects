"""
Capture the screenshot of the current browser and save it along with the report file.
Which is useful for debugging and gracefully handles exception if screenshot capture fails
"""

def capture_error(driver, name="error"):
    try:
        driver.save_screenshot(f"reports/{name}.png")
    except Exception as e:
        print(f"Screenshot capture failed: {e}")