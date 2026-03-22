@echo off
setlocal enabledelayedexpansion
title SauceDemo - Automated Regression Testing
color 0B

cls
echo.
echo  ==========================================================
echo.
echo     SAUCEDEMO - AUTOMATED REGRESSION TESTING
echo     ==========================================
echo.
echo     Application : https://www.saucedemo.com/v1/
echo     Test Cases  : 12 scenarios (Login, Cart, Checkout...)
echo     Framework   : Python + Selenium
echo.
echo  ==========================================================
echo.
echo     Select your browser:
echo.
echo        1. Google Chrome
echo        2. Microsoft Edge
echo        3. Mozilla Firefox
echo.
echo  ==========================================================
echo.

set /p browser_choice="     Enter choice (1/2/3): "

set browser=chrome
if "%browser_choice%"=="2" set browser=edge
if "%browser_choice%"=="3" set browser=firefox

cls
echo.
echo  ==========================================================
echo     STARTING AUTOMATED TESTING
echo  ==========================================================
echo.
echo     Browser     : %browser%
echo     Test Suite  : SauceDemo Regression (12 Test Cases)
echo     Excel File  : test_data\test_cases.xlsx
echo.
echo  ==========================================================
echo.
echo     The browser will open now. Please do NOT close it.
echo     Watch the automation run through all test cases:
echo.
echo       TC001 - Valid Login
echo       TC002 - Invalid Login
echo       TC003 - Locked Out User
echo       TC004 - Product Page Verification
echo       TC005 - Add Product to Cart
echo       TC006 - Remove Product from Cart
echo       TC007 - Complete Checkout Flow
echo       TC008 - Product Sorting
echo       TC009 - Logout
echo       TC010 - Cart Badge Count
echo       TC011 - Product Details Navigation
echo       TC012 - Checkout Without Info
echo.
echo  ==========================================================
echo.
echo     Starting in 3 seconds...
timeout /t 3 /nobreak >nul

:: Check if Excel template exists, create if not
if not exist "test_data\test_cases.xlsx" (
    echo     [INFO] Creating Excel test case template...
    python -c "import sys; sys.path.insert(0, '.'); from python_framework.utils.excel_handler import create_test_case_template; create_test_case_template()"
    echo.
)

echo  ----------------------------------------------------------
echo     TEST EXECUTION LOG
echo  ----------------------------------------------------------
echo.

:: Run the Excel-driven tests with visible browser
cd python_framework
python -m pytest tests/test_excel_driven.py::TestExcelDriven::test_run_excel_test_cases -v --tb=short --browser=%browser% --excel-file=../test_data/test_cases.xlsx --html=../reports/test_report.html --self-contained-html 2>&1
set test_exit_code=%errorlevel%
cd ..

echo.
echo  ==========================================================
echo     TEST EXECUTION COMPLETE
echo  ==========================================================
echo.

if %test_exit_code% equ 0 (
    color 0A
    echo     RESULT:  ALL TESTS PASSED
) else (
    color 0C
    echo     RESULT:  SOME TESTS FAILED - Check report for details
)

echo.
echo     Reports generated:
echo       HTML Report  : reports\test_report.html
echo.

:: Find and show the Excel results file
for /f "delims=" %%f in ('dir /b /o-d reports\test_results_*.xlsx 2^>nul') do (
    echo       Excel Report : reports\%%f
    goto :found_excel
)
:found_excel

echo       Screenshots  : reports\screenshots\
echo       Logs         : logs\
echo.
echo  ==========================================================
echo.

:: Auto-open the HTML report
echo     Opening test report in your default browser...
echo.
if exist "reports\test_report.html" (
    start "" "reports\test_report.html"
) else (
    echo     [WARNING] HTML report not found.
)

echo.
echo     Press any key to exit...
pause >nul
