#!/bin/bash
# Quick Start Script for Linux/Mac

echo "================================================"
echo " CORE Engineer Training Portal - Startup"
echo "================================================"
echo ""

# Navigate to script directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
python -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Check if database exists
if [ ! -f "data/tickets.db" ]; then
    echo "Initializing database with sample data..."
    python src/init_data.py
    echo ""
fi

# Start the application
echo "================================================"
echo " Starting CORE Engineer Training Portal..."
echo "================================================"
echo ""
echo " Access the application at: http://localhost:8501"
echo ""
echo " Press Ctrl+C to stop the server"
echo "================================================"
echo ""

streamlit run src/app.py
