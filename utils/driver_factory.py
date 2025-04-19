from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config.config import BROWSER, HEADLESS, IMPLICIT_WAIT
import logging


class DriverFactory:
    """Factory class for creating WebDriver instances based on configuration."""
    
    @staticmethod
    def get_driver():
        """
        Create and return a WebDriver instance based on the configured browser.
        
        Returns:
            WebDriver: A configured Selenium WebDriver instance.
        """
        logging.info(f"Initializing {BROWSER} browser (headless: {HEADLESS})")
        
        if BROWSER.lower() == "chrome":
            options = webdriver.ChromeOptions()
            if HEADLESS:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-extensions")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-gpu")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        elif BROWSER.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            if HEADLESS:
                options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        elif BROWSER.lower() == "edge":
            options = webdriver.EdgeOptions()
            if HEADLESS:
                options.add_argument("--headless")
            options.add_argument("--start-maximized")
            driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
        else:
            raise ValueError(f"Unsupported browser: {BROWSER}")
        
        # Set implicit wait
        driver.implicitly_wait(IMPLICIT_WAIT)
        # Set window size if not already maximized in options
        if BROWSER.lower() != "firefox":
            driver.maximize_window()
        
        return driver 