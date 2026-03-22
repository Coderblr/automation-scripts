"""
Keyword-Driven Test Engine

Maps action keywords from Excel test cases to Selenium operations.
Testers define tests using keywords like 'click', 'type', 'verify_text', etc.

Supports variables in Excel using ${variable_name} syntax:
  ${base_url}    → base URL from config.ini
  ${username}    → test_username from config.ini
  ${password}    → test_password from config.ini
  ${api_url}     → api_base_url from config.ini
"""

import os
import logging
import configparser
import requests
from python_framework.base.base_page import BasePage

logger = logging.getLogger(__name__)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.ini')


def _load_config_variables():
    """Load variables from config.ini so Excel can use ${base_url}, ${username}, etc."""
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    variables = {
        'base_url': config.get('application', 'base_url', fallback='http://localhost:3000'),
        'api_url': config.get('application', 'api_base_url', fallback='http://localhost:8000'),
        'username': config.get('credentials', 'test_username', fallback=''),
        'password': config.get('credentials', 'test_password', fallback=''),
        'browser': config.get('browser', 'browser_name', fallback='chrome'),
    }
    return variables


class KeywordEngine:
    """Executes test steps based on action keywords from Excel test cases."""

    def __init__(self, driver):
        self.driver = driver
        self.page = BasePage(driver)
        self.variables = _load_config_variables()
        logger.info(f"Config variables loaded: base_url={self.variables.get('base_url')}")

    def execute_step(self, action, locator_type=None, locator_value=None,
                     test_data=None, expected_result=None):
        """Execute a single test step based on the action keyword."""
        action = str(action).strip().lower()
        locator_type = str(locator_type).strip().lower() if locator_type else None
        locator_value = str(locator_value).strip() if locator_value else None
        test_data = str(test_data).strip() if test_data else None
        expected_result = str(expected_result).strip() if expected_result else None

        # Replace ${variable} placeholders with values from config + stored vars
        locator_value = self._resolve_variables(locator_value)
        test_data = self._resolve_variables(test_data)
        expected_result = self._resolve_variables(expected_result)

        logger.info(f"Executing: {action} | Locator: {locator_type}={locator_value} | "
                    f"Data: {test_data} | Expected: {expected_result}")

        action_map = {
            'open_browser': self._open_browser,
            'navigate': self._navigate,
            'go_to_url': self._navigate,
            'open_url': self._navigate,
            'click': self._click,
            'type': self._type,
            'send_keys': self._type,
            'enter_text': self._type,
            'clear': self._clear,
            'select_dropdown': self._select_dropdown,
            'select': self._select_dropdown,
            'verify_text': self._verify_text,
            'assert_text': self._verify_text,
            'verify_title': self._verify_title,
            'assert_title': self._verify_title,
            'verify_url': self._verify_url,
            'verify_element_present': self._verify_element_present,
            'verify_element_visible': self._verify_element_visible,
            'hover': self._hover,
            'mouse_over': self._hover,
            'double_click': self._double_click,
            'right_click': self._right_click,
            'scroll_down': self._scroll_down,
            'scroll_up': self._scroll_up,
            'scroll_to_element': self._scroll_to_element,
            'wait': self._wait,
            'sleep': self._wait,
            'press_key': self._press_key,
            'switch_frame': self._switch_frame,
            'switch_default': self._switch_default,
            'switch_window': self._switch_window,
            'accept_alert': self._accept_alert,
            'dismiss_alert': self._dismiss_alert,
            'take_screenshot': self._take_screenshot,
            'screenshot': self._take_screenshot,
            'refresh': self._refresh,
            'go_back': self._go_back,
            'upload_file': self._upload_file,
            'store_text': self._store_text,
            'store_attribute': self._store_attribute,
            'execute_js': self._execute_js,
            'close_browser': self._close_browser,
            'close_window': self._close_window,
            'api_get': self._api_get,
            'api_post': self._api_post,
            'verify_api_status': self._verify_api_status,
        }

        handler = action_map.get(action)
        if not handler:
            raise ValueError(f"Unknown action keyword: '{action}'. "
                             f"Supported actions: {sorted(action_map.keys())}")

        return handler(locator_type, locator_value, test_data, expected_result)

    def _resolve_variables(self, text):
        if not text:
            return text
        for var_name, var_value in self.variables.items():
            text = text.replace(f"${{{var_name}}}", str(var_value))
        return text

    # --- Browser Actions ---

    def _open_browser(self, *args):
        pass  # Browser is already opened by the driver factory

    def _navigate(self, lt, lv, test_data, expected):
        url = test_data or lv
        if url:
            self.page.navigate_to(url)

    def _close_browser(self, *args):
        self.driver.quit()

    def _close_window(self, *args):
        self.page.close_current_window()

    def _refresh(self, *args):
        self.page.refresh_page()

    def _go_back(self, *args):
        self.page.go_back()

    # --- Element Actions ---

    def _click(self, lt, lv, test_data, expected):
        self.page.click(lt, lv)

    def _type(self, lt, lv, test_data, expected):
        self.page.type_text(lt, lv, test_data or '')

    def _clear(self, lt, lv, test_data, expected):
        self.page.clear_field(lt, lv)

    def _select_dropdown(self, lt, lv, test_data, expected):
        self.page.select_dropdown(lt, lv, test_data)

    def _hover(self, lt, lv, test_data, expected):
        self.page.hover(lt, lv)

    def _double_click(self, lt, lv, test_data, expected):
        self.page.double_click(lt, lv)

    def _right_click(self, lt, lv, test_data, expected):
        self.page.right_click(lt, lv)

    def _press_key(self, lt, lv, test_data, expected):
        self.page.press_key(test_data or lv)

    def _upload_file(self, lt, lv, test_data, expected):
        self.page.upload_file(lt, lv, test_data)

    # --- Scroll ---

    def _scroll_down(self, lt, lv, test_data, expected):
        pixels = int(test_data) if test_data else 500
        self.page.scroll_page("down", pixels)

    def _scroll_up(self, lt, lv, test_data, expected):
        pixels = int(test_data) if test_data else 500
        self.page.scroll_page("up", pixels)

    def _scroll_to_element(self, lt, lv, test_data, expected):
        self.page.scroll_to_element(lt, lv)

    # --- Waits ---

    def _wait(self, lt, lv, test_data, expected):
        seconds = float(test_data or lv or 2)
        self.page.wait_seconds(seconds)

    # --- Verification ---

    def _verify_text(self, lt, lv, test_data, expected):
        expected_text = expected or test_data
        self.page.verify_text(lt, lv, expected_text)

    def _verify_title(self, lt, lv, test_data, expected):
        expected_title = expected or test_data
        self.page.verify_title(expected_title)

    def _verify_url(self, lt, lv, test_data, expected):
        expected_url = expected or test_data
        self.page.verify_url_contains(expected_url)

    def _verify_element_present(self, lt, lv, test_data, expected):
        assert self.page.is_element_present(lt, lv), (
            f"Element not present: {lt}={lv}")

    def _verify_element_visible(self, lt, lv, test_data, expected):
        assert self.page.is_element_visible(lt, lv), (
            f"Element not visible: {lt}={lv}")

    # --- Frames & Windows ---

    def _switch_frame(self, lt, lv, test_data, expected):
        self.page.switch_to_frame(lt, lv)

    def _switch_default(self, *args):
        self.page.switch_to_frame()

    def _switch_window(self, lt, lv, test_data, expected):
        index = int(test_data or lv or 1)
        self.page.switch_to_window(index)

    # --- Alerts ---

    def _accept_alert(self, *args):
        self.page.accept_alert()

    def _dismiss_alert(self, *args):
        self.page.dismiss_alert()

    # --- Screenshot ---

    def _take_screenshot(self, lt, lv, test_data, expected):
        name = test_data or lv or None
        return self.page.take_screenshot(name)

    # --- Variable Storage ---

    def _store_text(self, lt, lv, test_data, expected):
        text = self.page.get_text(lt, lv)
        var_name = test_data or 'stored_text'
        self.variables[var_name] = text
        logger.info(f"Stored text '{text}' in variable '{var_name}'")

    def _store_attribute(self, lt, lv, test_data, expected):
        parts = (test_data or '').split('|')
        attribute = parts[0] if parts else 'value'
        var_name = parts[1] if len(parts) > 1 else 'stored_attr'
        value = self.page.get_attribute(lt, lv, attribute)
        self.variables[var_name] = value
        logger.info(f"Stored attribute '{attribute}'='{value}' in variable '{var_name}'")

    # --- JavaScript ---

    def _execute_js(self, lt, lv, test_data, expected):
        script = test_data or lv
        return self.page.execute_js(script)

    # --- API Testing ---

    def _api_get(self, lt, lv, test_data, expected):
        url = test_data or lv
        response = requests.get(url, timeout=30)
        self.variables['api_response'] = response
        self.variables['api_status_code'] = response.status_code
        self.variables['api_body'] = response.text
        logger.info(f"API GET {url} -> Status: {response.status_code}")
        return response

    def _api_post(self, lt, lv, test_data, expected):
        import json
        url = lv
        try:
            body = json.loads(test_data) if test_data else {}
        except json.JSONDecodeError:
            body = {"data": test_data}
        response = requests.post(url, json=body, timeout=30)
        self.variables['api_response'] = response
        self.variables['api_status_code'] = response.status_code
        self.variables['api_body'] = response.text
        logger.info(f"API POST {url} -> Status: {response.status_code}")
        return response

    def _verify_api_status(self, lt, lv, test_data, expected):
        expected_code = int(expected or test_data or 200)
        actual_code = self.variables.get('api_status_code')
        assert actual_code == expected_code, (
            f"API status code mismatch. Expected: {expected_code}, Got: {actual_code}")
