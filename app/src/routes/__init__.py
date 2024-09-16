from fastapi import APIRouter
from src.api import test_api
from src.admin.controllers import session_controller, users_controller

from src.api import inventory_forecasting_api
"""
This module initializes the API router and includes various routes.

The routes included are:
- session_controller.router: Handles session related routes.
- users_controller.router: Handles user related routes.
- test_api.router: Handles test API routes.
- inventory_forecasting_api.router: Handles inventory forecasting API routes.

Note: The session_controller.router and users_controller.router are not included in the API schema.
"""

api_router = APIRouter()

api_router.include_router(session_controller.router, tags=["views"], include_in_schema=False)
api_router.include_router(users_controller.router, tags=["views"], include_in_schema=False)

api_router.include_router(test_api.router, tags=["API"])
api_router.include_router(inventory_forecasting_api.router, tags=["API"])
