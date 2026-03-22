"""
Auto-generated test script from Excel
Test Case: TC007 - Complete Checkout Flow
Generated: 2026-03-21 11:02:04
"""

import os
import sys
import pytest
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.base.base_page import BasePage


class Test_TC007:
    """Complete Checkout Flow"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.page = BasePage(driver)

    @pytest.mark.regression
    def test_complete_checkout_flow(self):
        """Execute: Complete Checkout Flow"""
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

        # Step 9: verify_url
        page.verify_url_contains("cart.html")

        # Step 10: verify_element_visible
        assert page.is_element_visible("css", ".cart_item"), "Element not visible: css=.cart_item"

        # Step 11: click
        page.click("css", ".checkout_button")

        # Step 12: wait
        page.wait_seconds(1)

        # Step 13: verify_url
        page.verify_url_contains("checkout-step-one.html")

        # Step 14: type
        page.type_text("id", "first-name", "John")

        # Step 15: type
        page.type_text("id", "last-name", "Doe")

        # Step 16: type
        page.type_text("id", "postal-code", "12345")

        # Step 17: click
        page.click("css", ".cart_button")

        # Step 18: wait
        page.wait_seconds(1)

        # Step 19: verify_url
        page.verify_url_contains("checkout-step-two.html")

        # Step 20: verify_element_visible
        assert page.is_element_visible("class", "summary_info"), "Element not visible: class=summary_info"

        # Step 21: take_screenshot
        page.take_screenshot("TC007_checkout_summary")

        # Step 22: click
        page.click("css", ".cart_button")

        # Step 23: wait
        page.wait_seconds(1)

        # Step 24: verify_url
        page.verify_url_contains("checkout-complete.html")

        # Step 25: verify_text
        page.verify_text("class", "complete-header", "THANK YOU")

        # Step 26: take_screenshot
        page.take_screenshot("TC007_order_complete")

