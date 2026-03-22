"""
Auto-generated test script from Excel
Test Case: TC004 - Product Page Verification
Generated: 2026-03-21 11:02:04
"""

import os
import sys
import pytest
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.base.base_page import BasePage


class Test_TC004:
    """Product Page Verification"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.page = BasePage(driver)

    @pytest.mark.regression
    def test_product_page_verification(self):
        """Execute: Product Page Verification"""
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

        # Step 6: verify_text
        page.verify_text("class", "product_label", "Products")

        # Step 7: verify_element_visible
        assert page.is_element_visible("class", "inventory_list"), "Element not visible: class=inventory_list"

        # Step 8: verify_element_visible
        assert page.is_element_visible("class", "product_sort_container"), "Element not visible: class=product_sort_container"

        # Step 9: verify_element_visible
        assert page.is_element_visible("css", ".shopping_cart_link"), "Element not visible: css=.shopping_cart_link"

        # Step 10: take_screenshot
        page.take_screenshot("TC004_products_page")

