@echo off
title Automation Test Framework - Setup
color 0A

echo ============================================================
echo    AUTOMATION TEST FRAMEWORK - SETUP
echo ============================================================
echo.

:: Check Python
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo         Download from: https://www.python.org/downloads/
    echo         Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)
python --version
echo [OK] Python found.
echo.

:: Install Python dependencies
echo [2/4] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [WARNING] Some packages may have failed to install.
) else (
    echo [OK] Python dependencies installed.
)
echo.

:: Create Excel template
echo [3/4] Creating Excel test case template...
python -c "import sys; sys.path.insert(0, '.'); from python_framework.utils.excel_handler import create_test_case_template; create_test_case_template()"
echo.

:: Check Java (optional)
echo [4/4] Checking Java installation (optional for Java tests)...
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Java not found. Java tests won't be available.
    echo        Download from: https://adoptium.net/
) else (
    java -version 2>&1
    echo [OK] Java found.
    
    mvn -version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [INFO] Maven not found. Required for Java tests.
        echo        Download from: https://maven.apache.org/download.cgi
    ) else (
        echo [OK] Maven found.
        echo Installing Java dependencies...
        cd java_framework
        mvn clean install -DskipTests -q
        cd ..
        echo [OK] Java dependencies installed.
    )
)

echo.
echo ============================================================
echo    SETUP COMPLETE!
echo ============================================================
echo.
echo  Next steps:
echo    1. Edit config\config.ini with your application URLs
echo    2. Edit test_data\test_cases.xlsx with your test cases
echo    3. Run: run_tests.bat
echo.
pause
