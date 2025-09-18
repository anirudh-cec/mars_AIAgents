"""
Mars AI Agents - Utility Functions Package

This package contains utility functions and helper modules for the Mars AI Agents system.

Modules:
    - file_utils: File handling and manipulation utilities
    - email_utils: Email processing utilities  
    - auth_utils: Authentication and authorization utilities
    - logging_utils: Logging configuration and utilities
"""

__version__ = "0.1.0"

# Import utility modules (when they exist)
# from . import file_utils
# from . import email_utils  
# from . import auth_utils
# from . import logging_utils

def get_utils_info():
    """Get information about available utilities."""
    return {
        'version': __version__,
        'description': 'Mars AI Agents utility functions package',
        'available_modules': [
            # Add module names as they are created
        ]
    }

__all__ = [
    'get_utils_info'
]