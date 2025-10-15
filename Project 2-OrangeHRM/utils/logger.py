import logging
import os
from datetime import datetime

# Internal cache to avoid duplicate logger creation
_loggers = {}

def get_logger(name="TestLogger"):
    """
        Creates and returns a logger with both file and console handlers.
        Each logger writes to a timestamped log file under 'results/logs'.
        Ensures consistent formatting and avoids duplicate handlers.
    """
    #  Create log directory if it doesn't exist
    log_dir = "results/logs"
    os.makedirs(log_dir, exist_ok=True)

    # Generate timestamped log filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"{name}_{timestamp}.log")

    # Initialize logger with DEBUG level
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    #  File handler: captures full debug-level logs
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Console handler: shows INFO-level logs in terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    #  Unified log format for both handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    #  Attach handlers only once to avoid duplication
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

     # Cache logger instance for reuse
    _loggers[name] = logger
    return logger