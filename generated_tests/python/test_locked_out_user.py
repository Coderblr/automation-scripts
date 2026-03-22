"""
Auto-generated test script from Excel
Test Case: TC003 - Locked Out User
Generated: 2026-03-21 11:02:04
"""

import os
import sys
import pytest
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.base.base_page import BasePage


class Test_TC003:
    """Locked Out User"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.page = BasePage(driver)

    @pytest.mark.regression
    def test_locked_out_user(self):
        """Execute: Locked Out User"""
        page = self.page

        # Step 1: navigate
        page.navigate_to("https://www.saucedemo.com/v1/")

        # Step 2: type
        page.type_text("id", "user-name", "locked_out_user")

        # Step 3: type
        page.type_text("id", "password", "secret_sauce")

        # Step 4: click
        page.click("id", "login-button")

        # Step 5: wait
        page.wait_seconds(1)

        # Step 6: verify_element_visible
        assert page.is_element_visible("css", "h3[data-test="error"]"), "Element not visible: css=h3[data-test="error"]"

        # Step 7: verify_text
        page.verify_text("css", "h3[data-test="error"]", "locked out")

        # Step 8: take_screenshot
        page.take_screenshot("TC003_locked_out_error")

