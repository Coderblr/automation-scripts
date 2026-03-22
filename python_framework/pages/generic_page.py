"""
Generic Page Object for dynamic/keyword-driven testing.
Extends BasePage with higher-level operations for common web app patterns.
"""

from python_framework.base.base_page import BasePage


class GenericPage(BasePage):
    """Provides high-level page operations for any web application."""

    def login(self, username_locator, password_locator, submit_locator,
              username, password, locator_type='id'):
        self.type_text(locator_type, username_locator, username)
        self.type_text(locator_type, password_locator, password)
        self.click(locator_type, submit_locator)

    def fill_form(self, field_data, locator_type='id'):
        """
        Fill a form with multiple fields.
        field_data: dict of {locator_value: text_to_type}
        """
        for locator_value, text in field_data.items():
            self.type_text(locator_type, locator_value, text)

    def get_table_data(self, table_locator_type='xpath', table_locator_value='//table'):
        """Extract all data from an HTML table as a list of lists."""
        table = self.find_element(table_locator_type, table_locator_value)
        rows = table.find_elements('tag name', 'tr')
        data = []
        for row in rows:
            cells = row.find_elements('tag name', 'td')
            if not cells:
                cells = row.find_elements('tag name', 'th')
            data.append([cell.text for cell in cells])
        return data

    def get_all_links(self):
        """Get all links on the current page."""
        links = self.find_elements('tag', 'a')
        return [(link.text, link.get_attribute('href')) for link in links]

    def check_broken_links(self):
        """Check all links on the page and return broken ones."""
        import requests
        links = self.get_all_links()
        broken = []
        for text, href in links:
            if not href or href.startswith(('javascript:', 'mailto:', '#')):
                continue
            try:
                response = requests.head(href, timeout=10, allow_redirects=True)
                if response.status_code >= 400:
                    broken.append({'text': text, 'url': href, 'status': response.status_code})
            except requests.RequestException as e:
                broken.append({'text': text, 'url': href, 'error': str(e)})
        return broken

    def get_page_load_time(self):
        """Get page load time using Navigation Timing API."""
        script = """
        var timing = window.performance.timing;
        return timing.loadEventEnd - timing.navigationStart;
        """
        return self.execute_js(script)

    def check_console_errors(self):
        """Get browser console errors (Chrome only)."""
        logs = self.driver.get_log('browser')
        return [log for log in logs if log['level'] == 'SEVERE']

    def get_page_title_and_meta(self):
        """Get page title and meta description."""
        title = self.get_title()
        meta_desc = self.execute_js(
            "var meta = document.querySelector('meta[name=\"description\"]'); "
            "return meta ? meta.content : '';"
        )
        return {'title': title, 'meta_description': meta_desc}
