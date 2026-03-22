@echo off
title Run Java Tests
color 0D

echo ============================================================
echo    Run Java Selenium Tests (TestNG)
echo ============================================================
echo.

java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Java is not installed or not in PATH.
    pause
    exit /b 1
)

mvn -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Maven is not installed or not in PATH.
    pause
    exit /b 1
)

cd /d "%~dp0..\java_framework"

echo  Running Maven tests...
echo.
mvn clean test %*

echo.
echo  Check results in: java_framework\target\surefire-reports\
cd /d "%~dp0.."
pause
