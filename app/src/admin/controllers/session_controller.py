from fastapi import APIRouter, Request, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from datetime import timedelta

from src.database import get_db
from src.utils.security import get_current_active_user
from src.core.template_setting import templates
from src import services
from src.serializers.user_serializer import UserCreate
from src.core import config
from src.core.jwt import create_access_token

from src.models import User
from src.services import product_service

router    = APIRouter()

@router.get("/")
async def dashboard(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
  """
  Dashboard function to handle the request and render the dashboard page.

  Parameters:
  - request (Request): The incoming request object.
  - db (Session, optional): The database session. Defaults to Depends(get_db).
  - current_user (User, optional): The current authenticated user. Defaults to Depends(get_current_active_user).

  Returns:
  - TemplateResponse: The rendered template response for the dashboard page.
  """

  details = product_service.details(db)
  template_vars = {
    "current_user": current_user,
    'details': details,
    'dashboard': 'active',
    'cdashboard': 'active'
  }
  return templates.TemplateResponse("dashboard/index.html", {"request": request, **template_vars})

@router.get("/login")
async def login_page(request: Request):
  """
  Renders the login page and sets the access_token cookie to None.
  Args:
    request (Request): The incoming request object.
  Returns:
    TemplateResponse: The response object containing the rendered login page.
  """
  # Render the login page
  # Set the access_token cookie to None
  
  response = templates.TemplateResponse("session/login.html", {"request": request})
  response.set_cookie(
    key="access_token",
    value=None,
    path='/',
    expires=None,
    httponly=None)

  return response

@router.post("/login")
async def login(*, request: Request, db: Session = Depends(get_db), email: str = Form(...), password: str = Form(...)):
  """
  Authenticate user and generate access token for login.
  Parameters:
  - request: The incoming request object.
  - db: The database session.
  - email: The email of the user.
  - password: The password of the user.
  Returns:
  - A RedirectResponse object with a cookie containing the access token.
  Raises:
  - HTTPException with status code 400 if the email or password is incorrect.
  """
  
  user = services.user_service.authenticate(db, email=email, password=password)
  if not user:
    raise HTTPException(
      status_code=400,
      detail="Incorrect email or password",
    )
  access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token =  create_access_token(data={"user_id": user.id}, expires_delta=access_token_expires)
  
  response = RedirectResponse(url='/', status_code=HTTP_303_SEE_OTHER)
  response.set_cookie(
    key="access_token",
    value=f"Bearer {access_token}",
    path='/',
    expires=access_token_expires,
    httponly=True)

  return response

@router.get("/register")
async def login_page(request: Request):
  """
  Renders the login page and sets the access_token cookie to None.
  Args:
    request (Request): The incoming request object.
  Returns:
    TemplateResponse: The rendered login page with the access_token cookie set to None.
  """
  
  response = templates.TemplateResponse("session/register.html", {"request": request})
  response.set_cookie(
      key="access_token",
      value=None,
      path='/',
      expires=None,
      httponly=None)

  return response

@router.post("/register")
async def register(*, request: Request, db: Session = Depends(get_db), username: str = Form(...), email: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
  """
  Register a new user.
  Args:
    request (Request): The incoming request object.
    db (Session, optional): The database session. Defaults to Depends(get_db).
    username (str): The username of the user. Required.
    email (str): The email of the user. Required.
    password (str): The password of the user. Required.
    confirm_password (str): The confirmation password. Required.
  Raises:
    HTTPException: If a user with the same email already exists or if the passwords do not match.
  Returns:
    RedirectResponse: A redirect response to the login page.
  """
  
  user = services.user_service.get_by_email(db, email=email)
  
  if user:
    raise HTTPException(
      status_code=400,
      detail="The user with this email already exists in the system",
    )
  if password != confirm_password:
    raise HTTPException(
      status_code=400,
      detail="The passwords do not match",
    )

  user_in = UserCreate(username=username, email=email, password=password)
  user = services.user_service.create(db, user_in=user_in)

  response = RedirectResponse(url='/login', status_code=HTTP_303_SEE_OTHER)
  return response

@router.get("/logout")
async def logout(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
  """
  Logout the current user by clearing the access token cookie and redirecting to the login page.

  Parameters:
  - db (Session): The database session.
  - current_user (User): The current authenticated user.

  Returns:
  - RedirectResponse: The redirect response to the login page.
  """

  response = RedirectResponse(url='/login', status_code=HTTP_303_SEE_OTHER)
  response.set_cookie(
      key="access_token",
      value=None,
      path='/',
      expires=None,
      httponly=None)
  return response
