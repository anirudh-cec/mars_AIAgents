"""
Mars AI Agents - Configuration Package

This package contains configuration files and settings for the Mars AI Agents system.

Modules:
    - settings: Application settings and configuration
    - gmail_config: Gmail API configuration
    - server_config: FastAPI server configuration
    - logging_config: Logging configuration
"""

__version__ = "0.1.0"

# Default configuration values
DEFAULT_CONFIG = {
    'gmail': {
        'target_email': 'demotest.tcs@gmail.com',
        'search_hours_back': 24,
        'max_results': 10,
        'credentials_file': 'credentials.json',
        'token_file': 'token.json'
    },
    'server': {
        'host': '0.0.0.0',
        'port': 8000,
        'reload': True,
        'log_level': 'info'
    },
    'frontend': {
        'port': 3000,
        'host': 'localhost'
    },
    'data': {
        'folder': 'data',
        'static_folder': 'static',
        'templates_folder': 'templates'
    }
}

# Import configuration modules (when they exist)
# from . import settings
# from . import gmail_config
# from . import server_config
# from . import logging_config

def get_config():
    """Get the default configuration."""
    return DEFAULT_CONFIG.copy()

def get_gmail_config():
    """Get Gmail-specific configuration."""
    return DEFAULT_CONFIG['gmail'].copy()

def get_server_config():
    """Get server-specific configuration."""
    return DEFAULT_CONFIG['server'].copy()

__all__ = [
    'DEFAULT_CONFIG',
    'get_config',
    'get_gmail_config', 
    'get_server_config'
]