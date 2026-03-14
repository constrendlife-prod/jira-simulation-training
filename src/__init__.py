"""Jira Simulation Program - Main package."""

__version__ = '0.1.0'

# Import the main app so Streamlit Cloud can run it
# This runs when Streamlit loads src/__init__.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Import everything from app.py - this will execute the app
from app import *
