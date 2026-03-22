"""
Auto-generated test script from Excel
Test Case: TC011 - Product Details Navigation
Generated: 2026-03-21 11:02:04
"""

import os
import sys
import pytest
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.base.base_page import BasePage


class Test_TC011:
    """Product Details Navigation"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.page = BasePage(driver)

    @pytest.mark.regression
    def test_product_details_navigation(self):
        """Execute: Product Details Navigation"""
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
        page.click("css", ".inventory_item:nth-child(1) .inventory_item_name")

        # Step 7: wait
        page.wait_seconds(1)

        # Step 8: verify_url
        page.verify_url_contains("inventory-item.html")

        # Step 9: verify_element_visible
        assert page.is_element_visible("class", "inventory_details_name"), "Element not visible: class=inventory_details_name"

        # Step 10: verify_element_visible
        assert page.is_element_visible("class", "inventory_details_price"), "Element not visible: class=inventory_details_price"

        # Step 11: verify_element_visible
        assert page.is_element_visible("class", "inventory_details_desc"), "Element not visible: class=inventory_details_desc"

        # Step 12: take_screenshot
        page.take_screenshot("TC011_product_details")

        # Step 13: click
        page.click("css", ".inventory_details_back_button")

        # Step 14: wait
        page.wait_seconds(1)

        # Step 15: verify_url
        page.verify_url_contains("inventory.html")

