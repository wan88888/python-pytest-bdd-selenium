import logging
import os
import datetime


def setup_logger(log_level=logging.INFO):
    """
    Setup and configure logger for the test framework.
    
    Args:
        log_level: The logging level (default: INFO)
    
    Returns:
        The configured logger instance
    """
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Configure logger
    logger = logging.getLogger("test_framework")
    logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    if logger.handlers:
        logger.handlers.clear()
    
    # Create file handler for output to file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(logs_dir, f"test_log_{timestamp}.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    
    # Create console handler for output to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Get a logger instance with default configuration
def get_logger():
    """
    Get a configured logger instance.
    
    Returns:
        Logger: A configured logger instance
    """
    return setup_logger() 