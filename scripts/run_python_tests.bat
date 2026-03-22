@echo off
title Run Python Tests
color 0E

echo ============================================================
echo    Run Python Selenium Tests
echo ============================================================
echo.
echo  Usage: run_python_tests.bat [OPTIONS]
echo.
echo  Arguments (all optional):
echo    --browser    chrome/firefox/edge (default: chrome)
echo    --headless   Run in headless mode
echo    --test-url   URL for smoke testing
echo    --excel-file Path to Excel test cases
echo    --api-url    API base URL
echo.
echo ============================================================
echo.

cd /d "%~dp0..\python_framework"
python -m pytest tests/ -v %* --html=../reports/python_report.html --self-contained-html
cd /d "%~dp0.."

echo.
echo  Report saved to: reports\python_report.html
pause
