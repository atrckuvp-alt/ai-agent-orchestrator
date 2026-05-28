@echo off
cd /d "%~dp0"

echo ==========================================
echo AI Agent Research Team - Live Run
echo ==========================================
echo.

python 04_scripts\run_orchestrator.py --api openrouter

echo.
echo ==========================================
echo Finished.
echo Check 03_reports and 00_memory folders.
echo ==========================================

pause