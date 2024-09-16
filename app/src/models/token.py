from pydantic import BaseModel
"""
This module contains the definition of the Token and TokenPayload classes.

Token:
    A class representing a token with an access token and token type.

    Attributes:
        access_token (str): The access token.
        token_type (str): The type of the token.

TokenPayload:
    A class representing the payload of a token.

    Attributes:
        user_id (int, optional): The user ID associated with the token. Defaults to None.
"""

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    user_id: int = None
