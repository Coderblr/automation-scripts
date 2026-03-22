"""
Excel-Driven Test Runner

Reads test cases from an Excel file and executes them using the Keyword Engine.
The browser opens visibly, and testers can watch the automation in real time.
After execution, an HTML report and Excel results file are generated.

Usage:
    pytest test_excel_driven.py --excel-file=path/to/tests.xlsx --browser=chrome
"""

import os
import sys
import time
import logging
import pytest
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from python_framework.utils.excel_handler import ExcelHandler
from python_framework.utils.keyword_engine import KeywordEngine

logger = logging.getLogger(__name__)


def _print_banner(tc_id, tc_name, total, current):
    """Print a visible banner in the console for each test case."""
    bar = "=" * 60
    print(f"\n{bar}")
    print(f"  [{current}/{total}] {tc_id} - {tc_name}")
    print(f"{bar}")


class TestExcelDriven:
    """Runs all test cases from Excel in a single browser session."""

    @pytest.fixture(autouse=True)
    def setup(self, driver, excel_file, sheet_name):
        self.driver = driver
        self.excel_file = excel_file
        self.sheet_name = sheet_name
        self.engine = KeywordEngine(driver)
        self.results = []

    def _get_test_cases(self):
        handler = ExcelHandler(self.excel_file)
        return handler.get_test_cases_grouped(self.sheet_name)

    @pytest.mark.excel
    @pytest.mark.regression
    def test_run_excel_test_cases(self):
        """Execute all test cases from the Excel file with live browser."""
        test_cases = self._get_test_cases()

        if not test_cases:
            pytest.skip("No test cases found in Excel file")

        tc_list = list(test_cases.items())
        total = len(tc_list)
        passed_count = 0
        failed_count = 0
        failures = []

        print(f"\n{'#' * 60}")
        print(f"  STARTING TEST EXECUTION - {total} Test Cases")
        print(f"{'#' * 60}")

        for idx, (tc_id, tc_data) in enumerate(tc_list, 1):
            tc_name = tc_data['name']
            _print_banner(tc_id, tc_name, total, idx)

            # Clear browser state between test cases so each starts fresh
            try:
                self.driver.delete_all_cookies()
                self.driver.execute_script("window.localStorage.clear();")
                self.driver.execute_script("window.sessionStorage.clear();")
            except Exception:
                pass

            tc_failed = False
            step_count = len(tc_data['steps'])

            for step in tc_data['steps']:
                step_no = step['Step_No']
                action = step['Action']
                start_time = time.time()

                result = {
                    'Test_Case_ID': tc_id,
                    'Test_Case_Name': tc_name,
                    'Step_No': step_no,
                    'Action': action,
                    'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                }

                try:
                    self.engine.execute_step(
                        action=action,
                        locator_type=step.get('Locator_Type') or None,
                        locator_value=step.get('Locator_Value') or None,
                        test_data=step.get('Test_Data') or None,
                        expected_result=step.get('Expected_Result') or None,
                    )
                    result['Status'] = 'PASS'
                    result['Error_Message'] = ''
                    print(f"    Step {step_no}/{step_count}: {action:30s} -> PASS")

                except Exception as e:
                    result['Status'] = 'FAIL'
                    result['Error_Message'] = str(e)
                    tc_failed = True
                    print(f"    Step {step_no}/{step_count}: {action:30s} -> FAIL: {e}")
                    try:
                        self.engine.execute_step('take_screenshot',
                                                 test_data=f"FAIL_{tc_id}_step{step_no}")
                    except Exception:
                        pass

                result['Duration_ms'] = int((time.time() - start_time) * 1000)
                self.results.append(result)

            if tc_failed:
                failed_count += 1
                failures.append(f"{tc_id}: {tc_name}")
                print(f"\n    >>> {tc_id} RESULT: FAILED <<<")
            else:
                passed_count += 1
                print(f"\n    >>> {tc_id} RESULT: PASSED <<<")

        # Print summary
        print(f"\n{'#' * 60}")
        print(f"  EXECUTION SUMMARY")
        print(f"{'#' * 60}")
        print(f"  Total : {total}")
        print(f"  Passed: {passed_count}")
        print(f"  Failed: {failed_count}")
        if failures:
            print(f"\n  Failed test cases:")
            for f in failures:
                print(f"    - {f}")
        print(f"{'#' * 60}\n")

        # Write results to Excel
        if self.results:
            try:
                result_path = ExcelHandler.write_results(self.results)
                print(f"  Excel results saved: {result_path}")
            except Exception as e:
                logger.error(f"Failed to write results: {e}")

        if failures:
            pytest.fail(
                f"{len(failures)} of {total} test case(s) failed:\n" +
                "\n".join(f"  - {f}" for f in failures)
            )
