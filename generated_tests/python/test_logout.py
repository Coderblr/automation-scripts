"""
Auto-generated test script from Excel
Test Case: TC009 - Logout
Generated: 2026-03-21 11:02:04
"""

import os
import sys
import pytest
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.base.base_page import BasePage


class Test_TC009:
    """Logout"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.page = BasePage(driver)

    @pytest.mark.regression
    def test_logout(self):
        """Execute: Logout"""
        page = self.page

        # Step 1: navigate
        page.navigate_to("https://www.saucedemo.com/v1/")

        # Step 2: type
        page.type_text("id", "user-name", "standard_user")

        # Step 3: type
        page.type_text("id", "password", "secret_sauce")

        # Step 4: click
        page.click("id", "login-button")

        # Step 5: wait
        page.wait_seconds(2)

        # Step 6: verify_url
        page.verify_url_contains("inventory.html")

        # Step 7: click
        page.click("css", ".bm-burger-button button")

        # Step 8: wait
        page.wait_seconds(1)

        # Step 9: click
        page.click("id", "logout_sidebar_link")

        # Step 10: wait
        page.wait_seconds(2)

        # Step 11: verify_element_visible
        assert page.is_element_visible("id", "login-button"), "Element not visible: id=login-button"

        # Step 12: take_screenshot
        page.take_screenshot("TC009_logout_success")

