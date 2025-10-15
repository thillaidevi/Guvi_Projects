import logging
from datetime import datetime
import json
import os
from logging.handlers import RotatingFileHandler

# Setup rotating log for human-readable output
log_handler = RotatingFileHandler("test_execution.log", maxBytes=5*1024*1024, backupCount=3)
log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

def log_result(test_name, status, screenshot_path=None, error=None):
    if screenshot_path and not os.path.exists(screenshot_path):
        screenshot_path = None

    result = {
        "test_name": test_name,
        "status": status,
        "screenshot": screenshot_path,
        "error": str(error) if error else None,
        "timestamp": datetime.now().isoformat()
    }

    # Write structured log to JSON
    log_file = os.path.join(os.getcwd(), "results.json")
    with open(log_file, "a") as f:
        f.write(json.dumps(result) + "\n")

    # Also log to rotating log file
    logger.info(f"{test_name} - {status} - Screenshot: {screenshot_path} - Error: {error}")