from fastapi import APIRouter, Request, Depends, UploadFile, File
"""
This module contains the API endpoints related to user management.
Endpoints:
- GET /users: Retrieves a list of users with pagination support.
- GET /download_sales_data: Downloads a fake sales data file in CSV format.
- POST /train_model: Trains and saves a machine learning model using an uploaded file.
"""
from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session

from src.database import get_db
from src.models import User
from src.utils.security import get_current_active_user
from src.services import user_service
from src.core.template_setting import templates
from src.utils.set_timezone import convert_to_ist

router    = APIRouter()


@router.get("/users")
async def dashboard(request: Request, db: Session = Depends(get_db),  current_user: User = Depends(get_current_active_user), page: int = 1,limit: int = 10):
  """
  Dashboard function to handle the request for the user dashboard.
  Args:
    request (Request): The incoming request object.
    db (Session, optional): The database session. Defaults to Depends(get_db).
    current_user (User, optional): The current active user. Defaults to Depends(get_current_active_user).
    page (int, optional): The page number for pagination. Defaults to 1.
    limit (int, optional): The limit of items per page for pagination. Defaults to 10.
  Returns:
    TemplateResponse: The template response for the user dashboard.
  """
  
  user_list = user_service.get_multi(db_session=db, page=page, limit=limit)
  template_vars =  {
        "current_user": current_user,
        'data': user_list,
        'users': 'active',
        'cusers': 'active'
    }
  for user in user_list['users']:
    user.created_at = convert_to_ist(user.created_at).strftime('%Y-%m-%d %H:%M:%S') if user.created_at else None

  return templates.TemplateResponse("users/index.html", {"request": request, **template_vars})

@router.get("/download_sales_data")
async def dashboard(request: Request, current_user: User = Depends(get_current_active_user)):
  """
  Endpoint for generating and downloading fake sales data as a CSV file.
  Args:
    request (Request): The incoming request object.
    current_user (User, optional): The current authenticated user. Defaults to Depends(get_current_active_user).
  Returns:
    StreamingResponse: The response containing the generated sales data as a CSV file.
  """
  
  buffer = user_service.genrate_fake_sales_data()
  return StreamingResponse(buffer, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=sales_data.csv"})

@router.post("/train_model")
async def dashboard(request: Request, current_user: User = Depends(get_current_active_user), file: UploadFile = File(...)):
  """
  Dashboard endpoint for the admin user.
  Parameters:
  - request (Request): The incoming request object.
  - current_user (User): The currently authenticated user.
  - file (UploadFile): The uploaded file containing data for training the model.
  Returns:
  - response: The response from the user_service.train_and_save_model() function.
  """
  response = await user_service.train_and_save_model(file)

  return response
