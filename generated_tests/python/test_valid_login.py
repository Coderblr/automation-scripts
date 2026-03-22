"""
Auto-generated test script from Excel
Test Case: TC001 - Valid Login
Generated: 2026-03-21 11:02:04
"""

import os
import sys
import pytest
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.base.base_page import BasePage


class Test_TC001:
    """Valid Login"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.page = BasePage(driver)

    @pytest.mark.regression
    def test_valid_login(self):
        """Execute: Valid Login"""
        page = self.page

        # Step 1: navigate
        page.navigate_to("https://www.saucedemo.com/v1/")

        # Step 2: verify_title
        page.verify_title("Swag Labs")

        # Step 3: type
        page.type_text("id", "user-name", "standard_user")

        # Step 4: type
        page.type_text("id", "password", "secret_sauce")

        # Step 5: click
        page.click("id", "login-button")

        # Step 6: wait
        page.wait_seconds(2)

        # Step 7: verify_url
        page.verify_url_contains("inventory.html")

        # Step 8: verify_element_visible
        assert page.is_element_visible("class", "inventory_list"), "Element not visible: class=inventory_list"

        # Step 9: take_screenshot
        page.take_screenshot("TC001_login_success")

