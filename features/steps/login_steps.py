from pytest_bdd import given, when, then, parsers
from pages.login_page import LoginPage
from pages.secure_page import SecurePage
from utils.logger import get_logger
from config.config import TEST_DATA

# Initialize logger
logger = get_logger()


@given("I am on the login page")
def on_login_page(driver):
    """Navigate to the login page."""
    logger.info("Navigating to the login page")
    login_page = LoginPage(driver)
    login_page.navigate()


@when(parsers.parse('I enter "{username}" as username'))
def enter_username(driver, username):
    """
    Enter the specified username.
    
    Args:
        driver: WebDriver instance
        username: Username to enter, can be a variable reference
    """
    logger.info(f"Entering username: {username}")
    
    # Check if the username is a reference to test data
    if username.startswith('$'):
        # Format: $dataset.key, e.g., $valid_user.username
        parts = username[1:].split('.')
        if len(parts) == 2:
            dataset, key = parts
            if dataset in TEST_DATA and key in TEST_DATA[dataset]:
                username = TEST_DATA[dataset][key]
                logger.info(f"Resolved username from test data: {username}")
    
    login_page = LoginPage(driver)
    login_page.enter_username(username)


@when(parsers.parse('I enter "{password}" as password'))
def enter_password(driver, password):
    """
    Enter the specified password.
    
    Args:
        driver: WebDriver instance
        password: Password to enter, can be a variable reference
    """
    logger.info(f"Entering password: {'*' * len(password)}")
    
    # Check if the password is a reference to test data
    if password.startswith('$'):
        # Format: $dataset.key, e.g., $valid_user.password
        parts = password[1:].split('.')
        if len(parts) == 2:
            dataset, key = parts
            if dataset in TEST_DATA and key in TEST_DATA[dataset]:
                password = TEST_DATA[dataset][key]
                logger.info(f"Resolved password from test data")
    
    login_page = LoginPage(driver)
    login_page.enter_password(password)


@when("I click the login button")
def click_login_button(driver):
    """Click the login button."""
    logger.info("Clicking login button")
    login_page = LoginPage(driver)
    login_page.click_login_button()


@then("I should be logged in successfully")
def verify_successful_login(driver):
    """Verify that login was successful."""
    logger.info("Verifying successful login")
    secure_page = SecurePage(driver)
    assert secure_page.is_element_visible(secure_page.SUCCESS_MESSAGE), "Success message is not displayed"
    success_message = secure_page.get_success_message()
    assert "You logged into a secure area!" in success_message, f"Unexpected success message: {success_message}"
    logger.info(f"Success message verified: {success_message}")


@then("I should see the secure area page")
def verify_secure_area_page(driver):
    """Verify that the secure area page is displayed."""
    logger.info("Verifying secure area page is displayed")
    secure_page = SecurePage(driver)
    assert secure_page.is_secure_page_displayed(), "Secure page is not displayed"
    logger.info("Secure area page verified")


@then("I should see an error message")
def verify_error_message(driver):
    """Verify that an error message is displayed."""
    logger.info("Verifying error message is displayed")
    login_page = LoginPage(driver)
    assert login_page.is_element_visible(login_page.LOGIN_ERROR_MESSAGE), "Error message is not displayed"
    logger.info("Error message verified")


@then(parsers.parse('The error message should contain "{expected_text}"'))
def verify_error_message_text(driver, expected_text):
    """
    Verify that the error message contains the expected text.
    
    Args:
        driver: WebDriver instance
        expected_text: Text expected to be in the error message, can be a variable reference
    """
    logger.info(f"Verifying error message contains: {expected_text}")
    
    # Check if the expected_text is a reference to test data
    if expected_text.startswith('$'):
        # Format: $error_messages.invalid_username
        parts = expected_text[1:].split('.')
        if len(parts) == 2:
            dataset, key = parts
            if dataset in TEST_DATA and key in TEST_DATA[dataset]:
                expected_text = TEST_DATA[dataset][key]
                logger.info(f"Resolved expected text from test data: {expected_text}")
    
    login_page = LoginPage(driver)
    error_message = login_page.get_error_message()
    assert expected_text in error_message, f"Error message '{error_message}' does not contain '{expected_text}'"
    logger.info(f"Error message verified: {error_message}") 