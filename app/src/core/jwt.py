import jwt


from datetime import datetime, timedelta, timezone
from src.core import config
"""
This module provides functions for JWT (JSON Web Token) encoding and decoding.

Functions:
- create_access_token: Generates an access token with the given data and expiration time.
- encode_user_email: Encodes the user email into an access token with the specified expiration time.
- decode_user_email: Decodes the user email from the given access token.

Constants:
- ALGORITHM: The algorithm used for JWT encoding.
- access_token_jwt_subject: The subject of the access token JWT.
"""

ALGORITHM = "HS256"
access_token_jwt_subject = "access"

def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """
    Generates an access token using the provided data and expiration delta.
    Args:
        data (dict): The data to be encoded in the access token.
        expires_delta (timedelta, optional): The expiration time delta for the access token. Defaults to None.
    Returns:
        str: The encoded access token.
    Raises:
        None
    Example:
        data = {"user_id": 123}
        expires_delta = timedelta(hours=1)
        token = create_access_token(data=data, expires_delta=expires_delta)
    """
    # Copy the data to avoid modifying the original dictionary
    # Calculate the expiration time
    # Add the expiration time and subject to the data
    # Encode the data into a JWT using the SECRET_KEY and ALGORITHM
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def encode_user_email(email: str, access_token_expires):
    """
    Encodes the user email into a JWT access token.
    Args:
        email (str): The user's email address.
        access_token_expires: The expiration time for the access token.
    Returns:
        str: The encoded JWT access token.
    """
    
    return create_access_token(data={"email": email}, expires_delta=access_token_expires)

def decode_user_email(token: str):
    """
    Decode the user email from the given token.
    Args:
        token (str): The JWT token containing the user email.
    Returns:
        str: The decoded user email.
    Raises:
        None
    """
    
    return jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])['email']
