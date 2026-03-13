@echo off
REM Quick Start Script for Windows
echo ================================================
echo  CORE Engineer Training Portal - Startup
echo ================================================
echo.

REM Navigate to script directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Check if dependencies are installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Check if database exists
if not exist "data\tickets.db" (
    echo Initializing database with sample data...
    python src\init_data.py
    echo.
)

REM Start the application
echo ================================================
echo  Starting CORE Engineer Training Portal...
echo ================================================
echo.
echo  Access the application at: http://localhost:8501
echo.
echo  Press Ctrl+C to stop the server
echo ================================================
echo.

streamlit run src\app.py

pause
