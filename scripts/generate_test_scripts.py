"""
Test Script Generator

Reads test cases from Excel and generates standalone test scripts in:
  - Python + Selenium (pytest)
  - Java + Selenium (TestNG)

This eliminates manual effort — testers define tests in Excel,
and this tool generates production-ready test code.

Usage:
    python generate_test_scripts.py --excel path/to/tests.xlsx --language python
    python generate_test_scripts.py --excel path/to/tests.xlsx --language java
    python generate_test_scripts.py --excel path/to/tests.xlsx --language both
"""

import os
import sys
import argparse
import re
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from python_framework.utils.excel_handler import ExcelHandler


def sanitize_name(name):
    """Convert a test case name into a valid function/method name."""
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', str(name))
    sanitized = re.sub(r'_+', '_', sanitized).strip('_').lower()
    if sanitized and sanitized[0].isdigit():
        sanitized = f"tc_{sanitized}"
    return sanitized or 'unnamed_test'


def generate_step_code_python(step, indent='        '):
    """Generate Python code for a single test step."""
    action = str(step.get('Action', '')).strip().lower()
    lt = step.get('Locator_Type', '') or ''
    lv = step.get('Locator_Value', '') or ''
    td = step.get('Test_Data', '') or ''
    er = step.get('Expected_Result', '') or ''

    lt_str = f'"{lt}"' if lt else 'None'
    lv_str = f'"{lv}"' if lv else 'None'

    lines = []

    if action in ('navigate', 'go_to_url', 'open_url'):
        url = td or lv
        lines.append(f'{indent}page.navigate_to("{url}")')
    elif action in ('click',):
        lines.append(f'{indent}page.click({lt_str}, "{lv}")')
    elif action in ('type', 'send_keys', 'enter_text'):
        lines.append(f'{indent}page.type_text({lt_str}, "{lv}", "{td}")')
    elif action == 'clear':
        lines.append(f'{indent}page.clear_field({lt_str}, "{lv}")')
    elif action in ('select_dropdown', 'select'):
        lines.append(f'{indent}page.select_dropdown({lt_str}, "{lv}", "{td}")')
    elif action in ('verify_text', 'assert_text'):
        expected = er or td
        lines.append(f'{indent}page.verify_text({lt_str}, "{lv}", "{expected}")')
    elif action in ('verify_title', 'assert_title'):
        expected = er or td
        lines.append(f'{indent}page.verify_title("{expected}")')
    elif action in ('verify_url',):
        expected = er or td
        lines.append(f'{indent}page.verify_url_contains("{expected}")')
    elif action == 'verify_element_present':
        lines.append(f'{indent}assert page.is_element_present({lt_str}, "{lv}"), '
                     f'"Element not found: {lt}={lv}"')
    elif action == 'verify_element_visible':
        lines.append(f'{indent}assert page.is_element_visible({lt_str}, "{lv}"), '
                     f'"Element not visible: {lt}={lv}"')
    elif action in ('hover', 'mouse_over'):
        lines.append(f'{indent}page.hover({lt_str}, "{lv}")')
    elif action == 'double_click':
        lines.append(f'{indent}page.double_click({lt_str}, "{lv}")')
    elif action == 'right_click':
        lines.append(f'{indent}page.right_click({lt_str}, "{lv}")')
    elif action in ('wait', 'sleep'):
        seconds = td or lv or '2'
        lines.append(f'{indent}page.wait_seconds({seconds})')
    elif action == 'press_key':
        key = td or lv
        lines.append(f'{indent}page.press_key("{key}")')
    elif action == 'scroll_down':
        pixels = td or '500'
        lines.append(f'{indent}page.scroll_page("down", {pixels})')
    elif action == 'scroll_up':
        pixels = td or '500'
        lines.append(f'{indent}page.scroll_page("up", {pixels})')
    elif action == 'scroll_to_element':
        lines.append(f'{indent}page.scroll_to_element({lt_str}, "{lv}")')
    elif action == 'switch_frame':
        lines.append(f'{indent}page.switch_to_frame({lt_str}, "{lv}")')
    elif action == 'switch_default':
        lines.append(f'{indent}page.switch_to_frame()')
    elif action == 'accept_alert':
        lines.append(f'{indent}page.accept_alert()')
    elif action == 'dismiss_alert':
        lines.append(f'{indent}page.dismiss_alert()')
    elif action in ('take_screenshot', 'screenshot'):
        name = td or lv or 'screenshot'
        lines.append(f'{indent}page.take_screenshot("{name}")')
    elif action == 'refresh':
        lines.append(f'{indent}page.refresh_page()')
    elif action == 'go_back':
        lines.append(f'{indent}page.go_back()')
    elif action == 'upload_file':
        lines.append(f'{indent}page.upload_file({lt_str}, "{lv}", "{td}")')
    elif action == 'execute_js':
        script = td or lv
        lines.append(f'{indent}page.execute_js("{script}")')
    elif action == 'api_get':
        url = td or lv
        lines.append(f'{indent}response = requests.get("{url}", timeout=30)')
        if er:
            lines.append(f'{indent}assert response.status_code == {er}, '
                         f'f"Expected {er}, got {{response.status_code}}"')
    elif action == 'api_post':
        url = lv
        lines.append(f'{indent}response = requests.post("{url}", json={td or "{}"}, timeout=30)')
        if er:
            lines.append(f'{indent}assert response.status_code == {er}')
    elif action == 'verify_api_status':
        expected = er or td or '200'
        lines.append(f'{indent}assert response.status_code == {expected}')
    elif action in ('open_browser', 'close_browser'):
        lines.append(f'{indent}pass  # {action} handled by fixture')
    else:
        lines.append(f'{indent}# TODO: Unknown action "{action}" - implement manually')

    return '\n'.join(lines)


def generate_python_test_file(tc_id, tc_name, steps):
    """Generate a complete Python pytest test file for one test case."""
    func_name = sanitize_name(tc_name)
    step_code_lines = []
    for step in steps:
        comment = f"        # Step {step.get('Step_No', '?')}: {step.get('Action', '')}"
        step_code_lines.append(comment)
        step_code_lines.append(generate_step_code_python(step))
        step_code_lines.append('')

    step_code = '\n'.join(step_code_lines)

    template = f'''"""
Auto-generated test script from Excel
Test Case: {tc_id} - {tc_name}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

import os
import sys
import pytest
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.base.base_page import BasePage


class Test_{sanitize_name(tc_id).upper()}:
    """{tc_name}"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.page = BasePage(driver)

    @pytest.mark.regression
    def test_{func_name}(self):
        """Execute: {tc_name}"""
        page = self.page

{step_code}
'''
    return template


_java_step_counter = 0


def generate_step_code_java(step, indent='        '):
    """Generate Java code for a single test step."""
    global _java_step_counter
    _java_step_counter += 1
    step_id = _java_step_counter

    action = str(step.get('Action', '')).strip().lower()
    lt = step.get('Locator_Type', '') or ''
    lv = step.get('Locator_Value', '') or ''
    td = step.get('Test_Data', '') or ''
    er = step.get('Expected_Result', '') or ''

    lv_escaped = lv.replace('"', '\\"')
    td_escaped = td.replace('"', '\\"')
    er_escaped = er.replace('"', '\\"')

    by_map = {
        'id': f'By.id("{lv_escaped}")',
        'name': f'By.name("{lv_escaped}")',
        'xpath': f'By.xpath("{lv_escaped}")',
        'css': f'By.cssSelector("{lv_escaped}")',
        'class': f'By.className("{lv_escaped}")',
        'tag': f'By.tagName("{lv_escaped}")',
        'link_text': f'By.linkText("{lv_escaped}")',
        'partial_link_text': f'By.partialLinkText("{lv_escaped}")',
    }

    by_expr = by_map.get(lt.lower(), f'By.id("{lv_escaped}")') if lt else None

    if action in ('navigate', 'go_to_url', 'open_url'):
        url = td or lv
        return f'{indent}driver.get("{url}");'
    elif action == 'click':
        return (f'{indent}wait.until(ExpectedConditions.elementToBeClickable({by_expr})).click();')
    elif action in ('type', 'send_keys', 'enter_text'):
        var = f'el{step_id}'
        return (f'{indent}WebElement {var} = wait.until(ExpectedConditions.visibilityOfElementLocated({by_expr}));\n'
                f'{indent}{var}.clear();\n'
                f'{indent}{var}.sendKeys("{td_escaped}");')
    elif action == 'clear':
        return f'{indent}driver.findElement({by_expr}).clear();'
    elif action in ('select_dropdown', 'select'):
        return (f'{indent}Select dropdown = new Select(driver.findElement({by_expr}));\n'
                f'{indent}dropdown.selectByVisibleText("{td_escaped}");')
    elif action in ('verify_text', 'assert_text'):
        expected = er or td
        var = f'text{step_id}'
        return (f'{indent}String {var} = wait.until(ExpectedConditions.visibilityOfElementLocated({by_expr})).getText();\n'
                f'{indent}Assert.assertTrue({var}.contains("{expected}"), '
                f'"Expected \\"{expected}\\" but got \\"" + {var} + "\\"");')
    elif action in ('verify_title', 'assert_title'):
        expected = er or td
        return f'{indent}Assert.assertTrue(driver.getTitle().contains("{expected}"));'
    elif action in ('verify_url',):
        expected = er or td
        return f'{indent}Assert.assertTrue(driver.getCurrentUrl().contains("{expected}"));'
    elif action == 'verify_element_present':
        return (f'{indent}Assert.assertTrue(driver.findElements({by_expr}).size() > 0, '
                f'"Element not found: {lt}={lv_escaped}");')
    elif action in ('wait', 'sleep'):
        seconds = td or lv or '2'
        ms = int(float(seconds) * 1000)
        return f'{indent}Thread.sleep({ms});'
    elif action in ('take_screenshot', 'screenshot'):
        return (f'{indent}File screenshot = ((TakesScreenshot)driver).getScreenshotAs(OutputType.FILE);\n'
                f'{indent}FileUtils.copyFile(screenshot, new File("reports/screenshots/{td or "screenshot"}.png"));')
    elif action == 'refresh':
        return f'{indent}driver.navigate().refresh();'
    elif action == 'go_back':
        return f'{indent}driver.navigate().back();'
    elif action == 'accept_alert':
        return (f'{indent}wait.until(ExpectedConditions.alertIsPresent());\n'
                f'{indent}driver.switchTo().alert().accept();')
    elif action == 'dismiss_alert':
        return (f'{indent}wait.until(ExpectedConditions.alertIsPresent());\n'
                f'{indent}driver.switchTo().alert().dismiss();')
    elif action in ('hover', 'mouse_over'):
        var = f'hover{step_id}'
        return (f'{indent}WebElement {var} = driver.findElement({by_expr});\n'
                f'{indent}new Actions(driver).moveToElement({var}).perform();')
    elif action == 'scroll_down':
        pixels = td or '500'
        return f'{indent}((JavascriptExecutor)driver).executeScript("window.scrollBy(0, {pixels})");'
    elif action in ('open_browser', 'close_browser'):
        return f'{indent}// {action} handled by @BeforeMethod/@AfterMethod'
    else:
        return f'{indent}// TODO: Unknown action "{action}" - implement manually'


def generate_java_test_file(tc_id, tc_name, steps):
    """Generate a complete Java TestNG test file for one test case."""
    global _java_step_counter
    _java_step_counter = 0

    class_name = ''.join(word.capitalize() for word in sanitize_name(tc_name).split('_'))
    class_name = f"Test{class_name}"

    step_code_lines = []
    for step in steps:
        comment = f"        // Step {step.get('Step_No', '?')}: {step.get('Action', '')}"
        step_code_lines.append(comment)
        step_code_lines.append(generate_step_code_java(step))
        step_code_lines.append('')

    step_code = '\n'.join(step_code_lines)

    template = f'''/*
 * Auto-generated test script from Excel
 * Test Case: {tc_id} - {tc_name}
 * Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
 */

package com.automation.tests;

import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.Assert;
import org.testng.annotations.*;
import io.github.bonigarcia.wdm.WebDriverManager;
import org.apache.commons.io.FileUtils;

import java.io.File;
import java.time.Duration;

public class {class_name} {{

    private WebDriver driver;
    private WebDriverWait wait;

    @BeforeMethod
    public void setUp() {{
        WebDriverManager.chromedriver().setup();
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--no-sandbox", "--disable-dev-shm-usage");
        driver = new ChromeDriver(options);
        driver.manage().window().maximize();
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
        wait = new WebDriverWait(driver, Duration.ofSeconds(20));
    }}

    @Test(description = "{tc_name}")
    public void test_{sanitize_name(tc_name)}() throws Exception {{
{step_code}
    }}

    @AfterMethod
    public void tearDown() {{
        if (driver != null) {{
            driver.quit();
        }}
    }}
}}
'''
    return template


def generate_scripts(excel_path, language='both', output_dir=None, sheet_name=None):
    """Main function to generate test scripts from Excel."""
    handler = ExcelHandler(excel_path)
    test_cases = handler.get_test_cases_grouped(sheet_name)

    if not test_cases:
        print("[ERROR] No test cases found in Excel file")
        return

    if not output_dir:
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'generated_tests')

    python_dir = os.path.join(output_dir, 'python')
    java_dir = os.path.join(output_dir, 'java')

    generated = {'python': [], 'java': []}

    for tc_id, tc_data in test_cases.items():
        tc_name = tc_data['name']
        steps = tc_data['steps']
        safe_name = sanitize_name(tc_name)

        if language in ('python', 'both'):
            os.makedirs(python_dir, exist_ok=True)
            content = generate_python_test_file(tc_id, tc_name, steps)
            filepath = os.path.join(python_dir, f"test_{safe_name}.py")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            generated['python'].append(filepath)
            print(f"  [Python] Generated: {filepath}")

        if language in ('java', 'both'):
            os.makedirs(java_dir, exist_ok=True)
            content = generate_java_test_file(tc_id, tc_name, steps)
            class_name = ''.join(w.capitalize() for w in safe_name.split('_'))
            filepath = os.path.join(java_dir, f"Test{class_name}.java")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            generated['java'].append(filepath)
            print(f"  [Java]   Generated: {filepath}")

    # Generate conftest.py for generated Python tests
    if language in ('python', 'both') and generated['python']:
        conftest_path = os.path.join(python_dir, 'conftest.py')
        conftest_content = '''"""Auto-generated conftest.py for generated test scripts."""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.base.driver_factory import DriverFactory


@pytest.fixture(scope='function')
def driver():
    driver = DriverFactory.get_driver()
    yield driver
    driver.quit()
'''
        with open(conftest_path, 'w', encoding='utf-8') as f:
            f.write(conftest_content)

    print(f"\n{'='*60}")
    print(f"Script Generation Complete!")
    print(f"{'='*60}")
    if generated['python']:
        print(f"  Python scripts: {len(generated['python'])} files in {python_dir}")
    if generated['java']:
        print(f"  Java scripts:   {len(generated['java'])} files in {java_dir}")
    print(f"\nTo run generated Python tests:")
    print(f"  cd generated_tests/python && pytest -v")
    print(f"\nTo run generated Java tests:")
    print(f"  cd generated_tests/java && mvn test")

    return generated


def main():
    parser = argparse.ArgumentParser(
        description='Generate test scripts from Excel test cases',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_test_scripts.py --excel test_data/test_cases.xlsx --language python
  python generate_test_scripts.py --excel test_data/test_cases.xlsx --language java
  python generate_test_scripts.py --excel test_data/test_cases.xlsx --language both
  python generate_test_scripts.py --excel test_data/test_cases.xlsx --language python --output my_tests
        """
    )
    parser.add_argument('--excel', '-e', required=True, help='Path to Excel test cases file')
    parser.add_argument('--language', '-l', choices=['python', 'java', 'both'],
                        default='both', help='Language to generate scripts in (default: both)')
    parser.add_argument('--output', '-o', default=None, help='Output directory (default: generated_tests)')
    parser.add_argument('--sheet', '-s', default=None, help='Excel sheet name (default: active sheet)')

    args = parser.parse_args()

    if not os.path.exists(args.excel):
        print(f"[ERROR] Excel file not found: {args.excel}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  Test Script Generator")
    print(f"{'='*60}")
    print(f"  Excel file : {args.excel}")
    print(f"  Language   : {args.language}")
    print(f"  Output dir : {args.output or 'generated_tests'}")
    print(f"{'='*60}\n")

    generate_scripts(args.excel, args.language, args.output, args.sheet)


if __name__ == '__main__':
    main()
