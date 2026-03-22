"""
Auto-generated test script from Excel
Test Case: TC005 - Add Product to Cart
Generated: 2026-03-21 11:02:04
"""

import os
import sys
import pytest
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.base.base_page import BasePage


class Test_TC005:
    """Add Product to Cart"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.page = BasePage(driver)

    @pytest.mark.regression
    def test_add_product_to_cart(self):
        """Execute: Add Product to Cart"""
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

        # Step 7: wait
        page.wait_seconds(1)

        # Step 8: verify_element_visible
        assert page.is_element_visible("css", ".shopping_cart_badge"), "Element not visible: css=.shopping_cart_badge"

        # Step 9: verify_text
        page.verify_text("css", ".shopping_cart_badge", "1")

        # Step 10: click
        page.click("css", ".shopping_cart_link")

        # Step 11: wait
        page.wait_seconds(1)

        # Step 12: verify_url
        page.verify_url_contains("cart.html")

        # Step 13: verify_element_visible
        assert page.is_element_visible("css", ".cart_item"), "Element not visible: css=.cart_item"

        # Step 14: take_screenshot
        page.take_screenshot("TC005_product_in_cart")

