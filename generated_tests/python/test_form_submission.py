"""
Auto-generated test script from Excel
Test Case: TC004 - Form Submission
Generated: 2026-03-21 10:29:21
"""

import os
import sys
import pytest
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.base.base_page import BasePage


class Test_TC004:
    """Form Submission"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.page = BasePage(driver)

    @pytest.mark.regression
    def test_form_submission(self):
        """Execute: Form Submission"""
        page = self.page

        # Step 1: navigate
        page.navigate_to("http://localhost:3000/contact")

        # Step 2: type
        page.type_text("name", "name", "John Doe")

        # Step 3: type
        page.type_text("name", "email", "john@example.com")

        # Step 4: type
        page.type_text("name", "message", "Test message")

        # Step 5: click
        page.click("xpath", "//button[@type="submit"]")

        # Step 6: wait
        page.wait_seconds(2)

        # Step 7: verify_text
        page.verify_text("css", ".success-message", "submitted")

