"""
Auto-generated test script from Excel
Test Case: TC008 - Product Sorting
Generated: 2026-03-21 11:02:04
"""

import os
import sys
import pytest
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.base.base_page import BasePage


class Test_TC008:
    """Product Sorting"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.page = BasePage(driver)

    @pytest.mark.regression
    def test_product_sorting(self):
        """Execute: Product Sorting"""
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

        # Step 6: select_dropdown
        page.select_dropdown("class", "product_sort_container", "Price (low to high)")

        # Step 7: wait
        page.wait_seconds(1)

        # Step 8: take_screenshot
        page.take_screenshot("TC008_sort_price_low_high")

        # Step 9: select_dropdown
        page.select_dropdown("class", "product_sort_container", "Price (high to low)")

        # Step 10: wait
        page.wait_seconds(1)

        # Step 11: take_screenshot
        page.take_screenshot("TC008_sort_price_high_low")

        # Step 12: select_dropdown
        page.select_dropdown("class", "product_sort_container", "Name (Z to A)")

        # Step 13: wait
        page.wait_seconds(1)

        # Step 14: take_screenshot
        page.take_screenshot("TC008_sort_name_z_to_a")

