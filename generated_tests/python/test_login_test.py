"""
Auto-generated test script from Excel
Test Case: TC001 - Login Test
Generated: 2026-03-21 10:29:21
"""

import os
import sys
import pytest
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.base.base_page import BasePage


class Test_TC001:
    """Login Test"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.page = BasePage(driver)

    @pytest.mark.regression
    def test_login_test(self):
        """Execute: Login Test"""
        page = self.page

        # Step 1: navigate
        page.navigate_to("http://localhost:3000/login")

        # Step 2: type
        page.type_text("id", "username", "testuser")

        # Step 3: type
        page.type_text("id", "password", "testpass123")

        # Step 4: click
        page.click("id", "login-btn")

        # Step 5: wait
        page.wait_seconds(2)

        # Step 6: verify_url
        page.verify_url_contains("/dashboard")

        # Step 7: take_screenshot
        page.take_screenshot("login_success")

