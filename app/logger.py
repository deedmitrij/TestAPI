import logging
import os
import time

from config import LOGS_DIR


logger = logging.getLogger(__name__)


def setup_logging():
    """Setup logging configuration."""
    # Create the logs directory if it doesn't exist
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    # Create a new file handler for each session
    session_timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    log_file = f"{LOGS_DIR}/session_{session_timestamp}.log"
    file_handler = logging.FileHandler(log_file)

    # Configure the file handler and add it to the logger
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Set the log level to capture general runtime information
    logger.setLevel(logging.INFO)
