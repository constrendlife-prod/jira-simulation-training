@echo off
REM ────────────────────────────────────────────────────────────────────────────
REM Git Push Helper Script for Windows
REM ────────────────────────────────────────────────────────────────────────────
REM This script helps you push to GitHub using credentials from .env
REM ────────────────────────────────────────────────────────────────────────────

echo ────────────────────────────────────────────────────────────────
echo 🚀 Git Push Helper for Jira Simulation Project
echo ────────────────────────────────────────────────────────────────
echo.

REM Show current status
echo 📊 Current Git Status:
git status --short
echo.

REM Ask for confirmation
set /p CONFIRM="Do you want to commit and push these changes? (y/n): "

if /i "%CONFIRM%"=="y" (
    echo.
    echo 📦 Adding files...
    git add .

    echo 💾 Creating commit...
    set /p COMMIT_MSG="Enter commit message (or press Enter for default): "
    if "%COMMIT_MSG%"=="" set COMMIT_MSG=Update: Changes to CORE Engineer Training Portal
    git commit -m "%COMMIT_MSG%"

    echo 🔐 Pushing to GitHub...
    REM Note: You'll need to enter your GitHub token as password when prompted
    git push origin main

    echo.
    echo ✅ Successfully pushed to GitHub!
    echo 🔗 Repository: https://github.com/constrendlife-prod/jira-simulation-training
) else (
    echo.
    echo ❌ Push cancelled.
)

pause
