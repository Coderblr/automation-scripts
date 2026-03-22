@echo off
title Automation Test Framework - Main Menu
color 0B

:MENU
cls
echo ============================================================
echo.
echo    AUTOMATION TEST FRAMEWORK
echo    Test Script Generator ^& Runner
echo.
echo ============================================================
echo.
echo    PYTHON + SELENIUM TESTS
echo    -----------------------
echo    1.  Run Tests from Excel File
echo    2.  Run URL Smoke Test
echo    3.  Run API Tests (FastAPI)
echo    4.  Run All Python Tests
echo.
echo    JAVA + SELENIUM TESTS
echo    ---------------------
echo    5.  Run Java Tests (TestNG)
echo.
echo    SCRIPT GENERATION
echo    -----------------
echo    6.  Generate Python Scripts from Excel
echo    7.  Generate Java Scripts from Excel
echo    8.  Generate Both (Python + Java)
echo.
echo    UTILITIES
echo    ---------
echo    9.  Create/Reset Excel Test Case Template
echo    10. Open Test Reports Folder
echo    11. Open Config File
echo    12. Run Setup (Install Dependencies)
echo.
echo    0.  Exit
echo.
echo ============================================================
echo.

set /p choice="  Enter your choice (0-12): "

if "%choice%"=="1" goto EXCEL_TEST
if "%choice%"=="2" goto URL_SMOKE
if "%choice%"=="3" goto API_TEST
if "%choice%"=="4" goto ALL_PYTHON
if "%choice%"=="5" goto JAVA_TEST
if "%choice%"=="6" goto GEN_PYTHON
if "%choice%"=="7" goto GEN_JAVA
if "%choice%"=="8" goto GEN_BOTH
if "%choice%"=="9" goto CREATE_TEMPLATE
if "%choice%"=="10" goto OPEN_REPORTS
if "%choice%"=="11" goto OPEN_CONFIG
if "%choice%"=="12" goto RUN_SETUP
if "%choice%"=="0" goto EXIT

echo.
echo  [ERROR] Invalid choice. Please enter a number between 0-12.
pause
goto MENU

:: ============================================================
:: PYTHON TESTS
:: ============================================================

:EXCEL_TEST
cls
echo ============================================================
echo    Run Tests from Excel File
echo ============================================================
echo.
echo  Options:
echo    1. Use default Excel file (test_data\test_cases.xlsx)
echo    2. Specify custom Excel file path
echo.
set /p excel_choice="  Enter choice (1-2): "

if "%excel_choice%"=="1" (
    set excel_path=test_data\test_cases.xlsx
) else (
    set /p excel_path="  Enter Excel file path: "
)

echo.
echo  Select browser:
echo    1. Chrome (default)
echo    2. Firefox
echo    3. Edge
echo.
set /p browser_choice="  Enter choice (1-3): "

set browser=chrome
if "%browser_choice%"=="2" set browser=firefox
if "%browser_choice%"=="3" set browser=edge

echo.
set /p headless="  Run headless? (y/N): "
set headless_flag=
if /i "%headless%"=="y" set headless_flag=--headless

echo.
echo  Running Excel-driven tests...
echo  Excel: %excel_path%
echo  Browser: %browser%
echo ============================================================
echo.

cd python_framework
python -m pytest tests/test_excel_driven.py -v --browser=%browser% --excel-file=../%excel_path% %headless_flag% --html=../reports/excel_test_report.html --self-contained-html
cd ..

echo.
echo  Test execution complete. Report: reports\excel_test_report.html
pause
goto MENU

:URL_SMOKE
cls
echo ============================================================
echo    URL Smoke Test
echo ============================================================
echo.
set /p test_url="  Enter URL to test (e.g., http://localhost:3000): "

echo.
echo  Select browser:
echo    1. Chrome (default)
echo    2. Firefox
echo    3. Edge
echo.
set /p browser_choice="  Enter choice (1-3): "

set browser=chrome
if "%browser_choice%"=="2" set browser=firefox
if "%browser_choice%"=="3" set browser=edge

echo.
set /p headless="  Run headless? (y/N): "
set headless_flag=
if /i "%headless%"=="y" set headless_flag=--headless

echo.
echo  Running smoke tests on: %test_url%
echo ============================================================
echo.

cd python_framework
python -m pytest tests/test_url_smoke.py -v --browser=%browser% --test-url=%test_url% %headless_flag% --html=../reports/smoke_test_report.html --self-contained-html
cd ..

echo.
echo  Smoke test complete. Report: reports\smoke_test_report.html
pause
goto MENU

:API_TEST
cls
echo ============================================================
echo    API Tests (FastAPI Backend)
echo ============================================================
echo.
set /p api_url="  Enter API base URL (default: http://localhost:8000): "
if "%api_url%"=="" set api_url=http://localhost:8000

echo.
echo  Running API tests against: %api_url%
echo ============================================================
echo.

cd python_framework
python -m pytest tests/test_api.py -v --api-url=%api_url% --html=../reports/api_test_report.html --self-contained-html
cd ..

echo.
echo  API test complete. Report: reports\api_test_report.html
pause
goto MENU

:ALL_PYTHON
cls
echo ============================================================
echo    Run All Python Tests
echo ============================================================
echo.
echo  Select browser:
echo    1. Chrome (default)
echo    2. Firefox
echo    3. Edge
echo.
set /p browser_choice="  Enter choice (1-3): "

set browser=chrome
if "%browser_choice%"=="2" set browser=firefox
if "%browser_choice%"=="3" set browser=edge

echo.
set /p headless="  Run headless? (y/N): "
set headless_flag=
if /i "%headless%"=="y" set headless_flag=--headless

echo.
echo  Running all Python tests...
echo ============================================================
echo.

cd python_framework
python -m pytest tests/ -v --browser=%browser% %headless_flag% --html=../reports/full_test_report.html --self-contained-html
cd ..

echo.
echo  All tests complete. Report: reports\full_test_report.html
pause
goto MENU

:: ============================================================
:: JAVA TESTS
:: ============================================================

:JAVA_TEST
cls
echo ============================================================
echo    Run Java Tests (TestNG)
echo ============================================================
echo.

java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Java is not installed. Please install Java JDK 11+.
    pause
    goto MENU
)

mvn -version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Maven is not installed. Please install Apache Maven.
    pause
    goto MENU
)

echo  Running Java TestNG tests...
echo ============================================================
echo.

cd java_framework
mvn clean test
cd ..

echo.
echo  Java tests complete. Check java_framework\target\surefire-reports for results.
pause
goto MENU

:: ============================================================
:: SCRIPT GENERATION
:: ============================================================

:GEN_PYTHON
cls
echo ============================================================
echo    Generate Python Test Scripts from Excel
echo ============================================================
echo.
set /p excel_path="  Enter Excel file path (default: test_data/test_cases.xlsx): "
if "%excel_path%"=="" set excel_path=test_data/test_cases.xlsx

echo.
echo  Generating Python test scripts...
echo ============================================================
echo.

python scripts/generate_test_scripts.py --excel %excel_path% --language python

echo.
echo  Generated scripts are in: generated_tests\python\
echo  Run them with: cd generated_tests\python ^&^& pytest -v
pause
goto MENU

:GEN_JAVA
cls
echo ============================================================
echo    Generate Java Test Scripts from Excel
echo ============================================================
echo.
set /p excel_path="  Enter Excel file path (default: test_data/test_cases.xlsx): "
if "%excel_path%"=="" set excel_path=test_data/test_cases.xlsx

echo.
echo  Generating Java test scripts...
echo ============================================================
echo.

python scripts/generate_test_scripts.py --excel %excel_path% --language java

echo.
echo  Generated scripts are in: generated_tests\java\
pause
goto MENU

:GEN_BOTH
cls
echo ============================================================
echo    Generate Python + Java Test Scripts from Excel
echo ============================================================
echo.
set /p excel_path="  Enter Excel file path (default: test_data/test_cases.xlsx): "
if "%excel_path%"=="" set excel_path=test_data/test_cases.xlsx

echo.
echo  Generating test scripts...
echo ============================================================
echo.

python scripts/generate_test_scripts.py --excel %excel_path% --language both

echo.
pause
goto MENU

:: ============================================================
:: UTILITIES
:: ============================================================

:CREATE_TEMPLATE
cls
echo ============================================================
echo    Create Excel Test Case Template
echo ============================================================
echo.
python -c "import sys; sys.path.insert(0, '.'); from python_framework.utils.excel_handler import create_test_case_template; create_test_case_template()"
echo.
echo  Template created at: test_data\test_cases.xlsx
echo  Open it in Excel to add your test cases.
pause
goto MENU

:OPEN_REPORTS
start "" "reports"
goto MENU

:OPEN_CONFIG
start notepad "config\config.ini"
goto MENU

:RUN_SETUP
call setup.bat
goto MENU

:EXIT
echo.
echo  Goodbye!
echo.
exit /b 0
