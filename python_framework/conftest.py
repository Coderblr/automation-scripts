"""
Pytest configuration and shared fixtures.
Handles browser setup/teardown, configuration loading, and reporting hooks.
"""

import os
import sys
import configparser
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from python_framework.base.driver_factory import DriverFactory
from python_framework.utils.logger_config import setup_logger

logger = setup_logger('conftest')

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini')


def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return config


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=None, help="Browser: chrome, firefox, edge")
    parser.addoption("--headless", action="store_true", default=False, help="Run in headless mode")
    parser.addoption("--base-url", action="store", default=None, help="Application base URL")
    parser.addoption("--api-url", action="store", default=None, help="API base URL")
    parser.addoption("--excel-file", action="store", default=None, help="Path to Excel test cases file")
    parser.addoption("--test-url", action="store", default=None, help="URL for smoke testing")
    parser.addoption("--sheet-name", action="store", default=None, help="Excel sheet name to use")


@pytest.fixture(scope='session')
def config():
    return load_config()


@pytest.fixture(scope='function')
def driver(request, config):
    browser = request.config.getoption("--browser") or config.get('browser', 'browser_name', fallback='chrome')
    headless = request.config.getoption("--headless") or config.getboolean('browser', 'headless', fallback=False)

    logger.info(f"Starting {browser} browser (headless={headless})")
    driver = DriverFactory.get_driver(browser_name=browser, headless=headless)

    yield driver

    logger.info("Closing browser")
    driver.quit()


@pytest.fixture(scope='session')
def base_url(request, config):
    return request.config.getoption("--base-url") or config.get('application', 'base_url', fallback='http://localhost:3000')


@pytest.fixture(scope='session')
def api_base_url(request, config):
    return request.config.getoption("--api-url") or config.get('application', 'api_base_url', fallback='http://localhost:8000')


@pytest.fixture(scope='session')
def excel_file(request, config):
    path = request.config.getoption("--excel-file") or config.get('test_data', 'excel_path', fallback='test_data/test_cases.xlsx')
    abs_path = os.path.abspath(path)
    if os.path.exists(abs_path):
        return abs_path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    return os.path.abspath(os.path.join(project_root, path))


@pytest.fixture(scope='session')
def sheet_name(request):
    return request.config.getoption("--sheet-name")


@pytest.fixture(scope='function')
def test_url(request, config):
    return request.config.getoption("--test-url") or config.get('application', 'base_url', fallback='http://localhost:3000')


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take screenshot on test failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            try:
                screenshots_dir = os.path.join(os.path.dirname(__file__), '..', 'reports', 'screenshots')
                os.makedirs(screenshots_dir, exist_ok=True)
                screenshot_name = f"FAIL_{item.name}"
                screenshot_path = os.path.join(screenshots_dir, f"{screenshot_name}.png")
                driver.save_screenshot(screenshot_path)
                logger.info(f"Failure screenshot saved: {screenshot_path}")
            except Exception as e:
                logger.error(f"Failed to take screenshot: {e}")
