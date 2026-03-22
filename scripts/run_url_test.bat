@echo off
title URL Smoke Test
color 0A

echo ============================================================
echo    Quick URL Smoke Test
echo ============================================================
echo.

if "%~1"=="" (
    set /p test_url="  Enter URL to test: "
) else (
    set test_url=%~1
)

echo.
echo  Testing: %test_url%
echo ============================================================
echo.

cd /d "%~dp0..\python_framework"
python -m pytest tests/test_url_smoke.py -v --test-url=%test_url% --html=../reports/smoke_report.html --self-contained-html
cd /d "%~dp0.."

echo.
echo  Report: reports\smoke_report.html
pause
