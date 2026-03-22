import os
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class BasePage:
    """Base class for all page objects. Provides common Selenium operations."""

    LOCATOR_MAP = {
        'id': By.ID,
        'name': By.NAME,
        'xpath': By.XPATH,
        'css': By.CSS_SELECTOR,
        'class': By.CLASS_NAME,
        'tag': By.TAG_NAME,
        'link_text': By.LINK_TEXT,
        'partial_link_text': By.PARTIAL_LINK_TEXT,
    }

    def __init__(self, driver, wait_time=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_time)
        self.actions = ActionChains(driver)

    def _get_by(self, locator_type):
        by = self.LOCATOR_MAP.get(locator_type.lower())
        if not by:
            raise ValueError(f"Invalid locator type: '{locator_type}'. "
                             f"Supported: {list(self.LOCATOR_MAP.keys())}")
        return by

    # --- Element Finding ---

    def find_element(self, locator_type, locator_value):
        by = self._get_by(locator_type)
        return self.wait.until(EC.presence_of_element_located((by, locator_value)))

    def find_elements(self, locator_type, locator_value):
        by = self._get_by(locator_type)
        return self.driver.find_elements(by, locator_value)

    def find_clickable_element(self, locator_type, locator_value):
        by = self._get_by(locator_type)
        return self.wait.until(EC.element_to_be_clickable((by, locator_value)))

    def find_visible_element(self, locator_type, locator_value):
        by = self._get_by(locator_type)
        return self.wait.until(EC.visibility_of_element_located((by, locator_value)))

    # --- Actions ---

    def click(self, locator_type, locator_value):
        element = self.find_clickable_element(locator_type, locator_value)
        element.click()

    def type_text(self, locator_type, locator_value, text):
        element = self.find_visible_element(locator_type, locator_value)
        element.clear()
        element.send_keys(text)

    def clear_field(self, locator_type, locator_value):
        element = self.find_visible_element(locator_type, locator_value)
        element.clear()

    def select_dropdown(self, locator_type, locator_value, option_text):
        element = self.find_visible_element(locator_type, locator_value)
        select = Select(element)
        select.select_by_visible_text(option_text)

    def select_dropdown_by_value(self, locator_type, locator_value, value):
        element = self.find_visible_element(locator_type, locator_value)
        select = Select(element)
        select.select_by_value(value)

    def hover(self, locator_type, locator_value):
        element = self.find_visible_element(locator_type, locator_value)
        ActionChains(self.driver).move_to_element(element).perform()

    def double_click(self, locator_type, locator_value):
        element = self.find_clickable_element(locator_type, locator_value)
        ActionChains(self.driver).double_click(element).perform()

    def right_click(self, locator_type, locator_value):
        element = self.find_clickable_element(locator_type, locator_value)
        ActionChains(self.driver).context_click(element).perform()

    def press_key(self, key_name):
        key = getattr(Keys, key_name.upper(), None)
        if key:
            ActionChains(self.driver).send_keys(key).perform()
        else:
            raise ValueError(f"Unknown key: {key_name}")

    def scroll_to_element(self, locator_type, locator_value):
        element = self.find_element(locator_type, locator_value)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def scroll_page(self, direction="down", pixels=500):
        if direction.lower() == "down":
            self.driver.execute_script(f"window.scrollBy(0, {pixels});")
        elif direction.lower() == "up":
            self.driver.execute_script(f"window.scrollBy(0, -{pixels});")

    def upload_file(self, locator_type, locator_value, file_path):
        element = self.find_element(locator_type, locator_value)
        element.send_keys(os.path.abspath(file_path))

    # --- Navigation ---

    def navigate_to(self, url):
        self.driver.get(url)

    def refresh_page(self):
        self.driver.refresh()

    def go_back(self):
        self.driver.back()

    def go_forward(self):
        self.driver.forward()

    # --- Waits ---

    def wait_for_element_visible(self, locator_type, locator_value, timeout=20):
        by = self._get_by(locator_type)
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, locator_value))
        )

    def wait_for_element_invisible(self, locator_type, locator_value, timeout=20):
        by = self._get_by(locator_type)
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located((by, locator_value))
        )

    def wait_seconds(self, seconds):
        time.sleep(float(seconds))

    # --- Getters ---

    def get_text(self, locator_type, locator_value):
        element = self.find_visible_element(locator_type, locator_value)
        return element.text

    def get_attribute(self, locator_type, locator_value, attribute):
        element = self.find_element(locator_type, locator_value)
        return element.get_attribute(attribute)

    def get_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url

    # --- Verifications ---

    def is_element_present(self, locator_type, locator_value):
        try:
            self.find_element(locator_type, locator_value)
            return True
        except Exception:
            return False

    def is_element_visible(self, locator_type, locator_value):
        try:
            element = self.find_element(locator_type, locator_value)
            return element.is_displayed()
        except Exception:
            return False

    def is_element_enabled(self, locator_type, locator_value):
        try:
            element = self.find_element(locator_type, locator_value)
            return element.is_enabled()
        except Exception:
            return False

    def verify_text(self, locator_type, locator_value, expected_text):
        actual_text = self.get_text(locator_type, locator_value)
        assert expected_text in actual_text, (
            f"Text verification failed. Expected: '{expected_text}', Got: '{actual_text}'"
        )

    def verify_title(self, expected_title):
        actual_title = self.get_title()
        assert expected_title in actual_title, (
            f"Title verification failed. Expected: '{expected_title}', Got: '{actual_title}'"
        )

    def verify_url_contains(self, expected_text):
        actual_url = self.get_current_url()
        assert expected_text in actual_url, (
            f"URL verification failed. Expected '{expected_text}' in '{actual_url}'"
        )

    # --- Frames & Windows ---

    def switch_to_frame(self, locator_type=None, locator_value=None):
        if locator_type and locator_value:
            frame = self.find_element(locator_type, locator_value)
            self.driver.switch_to.frame(frame)
        else:
            self.driver.switch_to.default_content()

    def switch_to_window(self, index=1):
        handles = self.driver.window_handles
        if index < len(handles):
            self.driver.switch_to.window(handles[index])

    def close_current_window(self):
        self.driver.close()
        handles = self.driver.window_handles
        if handles:
            self.driver.switch_to.window(handles[0])

    # --- Alerts ---

    def accept_alert(self):
        self.wait.until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self):
        self.wait.until(EC.alert_is_present())
        self.driver.switch_to.alert.dismiss()

    def get_alert_text(self):
        self.wait.until(EC.alert_is_present())
        return self.driver.switch_to.alert.text

    # --- JavaScript ---

    def execute_js(self, script, *args):
        return self.driver.execute_script(script, *args)

    # --- Screenshots ---

    def take_screenshot(self, name=None):
        screenshots_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'screenshots')
        os.makedirs(screenshots_dir, exist_ok=True)
        filename = name or f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        filepath = os.path.join(screenshots_dir, f"{filename}.png")
        self.driver.save_screenshot(filepath)
        return filepath
