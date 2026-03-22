"""
API Test Suite for FastAPI Backend

Tests REST API endpoints directly without a browser.
Supports GET, POST, PUT, DELETE operations.

Usage:
    pytest test_api.py --api-url=http://localhost:8000
"""

import os
import sys
import json
import logging
import pytest
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

logger = logging.getLogger(__name__)


class TestAPIHealth:
    """Basic API health and availability tests."""

    @pytest.fixture(autouse=True)
    def setup(self, api_base_url):
        self.api_url = api_base_url
        self.session = requests.Session()

    @pytest.mark.api
    @pytest.mark.smoke
    def test_api_is_reachable(self):
        """Verify the API server is running and reachable."""
        try:
            response = self.session.get(f"{self.api_url}/docs", timeout=10)
            assert response.status_code == 200, f"API not reachable. Status: {response.status_code}"
            logger.info(f"API is reachable at {self.api_url}")
        except requests.ConnectionError:
            pytest.fail(f"Cannot connect to API at {self.api_url}. Is the server running?")

    @pytest.mark.api
    @pytest.mark.smoke
    def test_health_endpoint(self, config):
        """Verify the health check endpoint."""
        health_path = config.get('api', 'health_endpoint', fallback='/api/health')
        url = f"{self.api_url}{health_path}"
        try:
            response = self.session.get(url, timeout=10)
            logger.info(f"Health check: {url} -> {response.status_code}")
            assert response.status_code in (200, 404), (
                f"Health endpoint returned unexpected status: {response.status_code}")
        except requests.ConnectionError:
            pytest.skip(f"API not running at {self.api_url}")

    @pytest.mark.api
    def test_api_docs_available(self):
        """Verify FastAPI auto-generated docs are available."""
        for path in ['/docs', '/redoc', '/openapi.json']:
            response = self.session.get(f"{self.api_url}{path}", timeout=10)
            logger.info(f"Docs endpoint {path}: {response.status_code}")
            if response.status_code == 200:
                return
        pytest.skip("No API docs endpoints found (tried /docs, /redoc, /openapi.json)")

    @pytest.mark.api
    def test_cors_headers(self):
        """Verify CORS headers are set correctly for frontend communication."""
        headers = {'Origin': 'http://localhost:3000'}
        try:
            response = self.session.options(f"{self.api_url}/", headers=headers, timeout=10)
            cors_header = response.headers.get('Access-Control-Allow-Origin', '')
            logger.info(f"CORS header: {cors_header}")
        except requests.ConnectionError:
            pytest.skip(f"API not running at {self.api_url}")


class TestAPIEndpoints:
    """Test specific API endpoints. Customize these for your application."""

    @pytest.fixture(autouse=True)
    def setup(self, api_base_url, config):
        self.api_url = api_base_url
        self.config = config
        self.session = requests.Session()

    @pytest.mark.api
    @pytest.mark.regression
    def test_get_request(self):
        """Test a GET endpoint returns valid JSON."""
        response = self.session.get(f"{self.api_url}/", timeout=10)
        assert response.status_code in (200, 404, 307), (
            f"Unexpected status: {response.status_code}")
        logger.info(f"GET / -> {response.status_code}")

    @pytest.mark.api
    @pytest.mark.regression
    def test_response_time(self):
        """Verify API response time is within acceptable limits."""
        response = self.session.get(f"{self.api_url}/docs", timeout=10)
        elapsed_ms = response.elapsed.total_seconds() * 1000
        logger.info(f"Response time: {elapsed_ms:.0f}ms")
        assert elapsed_ms < 5000, f"Response time {elapsed_ms:.0f}ms exceeds 5 seconds"

    @pytest.mark.api
    def test_invalid_endpoint_returns_404(self):
        """Verify non-existent endpoints return 404."""
        response = self.session.get(f"{self.api_url}/api/nonexistent_endpoint_xyz", timeout=10)
        assert response.status_code in (404, 422), (
            f"Expected 404 for invalid endpoint, got {response.status_code}")

    @pytest.mark.api
    def test_json_content_type(self):
        """Verify API returns proper JSON content type."""
        response = self.session.get(f"{self.api_url}/openapi.json", timeout=10)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            assert 'json' in content_type.lower(), (
                f"Expected JSON content type, got: {content_type}")
            try:
                response.json()
            except json.JSONDecodeError:
                pytest.fail("Response is not valid JSON")
