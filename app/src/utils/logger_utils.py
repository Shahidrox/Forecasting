import logging
"""
This module provides utilities for logging.

Functions:
  - None

Classes:
  - None

Variables:
  - logger: The logger object for this module.

Usage:
  - Import the logger object from this module to use it for logging in other modules.
"""

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
