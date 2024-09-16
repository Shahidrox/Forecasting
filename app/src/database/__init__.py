from src.database.session import Session
from src.utils.logger_utils import logger
"""
This module provides a function to get a database session.

The `get_db` function is an asynchronous generator that yields a database session. It is used as a middleware to handle database connections and ensure proper closing of the session.

Returns:
    Session: A database session object.

Raises:
    Exception: If there is an error in the database connection.

Example:
    async for db in get_db():
        # Use the database session
        ...
"""

async def get_db():
    """
    Asynchronous function to get a database connection.
    Returns:
        Session: A database session object.
    Raises:
        Exception: If there is an error in the database connection.
    """
    # Create a new database session
    # Yield the database session
    # Log the error and raise an exception
    # Close the database session
  
  db = Session()
  try:
      yield db
  except Exception as e:
      logger.error(f"Middleware batabase connection error: {e}")
      raise
  finally:
      db.close()