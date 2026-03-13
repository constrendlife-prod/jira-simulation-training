"""
Simple script to run the Streamlit application.
"""
import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    import streamlit.web.cli as stcli

    # Run streamlit app
    sys.argv = ["streamlit", "run", "src/app.py", "--server.headless", "true"]
    sys.exit(stcli.main())
