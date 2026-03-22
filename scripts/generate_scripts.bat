@echo off
title Test Script Generator
color 0C

echo ============================================================
echo    Test Script Generator - Excel to Code
echo ============================================================
echo.

if "%~1"=="" (
    set /p excel_path="  Enter Excel file path (default: test_data/test_cases.xlsx): "
    if "!excel_path!"=="" set excel_path=test_data/test_cases.xlsx
) else (
    set excel_path=%~1
)

echo.
echo  Select language to generate:
echo    1. Python (pytest + Selenium)
echo    2. Java (TestNG + Selenium)
echo    3. Both
echo.
set /p lang_choice="  Enter choice (1-3): "

set language=both
if "%lang_choice%"=="1" set language=python
if "%lang_choice%"=="2" set language=java

echo.
echo  Generating %language% test scripts...
echo ============================================================
echo.

cd /d "%~dp0.."
python scripts/generate_test_scripts.py --excel %excel_path% --language %language%

echo.
pause
