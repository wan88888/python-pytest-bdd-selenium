from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import LOGIN_URL


class LoginPage(BasePage):
    """Page object representing the login page."""
    
    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOGIN_ERROR_MESSAGE = (By.ID, "flash-messages")
    LOGIN_SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".flash.success")
    
    def __init__(self, driver):
        """Initialize LoginPage with driver."""
        super().__init__(driver)
    
    def navigate(self):
        """Navigate to the login page."""
        self.navigate_to(LOGIN_URL)
        return self
    
    def enter_username(self, username):
        """
        Enter username in the username field.
        
        Args:
            username: Username to enter
        
        Returns:
            LoginPage: Self reference for method chaining
        """
        self.send_keys(self.USERNAME_INPUT, username)
        return self
    
    def enter_password(self, password):
        """
        Enter password in the password field.
        
        Args:
            password: Password to enter
        
        Returns:
            LoginPage: Self reference for method chaining
        """
        self.send_keys(self.PASSWORD_INPUT, password)
        return self
    
    def click_login_button(self):
        """
        Click the login button.
        
        Returns:
            LoginPage: Self reference for method chaining
        """
        self.click(self.LOGIN_BUTTON)
        return self
    
    def login(self, username, password):
        """
        Perform login with provided credentials.
        
        Args:
            username: Username to enter
            password: Password to enter
        
        Returns:
            LoginPage: Self reference for method chaining
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        return self
    
    def is_login_successful(self):
        """
        Check if login was successful based on success message.
        
        Returns:
            bool: True if login was successful, False otherwise
        """
        return self.is_element_visible(self.LOGIN_SUCCESS_MESSAGE)
    
    def get_error_message(self):
        """
        Get the login error message.
        
        Returns:
            str: The error message text
        """
        return self.get_text(self.LOGIN_ERROR_MESSAGE) 