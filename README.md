# Web Automation Testing Framework

A test automation framework built with Python, pytest-bdd, and Selenium using the Page Object Model (POM) design pattern.

## Project Structure

```
├── config/             # Configuration files
├── features/           # BDD feature files
│   └── steps/          # Step definitions
├── logs/               # Test execution logs
├── pages/              # Page objects
├── reports/            # Test reports 
│   └── screenshots/    # Test failure screenshots
├── tests/              # Test scripts
└── utils/              # Utility functions and classes
```

## Requirements

- Python 3.x
- pip (Python package manager)
- Web browsers (Chrome, Firefox, or Edge)

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

3. Install the required packages:
   ```
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Running Tests

### Using pytest directly

To run all tests:

```
pytest
```

To run a specific test:

```
pytest tests/test_login.py
```

### Using the runner script

The framework includes a convenient runner script that provides various options:

```
python run_tests.py --headless --report --verbose
```

Available options:

- `--browser`, `-b`: Browser to use (chrome, firefox, edge)
- `--headless`: Run in headless mode
- `--path`, `-p`: Path to test files/directories
- `--markers`, `-m`: Run tests with specific pytest markers
- `--report`, `-r`: Generate HTML report
- `--report-name`: Custom report name (default: report_<timestamp>.html)
- `--verbose`, `-v`: Verbose output
- `--parallel`, `-n`: Number of parallel processes (default: 0 for no parallelism)
- `--reruns`: Number of times to retry failed tests (default: 0)
- `--log-level`: Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `--tags`: Run tests with specific BDD tags
- `--skip-browser-update`: Skip automatic browser driver update
- `--clean`: Clean reports and screenshots before running

Examples:

```bash
# Run all tests in headless mode with Chrome and generate a report
python run_tests.py --headless --report

# Run specific tests with Firefox
python run_tests.py --browser firefox --path tests/test_login.py

# Run tests with a specific marker
python run_tests.py --markers "smoke" --report

# Run tests in parallel (2 processes)
python run_tests.py --parallel 2 --headless --report

# Clean previous reports and run tests
python run_tests.py --clean --headless --report

# Generate a report with a custom name
python run_tests.py --headless --report --report-name final_report.html

# Set a specific log level
python run_tests.py --headless --log-level DEBUG
```

## HTML Test Reports

The framework is configured to generate HTML test reports with screenshots for failed tests.

Reports are saved in the `reports` directory with a timestamp-based filename (e.g., `report_20250420_005002.html`).

Screenshots of any test failures are automatically captured and embedded in the report, and are also saved in the `reports/screenshots` directory.

## Logging

The framework includes a comprehensive logging system that logs test execution details:

- Test execution logs are saved in the `logs` directory
- Different log levels are supported (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Logs are created with timestamps for traceability

## Configuration

You can configure the test execution using various methods:

### Environment Variables

- `BROWSER`: The browser to use (chrome, firefox, or edge). Default is chrome.
- `HEADLESS`: Whether to run the browser in headless mode (true or false). Default is false.
- `ENV`: Environment to use (prod, staging, dev). Default is prod.
- `IMPLICIT_WAIT`: Implicit wait time in seconds. Default is 10.
- `EXPLICIT_WAIT`: Explicit wait time in seconds. Default is 20.
- `MAX_RETRIES`: Maximum number of retries for failed operations. Default is 3.
- `LOG_LEVEL`: Default logging level. Default is INFO.

Example:
```
BROWSER=firefox HEADLESS=true ENV=staging pytest
```

### Test Data

Test data is configured in `config/config.py` with support for environment-specific configurations. You can refer to test data in feature files using the `$` prefix:

```gherkin
Scenario: Successful login with valid credentials
  Given I am on the login page
  When I enter "$valid_user.username" as username
  And I enter "$valid_user.password" as password
  And I click the login button
  Then I should be logged in successfully
```

## Example Scenario

The framework includes example scenarios that test the login functionality of [The Internet Herokuapp](http://the-internet.herokuapp.com/login).

The tests verify:
1. Successful login with valid credentials
2. Failed login with invalid credentials

## Development

### Adding to .gitignore

The repository includes a `.gitignore` file that excludes common files and directories not needed in version control:

- Python bytecode files
- Virtual environments
- Test reports and artifacts
- Logs
- IDE-specific files
- Temporary files 