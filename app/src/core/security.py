from passlib.context import CryptContext
from core.security import get_password_hash, verify_password
"""
This module provides functions for handling password security.

Functions:
- get_password_hash(password: str) -> str: Hashes a password using bcrypt algorithm.
- verify_password(plain_password: str, hashed_password: str) -> bool: Verifies a plain password against a hashed password.

Usage:
1. Import the module:

2. Hash a password:
    hashed_password = get_password_hash("password123")

3. Verify a password:
    is_valid = verify_password("password123", hashed_password)
"""


# Create a CryptContext instance
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Generates a hash of the given password.
    Args:
        password (str): The password to be hashed.
    Returns:
        str: The hashed password.
    """
    
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if the plain password matches the hashed password.
    Args:
        plain_password (str): The plain password to be verified.
        hashed_password (str): The hashed password to compare against.
    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    
    return pwd_context.verify(plain_password, hashed_password)
