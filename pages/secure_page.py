from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SecurePage(BasePage):
    """Page object representing the secure page after successful login."""
    
    # Locators
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".flash.success")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "a.button")
    SECURE_AREA_HEADER = (By.CSS_SELECTOR, "h2")
    
    def __init__(self, driver):
        """Initialize SecurePage with driver."""
        super().__init__(driver)
    
    def get_success_message(self):
        """
        Get the success message text.
        
        Returns:
            str: The success message text
        """
        return self.get_text(self.SUCCESS_MESSAGE)
    
    def is_secure_page_displayed(self):
        """
        Check if the secure page is displayed.
        
        Returns:
            bool: True if the secure page is displayed, False otherwise
        """
        return self.is_element_visible(self.SECURE_AREA_HEADER) and "Secure Area" in self.get_text(self.SECURE_AREA_HEADER)
    
    def logout(self):
        """
        Click the logout button.
        
        Returns:
            SecurePage: Self reference for method chaining
        """
        self.click(self.LOGOUT_BUTTON)
        return self 