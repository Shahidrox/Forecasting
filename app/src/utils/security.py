import jwt
from jwt.exceptions import PyJWTError

from fastapi import Depends, HTTPException, Security, status
from src.utils.bearer_with_cookie import OAuth2PasswordBearerWithCookie
from sqlalchemy.orm import Session

from src.database import get_db
from src.core import config
from src.models import User
from src.core.jwt import ALGORITHM
from src.models.token import TokenPayload
from src import services
"""
This module contains functions related to user authentication and authorization.
Functions:
- get_current_user: Retrieves the current user based on the provided token.
- get_current_active_user: Retrieves the current active user based on the provided token.
Dependencies:
- jwt: JSON Web Token library for decoding and verifying tokens.
- PyJWTError: Exception class for JWT related errors.
- fastapi: FastAPI framework for building APIs.
- Depends: Dependency injection decorator for FastAPI.
- HTTPException: Exception class for HTTP related errors.
- status: HTTP status codes.
- OAuth2PasswordBearerWithCookie: Custom OAuth2 password bearer with cookie authentication scheme.
- Session: SQLAlchemy session object.
- get_db: Function for retrieving the database session.
- config: Configuration settings for the application.
- User: User model class.
- ALGORITHM: Algorithm used for JWT encoding and decoding.
- TokenPayload: Token payload model class.
- services: Module containing various services for interacting with the database.
"""

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login")

def get_current_user(db: Session = Depends(get_db), token: str = Security(oauth2_scheme)):
  """
  Retrieves the current user based on the provided token.
  Args:
    db (Session): The database session.
    token (str): The authentication token.
  Returns:
    User: The current user.
  Raises:
    HTTPException: If the token has expired or is invalid.
  """
  
  try:
    payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
    token_data = TokenPayload(**payload)
  except PyJWTError:
    raise HTTPException(
      status_code=status.HTTP_303_SEE_OTHER,
      detail="Token has expired. Please log in again.",
      headers={"Location": "/login"},
    )
  user = services.user_service.get(db, user_id=token_data.user_id)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_303_SEE_OTHER,
      detail="User not found",
      headers={"Location": "/login"},
    )
  return user


def get_current_active_user(current_user: User = Security(get_current_user)):
  """
  Get the current active user.

  Args:
    current_user (User, optional): The current user. Defaults to Security(get_current_user).

  Raises:
    HTTPException: If the current user is inactive.

  Returns:
    User: The current active user.
  """

  if not services.user_service.is_active(current_user):
    raise HTTPException(
      status_code=status.HTTP_303_SEE_OTHER,
      detail="Inactive user",
      headers={"Location": "/login"},
    )
  return current_user

