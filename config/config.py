import os
import json
from pathlib import Path

# Project paths
ROOT_DIR = Path(__file__).parent.parent
REPORTS_DIR = ROOT_DIR / 'reports'
SCREENSHOTS_DIR = REPORTS_DIR / 'screenshots'
LOGS_DIR = ROOT_DIR / 'logs'

# Ensure directories exist
REPORTS_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Browser configuration
BROWSER = os.environ.get('BROWSER', 'chrome')
HEADLESS = os.environ.get('HEADLESS', 'False').lower() == 'true'

# Environment configuration
ENV = os.environ.get('ENV', 'prod')

# Environment URLs
ENVIRONMENTS = {
    'prod': {
        'base_url': 'http://the-internet.herokuapp.com',
    },
    'staging': {
        'base_url': 'http://staging-the-internet.herokuapp.com',
    },
    'dev': {
        'base_url': 'http://dev-the-internet.herokuapp.com',
    }
}

# URL configuration
BASE_URL = ENVIRONMENTS.get(ENV, ENVIRONMENTS['prod'])['base_url']
LOGIN_URL = f'{BASE_URL}/login'

# Test data
TEST_DATA = {
    'valid_user': {
        'username': 'tomsmith',
        'password': 'SuperSecretPassword!'
    },
    'invalid_user': {
        'username': 'invalid_user',
        'password': 'invalid_password'
    }
}

# For backward compatibility
VALID_USERNAME = TEST_DATA['valid_user']['username']
VALID_PASSWORD = TEST_DATA['valid_user']['password']

# Timeouts
IMPLICIT_WAIT = int(os.environ.get('IMPLICIT_WAIT', 10))
EXPLICIT_WAIT = int(os.environ.get('EXPLICIT_WAIT', 20))

# Retry configuration
MAX_RETRIES = int(os.environ.get('MAX_RETRIES', 3))
RETRY_DELAY = int(os.environ.get('RETRY_DELAY', 2))

# Logging configuration
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


def get_test_data(data_file=None):
    """
    Get test data from JSON file or use default.
    
    Args:
        data_file: Path to JSON file with test data
        
    Returns:
        dict: Test data
    """
    if data_file and os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return json.load(f)
    
    return TEST_DATA 