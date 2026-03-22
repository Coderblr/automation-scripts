"""
Auto-generated test script from Excel
Test Case: TC002 - Homepage Verification
Generated: 2026-03-21 10:29:21
"""

import os
import sys
import pytest
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.base.base_page import BasePage


class Test_TC002:
    """Homepage Verification"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.page = BasePage(driver)

    @pytest.mark.regression
    def test_homepage_verification(self):
        """Execute: Homepage Verification"""
        page = self.page

        # Step 1: navigate
        page.navigate_to("http://localhost:3000")

        # Step 2: verify_title
        page.verify_title("Home")

        # Step 3: verify_element_present
        assert page.is_element_present("xpath", "//nav"), "Element not found: xpath=//nav"

        # Step 4: verify_element_visible
        assert page.is_element_visible("css", "header"), "Element not visible: css=header"

        # Step 5: take_screenshot
        page.take_screenshot("homepage")

