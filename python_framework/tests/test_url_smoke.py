"""
URL Smoke Test

Provides quick smoke testing for any given URL.
Checks: page loads, title exists, no console errors, broken links, performance.

Usage:
    pytest test_url_smoke.py --test-url=http://localhost:3000
    pytest test_url_smoke.py --test-url=https://example.com --headless
"""

import os
import sys
import logging
import requests
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.pages.generic_page import GenericPage

logger = logging.getLogger(__name__)


class TestURLSmoke:
    """Smoke tests for a given URL - validates basic page health."""

    @pytest.fixture(autouse=True)
    def setup(self, driver, test_url):
        self.driver = driver
        self.test_url = test_url
        self.page = GenericPage(driver)

    @pytest.mark.smoke
    def test_page_loads(self):
        """Verify the page loads without errors."""
        logger.info(f"Testing URL: {self.test_url}")
        self.page.navigate_to(self.test_url)
        assert self.driver.title or self.driver.page_source, "Page failed to load"
        logger.info(f"Page loaded. Title: '{self.driver.title}'")

    @pytest.mark.smoke
    def test_page_title_exists(self):
        """Verify the page has a title."""
        self.page.navigate_to(self.test_url)
        title = self.driver.title
        assert title and len(title.strip()) > 0, "Page title is empty"
        logger.info(f"Page title: '{title}'")

    @pytest.mark.smoke
    def test_http_status(self):
        """Verify the URL returns HTTP 200."""
        response = requests.get(self.test_url, timeout=30)
        assert response.status_code == 200, (
            f"Expected status 200, got {response.status_code}")
        logger.info(f"HTTP status: {response.status_code}")

    @pytest.mark.smoke
    def test_page_has_content(self):
        """Verify the page body is not empty."""
        self.page.navigate_to(self.test_url)
        body_text = self.driver.find_element('tag name', 'body').text
        assert len(body_text.strip()) > 0, "Page body is empty"
        logger.info(f"Page has {len(body_text)} characters of content")

    @pytest.mark.smoke
    def test_no_broken_images(self):
        """Check for broken images on the page."""
        self.page.navigate_to(self.test_url)
        broken_images = self.page.execute_js("""
            var images = document.querySelectorAll('img');
            var broken = [];
            images.forEach(function(img) {
                if (!img.complete || img.naturalHeight === 0) {
                    broken.push(img.src);
                }
            });
            return broken;
        """)
        if broken_images:
            logger.warning(f"Broken images found: {broken_images}")
        assert len(broken_images) == 0, f"Found {len(broken_images)} broken images: {broken_images}"

    @pytest.mark.smoke
    def test_page_load_performance(self):
        """Check that page loads within acceptable time (< 10 seconds)."""
        self.page.navigate_to(self.test_url)
        load_time = self.page.get_page_load_time()
        logger.info(f"Page load time: {load_time}ms")
        assert load_time < 10000, f"Page load time {load_time}ms exceeds 10 seconds"

    @pytest.mark.smoke
    def test_responsive_viewport(self):
        """Verify page renders at different viewport sizes."""
        viewports = [
            (1920, 1080, 'Desktop'),
            (768, 1024, 'Tablet'),
            (375, 812, 'Mobile'),
        ]
        self.page.navigate_to(self.test_url)
        for width, height, name in viewports:
            self.driver.set_window_size(width, height)
            self.page.wait_seconds(1)
            body = self.driver.find_element('tag name', 'body')
            assert body.is_displayed(), f"Body not visible at {name} ({width}x{height})"
            logger.info(f"Viewport {name} ({width}x{height}): OK")

        self.driver.maximize_window()

    @pytest.mark.smoke
    def test_take_screenshot(self):
        """Capture a screenshot of the page for visual verification."""
        self.page.navigate_to(self.test_url)
        path = self.page.take_screenshot('smoke_test_screenshot')
        assert os.path.exists(path), "Screenshot was not saved"
        logger.info(f"Screenshot saved: {path}")


class TestBrokenLinks:
    """Check for broken links on the target URL."""

    @pytest.fixture(autouse=True)
    def setup(self, driver, test_url):
        self.driver = driver
        self.test_url = test_url
        self.page = GenericPage(driver)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_no_broken_links(self):
        """Verify all links on the page return valid HTTP responses."""
        self.page.navigate_to(self.test_url)
        broken = self.page.check_broken_links()

        if broken:
            for link in broken:
                logger.error(f"Broken link: {link}")

        assert len(broken) == 0, (
            f"Found {len(broken)} broken link(s):\n" +
            "\n".join(f"  - {b.get('url', 'unknown')}: {b.get('status', b.get('error', 'unknown'))}"
                      for b in broken)
        )
