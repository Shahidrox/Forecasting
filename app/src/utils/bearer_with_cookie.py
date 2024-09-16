from typing import Dict
from typing import Optional

from fastapi import HTTPException
from fastapi import Request, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param

class OAuth2PasswordBearerWithCookie(OAuth2):
    """
    Custom OAuth2 class for bearer token authentication with cookie.

    Args:
        tokenUrl (str): The URL to obtain the token.
        scheme_name (str, optional): The name of the authentication scheme. Defaults to None.
        scopes (Dict[str, str], optional): The scopes required for the token. Defaults to None.
        auto_error (bool, optional): Whether to raise an error if authentication fails. Defaults to True.

    Returns:
        Optional[str]: The bearer token extracted from the request cookie.

    Raises:
        HTTPException: If authentication fails and auto_error is True.

    Example:
        bearer = OAuth2PasswordBearerWithCookie(tokenUrl="/token", scopes={"read": "Read access"})
        token = await bearer(request)
        if token:
            # Token is valid, continue with the request
            # Token is invalid or missing, handle accordingly
    """
        pass

        pass

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get(
            "access_token"
        )

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_303_SEE_OTHER,
                    detail="Not authenticated",
                    headers={"Location": "/login"},
                )
            else:
                return None
        return param