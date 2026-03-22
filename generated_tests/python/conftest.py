"""Auto-generated conftest.py for generated test scripts."""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.base.driver_factory import DriverFactory


@pytest.fixture(scope='function')
def driver():
    driver = DriverFactory.get_driver()
    yield driver
    driver.quit()
