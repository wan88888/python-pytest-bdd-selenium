import pytest
import os
import datetime
from pytest_bdd import given
from utils.driver_factory import DriverFactory
from utils.logger import get_logger
from pytest_html import extras
from config.config import SCREENSHOTS_DIR, LOGS_DIR

# Initialize logger
logger = get_logger()


@pytest.fixture(scope="function")
def driver(request):
    """
    Initialize WebDriver instance for tests.
    
    This fixture is used for each test function and sets up a fresh browser
    instance for each test. The browser closes automatically after the test.
    """
    logger.info(f"Starting test: {request.node.name}")
    
    driver = DriverFactory.get_driver()
    
    # Add driver to request for accessing in hook
    request.node.driver = driver
    
    yield driver
    
    # Teardown
    if driver:
        logger.info(f"Closing browser for test: {request.node.name}")
        driver.quit()


# Add hooks for pytest-bdd
def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    """Hook for test failures."""
    logger.error(f"Step failed in scenario '{scenario.name}', step: '{step.name}'")
    logger.error(f"Error: {str(exception)}")
    
    driver = step_func_args.get('driver')
    if driver:
        take_screenshot(driver, f"step_error_{scenario.name}_{step.name}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook for test failure to capture screenshots.
    
    This hook will capture screenshots on test failures and attach them to the HTML report.
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        if hasattr(item, "driver"):
            # Log test result
            if report.passed:
                logger.info(f"Test passed: {item.name}")
            elif report.failed:
                logger.error(f"Test failed: {item.name}")
                screenshot_path = take_screenshot(item.driver, f"test_failed_{item.name}")
                
                # Add screenshot to the HTML report
                report.extras = getattr(report, "extras", [])
                report.extras.append(extras.image(screenshot_path))
                report.extras.append(extras.html(f"<div>Screenshot saved to: {screenshot_path}</div>"))
            elif report.skipped:
                logger.info(f"Test skipped: {item.name}")


def take_screenshot(driver, name):
    """
    Take a screenshot and save it to the reports/screenshots directory.
    
    Args:
        driver: WebDriver instance
        name: Base name for the screenshot
    
    Returns:
        str: Path to the saved screenshot
    """
    # Ensure screenshots directory exists
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    
    # Create timestamp for unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOTS_DIR, filename)
    
    # Take screenshot
    driver.save_screenshot(filepath)
    logger.info(f"Screenshot saved: {filepath}")
    
    return filepath 