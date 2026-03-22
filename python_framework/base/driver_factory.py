import os
import configparser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class DriverFactory:
    """Creates and configures WebDriver instances based on config settings."""

    CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.ini')

    @staticmethod
    def _load_config():
        config = configparser.ConfigParser()
        config.read(DriverFactory.CONFIG_PATH)
        return config

    @staticmethod
    def get_driver(browser_name=None, headless=None):
        config = DriverFactory._load_config()
        browser = (browser_name or config.get('browser', 'browser_name', fallback='chrome')).lower()
        is_headless = headless if headless is not None else config.getboolean('browser', 'headless', fallback=False)
        implicit_wait = config.getint('browser', 'implicit_wait', fallback=10)
        page_load_timeout = config.getint('browser', 'page_load_timeout', fallback=30)

        driver = DriverFactory._create_driver(browser, is_headless)
        driver.implicitly_wait(implicit_wait)
        driver.set_page_load_timeout(page_load_timeout)
        driver.maximize_window()
        return driver

    @staticmethod
    def _create_driver(browser, headless):
        if browser == 'chrome':
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-notifications')
            options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
            options.add_experimental_option('prefs', {
                'credentials_enable_service': False,
                'profile.password_manager_enabled': False,
                'profile.password_manager_leak_detection': False,
            })
            try:
                service = ChromeService(ChromeDriverManager().install())
                return webdriver.Chrome(service=service, options=options)
            except Exception:
                return webdriver.Chrome(options=options)

        elif browser == 'firefox':
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument('--headless')
            service = FirefoxService(GeckoDriverManager().install())
            return webdriver.Firefox(service=service, options=options)

        elif browser == 'edge':
            options = webdriver.EdgeOptions()
            if headless:
                options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-gpu')
            options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
            options.add_experimental_option('prefs', {
                'credentials_enable_service': False,
                'profile.password_manager_enabled': False,
                'profile.password_manager_leak_detection': False,
            })
            try:
                service = EdgeService(EdgeChromiumDriverManager().install())
                return webdriver.Edge(service=service, options=options)
            except Exception:
                return webdriver.Edge(options=options)

        else:
            raise ValueError(f"Unsupported browser: {browser}. Use 'chrome', 'firefox', or 'edge'.")
