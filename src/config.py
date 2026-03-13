"""
Configuration loader for Jira Simulation Program.

Reads settings from .env file using python-dotenv.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Application configuration loaded from environment variables."""

    # Application settings
    APP_NAME = os.getenv('APP_NAME', 'Jira Simulation Program')
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # Admin configuration
    ADMIN_EMAILS = os.getenv('ADMIN_EMAILS', '').split(',')

    # Azure AD / MSAL
    MSAL_CLIENT_ID = os.getenv('MSAL_CLIENT_ID')
    MSAL_AUTHORITY = os.getenv('MSAL_AUTHORITY')
    MSAL_TENANT_ID = os.getenv('MSAL_TENANT_ID')

    # OIDC Authentication
    AUTH_CLIENT_ID = os.getenv('AUTH_CLIENT_ID')
    AUTH_CLIENT_SECRET = os.getenv('AUTH_CLIENT_SECRET')
    AUTH_REDIRECT_URI = os.getenv('AUTH_REDIRECT_URI')
    AUTH_COOKIE_SECRET = os.getenv('AUTH_COOKIE_SECRET')
    AUTH_SERVER_METADATA_URL = os.getenv('AUTH_SERVER_METADATA_URL')

    # Cosmos DB
    COSMOSDB_ENDPOINT = os.getenv('COSMOSDB_ENDPOINT')
    COSMOSDB_KEY = os.getenv('COSMOSDB_KEY')
    COSMOSDB_DATABASE_NAME = os.getenv('COSMOSDB_DATABASE_NAME')
    STORAGE_BACKEND = os.getenv('STORAGE_BACKEND', 'local')

    # Jira
    JIRA_URL = os.getenv('JIRA_URL')
    JIRA_EMAIL = os.getenv('JIRA_EMAIL')
    JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
    JIRA_PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY')

    # Database (SQL alternative)
    DATABASE_URL = os.getenv('DATABASE_URL')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', '5432'))
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')

    @classmethod
    def is_admin(cls, email: str) -> bool:
        """Check if an email is in the admin list."""
        return email.lower().strip() in [e.lower().strip() for e in cls.ADMIN_EMAILS if e]

    @classmethod
    def validate(cls) -> list[str]:
        """Validate required configuration and return list of missing items."""
        missing = []

        # Check required fields based on configuration
        if cls.STORAGE_BACKEND == 'cosmosdb':
            if not cls.COSMOSDB_ENDPOINT:
                missing.append('COSMOSDB_ENDPOINT')
            if not cls.COSMOSDB_KEY:
                missing.append('COSMOSDB_KEY')
            if not cls.COSMOSDB_DATABASE_NAME:
                missing.append('COSMOSDB_DATABASE_NAME')

        return missing


# Create a singleton instance
config = Config()
