# Jira - Simulation Program

## Project Overview
A simulation program for Jira workflows and processes. This project allows testing and modeling of Jira ticket workflows, automations, and processes.

## Tech Stack
- **Language**: Python 3.8+
- **Configuration**: Environment variables (.env)
- **Dependencies**: Managed via requirements.txt

## Project Structure
- `src/` - Main source code
  - Core simulation logic
  - Jira workflow models
- `tests/` - Unit tests
- `data/` - Sample data and inputs
- `config/` - Configuration files
- `.env` - Environment variables (secrets, API keys)

## Configuration
- Uses `.env` file for environment variables
- Load with `python-dotenv` package
- Never commit `.env` to version control

## Coding Standards
- Follow PEP 8 for Python code
- Use type hints where applicable
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular
- No emojis in code unless explicitly requested

## Development Workflow
1. Activate virtual environment: `venv/Scripts/activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `pytest tests/`
4. Run main program: `python src/main.py`

## Important Notes
- Keep secrets in `.env` file only
- Update requirements.txt when adding new dependencies
- Write tests for all new features
- Document API integrations and external dependencies
