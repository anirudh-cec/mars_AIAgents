"""
Mars AI Agents - Gmail Integration and Processing System

A comprehensive system for processing Gmail attachments with React frontend 
and FastAPI backend integration.

Modules:
    - api_server: FastAPI backend server
    - get_data: Gmail API integration for downloading attachments  
    - start_dev: Development server launcher
    - main: Main application entry point
"""

__version__ = "0.1.0"
__author__ = "Mars AI Agents Team"
__description__ = "Mars AI Agents - Gmail integration and processing system with FastAPI backend and React frontend"

# Import main modules for easy access
from . import api_server
from . import get_data
from . import utils
from . import config

# Define package-level constants
GMAIL_TARGET_EMAIL = "demotest.tcs@gmail.com"
DATA_FOLDER = "data"
STATIC_FOLDER = "static" 
TEMPLATES_FOLDER = "templates"

# Version info
VERSION_INFO = {
    "version": __version__,
    "description": __description__,
    "author": __author__
}

__all__ = [
    'api_server',
    'get_data',
    'utils',
    'config',
    'GMAIL_TARGET_EMAIL',
    'DATA_FOLDER',
    'STATIC_FOLDER',
    'TEMPLATES_FOLDER',
    'VERSION_INFO'
]
