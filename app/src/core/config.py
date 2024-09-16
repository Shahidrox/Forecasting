
"""
Configuration settings for the forecasting application.

Attributes:
  BACKEND_CORS_ORIGINS (str): The allowed origins for CORS (Cross-Origin Resource Sharing).
  DATABASE_URI (str): The URI for the SQLite database.
  SECRET_KEY (bytes): The secret key used for encryption.
  ACCESS_TOKEN_EXPIRE_MINUTES (int): The expiration time for access tokens in minutes.
"""

BACKEND_CORS_ORIGINS='https://localhost:8000'
DATABASE_URI = "sqlite:///./forecasting.db"
SECRET_KEY = b'\xb0\x11\x00 \xa1\x88}i\xc2\xae\x18\x93P\x17|\x04\x7fy\xb5llw\xd3=\x9a\t\xc0\x8f,\xac\x00\xbf'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days