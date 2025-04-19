import time
import random
import string
import re
import os
import json
from datetime import datetime
from pathlib import Path
from utils.logger import get_logger

logger = get_logger()


def wait_for(condition_function, timeout=30, poll_frequency=0.5, error_message=None):
    """
    Wait for a condition to be true.
    
    Args:
        condition_function: Function that returns True/False
        timeout: Maximum time to wait in seconds
        poll_frequency: How often to check the condition
        error_message: Message to include in the timeout exception
        
    Returns:
        The result of the condition function once it returns truthy
        
    Raises:
        TimeoutError: If the condition is not met within the timeout
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        result = condition_function()
        if result:
            return result
        time.sleep(poll_frequency)
    
    if error_message is None:
        error_message = f"Timed out waiting for condition after {timeout} seconds"
    
    logger.error(error_message)
    raise TimeoutError(error_message)


def generate_random_string(length=10, include_digits=True, include_special=False):
    """
    Generate a random string.
    
    Args:
        length: Length of the string
        include_digits: Whether to include digits
        include_special: Whether to include special characters
        
    Returns:
        str: The random string
    """
    chars = string.ascii_letters
    if include_digits:
        chars += string.digits
    if include_special:
        chars += string.punctuation
    
    return ''.join(random.choice(chars) for _ in range(length))


def generate_timestamp_string(format_string="%Y%m%d_%H%M%S"):
    """
    Generate a timestamp string.
    
    Args:
        format_string: Format string for datetime.strftime
        
    Returns:
        str: The timestamp string
    """
    return datetime.now().strftime(format_string)


def is_valid_email(email):
    """
    Check if a string is a valid email address.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def load_json_file(file_path):
    """
    Load a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        dict: The loaded JSON data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file is not valid JSON
    """
    path = Path(file_path)
    if not path.exists():
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {file_path}: {e}")
        raise


def save_json_file(data, file_path):
    """
    Save data to a JSON file.
    
    Args:
        data: Data to save
        file_path: Path to save the JSON file
        
    Returns:
        str: The file path
    """
    path = Path(file_path)
    
    # Create parent directories if they don't exist
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    
    return str(path)


def retry(func, max_attempts=3, delay=1, backoff=2, exceptions=(Exception,)):
    """
    Retry a function with exponential backoff.
    
    Args:
        func: Function to retry
        max_attempts: Maximum number of attempts
        delay: Initial delay between retries in seconds
        backoff: Backoff multiplier
        exceptions: Tuple of exceptions to catch
        
    Returns:
        The result of the function call
        
    Raises:
        The last exception if all attempts fail
    """
    attempt = 0
    while attempt < max_attempts:
        try:
            return func()
        except exceptions as e:
            attempt += 1
            if attempt == max_attempts:
                logger.error(f"All {max_attempts} attempts failed. Last error: {e}")
                raise
            
            sleep_time = delay * (backoff ** (attempt - 1))
            logger.warning(f"Attempt {attempt} failed: {e}. Retrying in {sleep_time:.1f} seconds...")
            time.sleep(sleep_time) 