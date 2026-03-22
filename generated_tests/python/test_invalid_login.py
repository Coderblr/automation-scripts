"""
Auto-generated test script from Excel
Test Case: TC002 - Invalid Login
Generated: 2026-03-21 11:02:04
"""

import os
import sys
import pytest
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.base.base_page import BasePage


class Test_TC002:
    """Invalid Login"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.page = BasePage(driver)

    @pytest.mark.regression
    def test_invalid_login(self):
        """Execute: Invalid Login"""
        page = self.page

        # Step 1: navigate
        page.navigate_to("https://www.saucedemo.com/v1/")

        # Step 2: type
        page.type_text("id", "user-name", "invalid_user")

        # Step 3: type
        page.type_text("id", "password", "wrong_password")

        # Step 4: click
        page.click("id", "login-button")

        # Step 5: wait
        page.wait_seconds(1)

        # Step 6: verify_element_visible
        assert page.is_element_visible("css", "h3[data-test="error"]"), "Element not visible: css=h3[data-test="error"]"

        # Step 7: verify_text
        page.verify_text("css", "h3[data-test="error"]", "do not match")

        # Step 8: take_screenshot
        page.take_screenshot("TC002_invalid_login_error")

