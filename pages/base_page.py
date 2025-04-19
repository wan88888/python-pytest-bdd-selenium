from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from utils.logger import get_logger
from config.config import EXPLICIT_WAIT


class BasePage:
    """Base class for all page objects."""
    
    def __init__(self, driver):
        """
        Initialize the BasePage with a driver.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)
        self.logger = get_logger()
    
    def navigate_to(self, url):
        """
        Navigate to a specified URL.
        
        Args:
            url: The URL to navigate to
        """
        self.logger.info(f"Navigating to {url}")
        self.driver.get(url)
    
    def find_element(self, locator):
        """
        Find an element on the page using the provided locator.
        
        Args:
            locator: Tuple containing (By, value)
        
        Returns:
            WebElement: The found element
        """
        try:
            return self.driver.find_element(*locator)
        except NoSuchElementException as e:
            self.logger.error(f"Element not found with locator: {locator}")
            raise e
    
    def find_elements(self, locator):
        """
        Find elements on the page using the provided locator.
        
        Args:
            locator: Tuple containing (By, value)
        
        Returns:
            List[WebElement]: The found elements
        """
        return self.driver.find_elements(*locator)
    
    def is_element_visible(self, locator, timeout=EXPLICIT_WAIT):
        """
        Check if an element is visible on the page.
        
        Args:
            locator: Tuple containing (By, value)
            timeout: Maximum time to wait for the element
        
        Returns:
            bool: True if element is visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            self.logger.info(f"Element not visible within {timeout} seconds: {locator}")
            return False
    
    def is_element_present(self, locator, timeout=EXPLICIT_WAIT):
        """
        Check if an element is present in the DOM.
        
        Args:
            locator: Tuple containing (By, value)
            timeout: Maximum time to wait for the element
        
        Returns:
            bool: True if element is present, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            self.logger.info(f"Element not present within {timeout} seconds: {locator}")
            return False
    
    def wait_for_element_visible(self, locator, timeout=EXPLICIT_WAIT):
        """
        Wait for an element to become visible.
        
        Args:
            locator: Tuple containing (By, value)
            timeout: Maximum time to wait
        
        Returns:
            WebElement: The visible element
        """
        try:
            self.logger.debug(f"Waiting for element to be visible: {locator}")
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException as e:
            self.logger.error(f"Element not visible within {timeout} seconds: {locator}")
            raise e
    
    def wait_for_element_clickable(self, locator, timeout=EXPLICIT_WAIT):
        """
        Wait for an element to become clickable.
        
        Args:
            locator: Tuple containing (By, value)
            timeout: Maximum time to wait
        
        Returns:
            WebElement: The clickable element
        """
        try:
            self.logger.debug(f"Waiting for element to be clickable: {locator}")
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException as e:
            self.logger.error(f"Element not clickable within {timeout} seconds: {locator}")
            raise e
    
    def wait_for_element_to_disappear(self, locator, timeout=EXPLICIT_WAIT):
        """
        Wait for an element to disappear from the page.
        
        Args:
            locator: Tuple containing (By, value)
            timeout: Maximum time to wait
        
        Returns:
            bool: True if the element disappeared
        """
        try:
            self.logger.debug(f"Waiting for element to disappear: {locator}")
            return WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
        except TimeoutException as e:
            self.logger.error(f"Element still visible after {timeout} seconds: {locator}")
            raise e
    
    def click(self, locator, timeout=EXPLICIT_WAIT):
        """
        Click on an element after ensuring it's clickable.
        
        Args:
            locator: Tuple containing (By, value)
            timeout: Maximum time to wait
        """
        try:
            element = self.wait_for_element_clickable(locator, timeout)
            self.logger.debug(f"Clicking element: {locator}")
            element.click()
        except (TimeoutException, StaleElementReferenceException) as e:
            self.logger.error(f"Failed to click element: {locator}")
            raise e
    
    def js_click(self, locator):
        """
        Click an element using JavaScript.
        
        Args:
            locator: Tuple containing (By, value)
        """
        element = self.find_element(locator)
        self.logger.debug(f"JavaScript clicking element: {locator}")
        self.driver.execute_script("arguments[0].click();", element)
    
    def send_keys(self, locator, text, clear_first=True, timeout=EXPLICIT_WAIT):
        """
        Send text to an element after ensuring it's visible.
        
        Args:
            locator: Tuple containing (By, value)
            text: Text to send to the element
            clear_first: Whether to clear the field first
            timeout: Maximum time to wait
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            if clear_first:
                element.clear()
            self.logger.debug(f"Sending text to element {locator}: {text}")
            element.send_keys(text)
        except (TimeoutException, StaleElementReferenceException) as e:
            self.logger.error(f"Failed to send text to element: {locator}")
            raise e
    
    def clear_and_send_keys(self, locator, text, timeout=EXPLICIT_WAIT):
        """
        Clear field and send text using different strategies to ensure the field is cleared.
        
        Args:
            locator: Tuple containing (By, value)
            text: Text to send
            timeout: Maximum time to wait
        """
        element = self.wait_for_element_visible(locator, timeout)
        element.clear()
        # Additional clearing with Ctrl+A and Delete
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(text)
    
    def get_text(self, locator, timeout=EXPLICIT_WAIT):
        """
        Get text from an element after ensuring it's visible.
        
        Args:
            locator: Tuple containing (By, value)
            timeout: Maximum time to wait
        
        Returns:
            str: The element's text content
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            return element.text
        except (TimeoutException, StaleElementReferenceException) as e:
            self.logger.error(f"Failed to get text from element: {locator}")
            raise e
    
    def get_attribute(self, locator, attribute, timeout=EXPLICIT_WAIT):
        """
        Get attribute value from an element.
        
        Args:
            locator: Tuple containing (By, value)
            attribute: Name of the attribute
            timeout: Maximum time to wait
        
        Returns:
            str: The attribute value
        """
        element = self.wait_for_element_visible(locator, timeout)
        return element.get_attribute(attribute)
    
    def hover_over(self, locator, timeout=EXPLICIT_WAIT):
        """
        Hover over an element.
        
        Args:
            locator: Tuple containing (By, value)
            timeout: Maximum time to wait
        """
        element = self.wait_for_element_visible(locator, timeout)
        ActionChains(self.driver).move_to_element(element).perform()
    
    def drag_and_drop(self, source_locator, target_locator, timeout=EXPLICIT_WAIT):
        """
        Perform drag and drop operation.
        
        Args:
            source_locator: Tuple containing (By, value) for source element
            target_locator: Tuple containing (By, value) for target element
            timeout: Maximum time to wait
        """
        source = self.wait_for_element_visible(source_locator, timeout)
        target = self.wait_for_element_visible(target_locator, timeout)
        ActionChains(self.driver).drag_and_drop(source, target).perform()
    
    def switch_to_frame(self, locator=None, timeout=EXPLICIT_WAIT):
        """
        Switch to an iframe.
        
        Args:
            locator: Tuple containing (By, value), or None for default content
            timeout: Maximum time to wait
        """
        if locator:
            frame = self.wait_for_element_visible(locator, timeout)
            self.driver.switch_to.frame(frame)
        else:
            self.driver.switch_to.default_content()
    
    def switch_to_window(self, window_index=0):
        """
        Switch to a window by index.
        
        Args:
            window_index: Index of the window to switch to
        """
        windows = self.driver.window_handles
        if window_index < len(windows):
            self.driver.switch_to.window(windows[window_index])
        else:
            self.logger.error(f"Window index {window_index} out of bounds")
            raise IndexError(f"Window index {window_index} out of bounds")
    
    def scroll_to_element(self, locator, timeout=EXPLICIT_WAIT):
        """
        Scroll to an element.
        
        Args:
            locator: Tuple containing (By, value)
            timeout: Maximum time to wait
        """
        element = self.wait_for_element_present(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def wait_for_page_load(self, timeout=EXPLICIT_WAIT):
        """
        Wait for page to completely load.
        
        Args:
            timeout: Maximum time to wait
        """
        self.logger.debug("Waiting for page to load")
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    
    def get_current_url(self):
        """
        Get the current URL.
        
        Returns:
            str: The current URL
        """
        return self.driver.current_url
    
    def get_title(self):
        """
        Get the page title.
        
        Returns:
            str: The page title
        """
        return self.driver.title
    
    def refresh_page(self):
        """Refresh the current page."""
        self.logger.debug("Refreshing page")
        self.driver.refresh()
        self.wait_for_page_load()
    
    def go_back(self):
        """Navigate back to the previous page."""
        self.logger.debug("Navigating back")
        self.driver.back()
        self.wait_for_page_load()
    
    def go_forward(self):
        """Navigate forward to the next page."""
        self.logger.debug("Navigating forward")
        self.driver.forward()
        self.wait_for_page_load()
    
    def is_element_enabled(self, locator, timeout=EXPLICIT_WAIT):
        """
        Check if element is enabled.
        
        Args:
            locator: Tuple containing (By, value)
            timeout: Maximum time to wait
        
        Returns:
            bool: True if element is enabled, False otherwise
        """
        element = self.wait_for_element_present(locator, timeout)
        return element.is_enabled()
    
    def is_element_selected(self, locator, timeout=EXPLICIT_WAIT):
        """
        Check if element is selected.
        
        Args:
            locator: Tuple containing (By, value)
            timeout: Maximum time to wait
        
        Returns:
            bool: True if element is selected, False otherwise
        """
        element = self.wait_for_element_present(locator, timeout)
        return element.is_selected()
    
    def wait_for_text_to_be_present(self, locator, text, timeout=EXPLICIT_WAIT):
        """
        Wait for text to be present in element.
        
        Args:
            locator: Tuple containing (By, value)
            text: Text to wait for
            timeout: Maximum time to wait
        
        Returns:
            bool: True if text is present, False otherwise
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
        except TimeoutException:
            self.logger.info(f"Text '{text}' not present in element {locator} within {timeout} seconds")
            return False 