# Jira Ticketing System - CORE Engineer Training Platform

## Overview
A web-based ticketing simulation system designed for CORE Engineer training. This platform allows administrators to create dispatch cases/scenarios and enables engineers to practice ticket resolution, communication, and escalation workflows.

## Features

### Admin Features
- Create dispatch cases with detailed training scenarios
- View and manage all tickets
- Assign tickets to CORE engineers
- Handle escalations (Assign back Reported)
- Track ticket history and audit trail

### Engineer Features
- View assigned tickets with training scenarios
- Reply and communicate on tickets
- Escalate to SEG when needed
- Assign back to CORE from reported status
- Practice real-world ticket workflows

## Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone or navigate to this repository

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Initialize the database with sample data:
```bash
python src/init_data.py
```

## Usage

### Running the Application

Start the Streamlit web application:
```bash
streamlit run src/app.py
```

Or use the run script:
```bash
python run.py
```

The application will open in your default web browser at `http://localhost:8501`

### Login Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Engineer Accounts:**
- Username: `engineer1` | Password: `eng123` (John Smith)
- Username: `engineer2` | Password: `eng123` (Sarah Johnson)
- Username: `engineer3` | Password: `eng123` (Mike Chen)
- Username: `engineer4` | Password: `eng123` (Emily Davis)

## Project Structure

```
Jira - Simulation Program/
├── .claude/          # Claude Code configuration
├── src/              # Source code
├── tests/            # Unit tests
├── data/             # Data files
├── config/           # Configuration files
├── .env              # Environment variables (not in git)
├── .gitignore        # Git ignore rules
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Contributing
Add contribution guidelines here.

## License
Add license information here.
