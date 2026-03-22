@echo off
setlocal enabledelayedexpansion
color 0A
title Java Automation Framework - Test Runner

echo ============================================================
echo   JAVA + SELENIUM TEST AUTOMATION FRAMEWORK
echo   SauceDemo Regression Testing
echo ============================================================
echo.

REM --- Check Java ---
java -version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Java is not installed or not in PATH.
    echo         Please install Java JDK 11+ and try again.
    echo         Download: https://adoptium.net/
    pause
    exit /b 1
)

REM --- Check Maven ---
mvn -version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Maven is not installed or not in PATH.
    echo         Please install Apache Maven 3.8+ and try again.
    echo         Download: https://maven.apache.org/download.cgi
    pause
    exit /b 1
)

echo [OK] Java found
echo [OK] Maven found
echo.

REM --- Browser selection ---
echo  Select Browser:
echo  ---------------------------------
echo    1. Chrome  (default)
echo    2. Microsoft Edge
echo    3. Firefox
echo  ---------------------------------
echo.
set /p browser_choice="  Enter choice (1/2/3): "

if "%browser_choice%"=="2" (
    set BROWSER=edge
) else if "%browser_choice%"=="3" (
    set BROWSER=firefox
) else (
    set BROWSER=chrome
)

echo.
echo  Selected browser: %BROWSER%
echo.

REM --- Update config.ini with selected browser ---
set CONFIG_FILE=%~dp0config\config.ini
if exist "%CONFIG_FILE%" (
    echo [INFO] Updating config.ini with browser = %BROWSER%
    powershell -Command "(Get-Content '%CONFIG_FILE%') -replace '^browser_name\s*=.*', 'browser_name = %BROWSER%' | Set-Content '%CONFIG_FILE%'"
)

REM --- Check if Excel file exists ---
if not exist "%~dp0test_data\test_cases.xlsx" (
    echo [INFO] Excel file not found. Generating test_cases.xlsx ...
    cd /d "%~dp0"
    python scripts\generate_test_scripts.py
    echo.
)

REM --- Run Maven tests ---
echo ============================================================
echo   STARTING TEST EXECUTION ...
echo   Browser: %BROWSER%
echo   Time   : %date% %time%
echo ============================================================
echo.

cd /d "%~dp0java_framework"

REM Build and run tests
call mvn clean test -Dbrowser=%BROWSER% 2>&1

echo.
echo ============================================================
if %errorlevel% equ 0 (
    color 0A
    echo   ALL TESTS PASSED!
) else (
    color 0C
    echo   SOME TESTS FAILED - Check reports for details.
)
echo ============================================================
echo.

REM --- Check for TestNG reports ---
if exist "target\surefire-reports\index.html" (
    echo [INFO] Opening TestNG HTML report...
    start "" "target\surefire-reports\index.html"
) else if exist "target\surefire-reports\emailable-report.html" (
    echo [INFO] Opening emailable report...
    start "" "target\surefire-reports\emailable-report.html"
) else (
    echo [INFO] TestNG reports are in: java_framework\target\surefire-reports\
)

echo.
echo  Press any key to exit...
pause >nul
color
exit /b 0
