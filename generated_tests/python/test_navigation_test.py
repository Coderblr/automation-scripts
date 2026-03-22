"""
Auto-generated test script from Excel
Test Case: TC005 - Navigation Test
Generated: 2026-03-21 10:29:21
"""

import os
import sys
import pytest
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.base.base_page import BasePage


class Test_TC005:
    """Navigation Test"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.page = BasePage(driver)

    @pytest.mark.regression
    def test_navigation_test(self):
        """Execute: Navigation Test"""
        page = self.page

        # Step 1: navigate
        page.navigate_to("http://localhost:3000")

        # Step 2: click
        page.click("link_text", "About")

        # Step 3: verify_url
        page.verify_url_contains("/about")

        # Step 4: go_back
        page.go_back()

        # Step 5: verify_url
        page.verify_url_contains("localhost:3000")

