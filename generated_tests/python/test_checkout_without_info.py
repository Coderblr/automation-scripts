"""
Auto-generated test script from Excel
Test Case: TC012 - Checkout Without Info
Generated: 2026-03-21 11:02:04
"""

import os
import sys
import pytest
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.base.base_page import BasePage


class Test_TC012:
    """Checkout Without Info"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.page = BasePage(driver)

    @pytest.mark.regression
    def test_checkout_without_info(self):
        """Execute: Checkout Without Info"""
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

        # Step 6: click
        page.click("css", ".inventory_item:nth-child(1) .btn_inventory")

        # Step 7: click
        page.click("css", ".shopping_cart_link")

        # Step 8: wait
        page.wait_seconds(1)

        # Step 9: click
        page.click("css", ".checkout_button")

        # Step 10: wait
        page.wait_seconds(1)

        # Step 11: click
        page.click("css", ".cart_button")

        # Step 12: wait
        page.wait_seconds(1)

        # Step 13: verify_element_visible
        assert page.is_element_visible("css", "h3[data-test="error"]"), "Element not visible: css=h3[data-test="error"]"

        # Step 14: verify_text
        page.verify_text("css", "h3[data-test="error"]", "First Name is required")

        # Step 15: take_screenshot
        page.take_screenshot("TC012_checkout_error")

