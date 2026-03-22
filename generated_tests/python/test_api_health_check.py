"""
Auto-generated test script from Excel
Test Case: TC003 - API Health Check
Generated: 2026-03-21 10:29:21
"""

import os
import sys
import pytest
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.base.base_page import BasePage


class Test_TC003:
    """API Health Check"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.page = BasePage(driver)

    @pytest.mark.regression
    def test_api_health_check(self):
        """Execute: API Health Check"""
        page = self.page

        # Step 1: api_get
        response = requests.get("http://localhost:8000/api/health", timeout=30)

        # Step 2: verify_api_status
        assert response.status_code == 200

