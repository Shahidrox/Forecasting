import os

from fastapi import APIRouter, Request, Depends, UploadFile, File
from fastapi.responses import FileResponse


"""
This module contains the API endpoints related to user management.
Endpoints:
- GET /users: Retrieves a list of users with pagination support.
- GET /download_sales_data: Downloads a fake sales data file in CSV format.
- POST /train_model: Trains and saves a machine learning model using an uploaded file.
"""
from fastapi.responses import StreamingResponse, JSONResponse

from sqlalchemy.orm import Session

from src.database import get_db
from src.models import User
from src.utils.security import get_current_active_user
from src.services import user_service, customer_behavior_service, new_product_forecasting_service
from src.core.template_setting import templates
from src.utils.set_timezone import convert_to_ist
from src.serializers.new_product_forecasting_serializer import ProductFeatures
router = APIRouter()


@router.get("/users")
async def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    page: int = 1,
    limit: int = 10,
):
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
    template_vars = {
        "current_user": current_user,
        "data": user_list,
        "users": "active",
        "cusers": "active",
    }
    for user in user_list["users"]:
        user.created_at = (
            convert_to_ist(user.created_at).strftime("%Y-%m-%d %H:%M:%S")
            if user.created_at
            else None
        )

    return templates.TemplateResponse(
        "users/index.html", {"request": request, **template_vars}
    )


@router.get("/download_sales_data")
async def dashboard(
    request: Request, current_user: User = Depends(get_current_active_user)
):
    """
    Endpoint for generating and downloading fake sales data as a CSV file.
    Args:
      request (Request): The incoming request object.
      current_user (User, optional): The current authenticated user. Defaults to Depends(get_current_active_user).
    Returns:
      StreamingResponse: The response containing the generated sales data as a CSV file.
    """

    buffer = user_service.genrate_fake_sales_data()
    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=sales_data.csv"},
    )


@router.post("/train_model")
async def dashboard(
    request: Request,
    current_user: User = Depends(get_current_active_user),
    file: UploadFile = File(...),
):
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


@router.get("/customer_behaviors")
async def customer_behaviors(
    request: Request, current_user: User = Depends(get_current_active_user)
):

    template_vars = {
        "current_user": current_user,
        "customer_behaviors": "active",
        "cusers": "active",
    }
    return templates.TemplateResponse(
        "users/customer_behaviors.html", {"request": request, **template_vars}
    )


@router.post("/upload_customer_behaviors")
async def import_csv(
    request: Request,
    current_user: User = Depends(get_current_active_user),
    file: UploadFile = File(...),
):
    response = await customer_behavior_service.import_customer_behaviors(file)

    return JSONResponse(content=response)


@router.get("/download/customer_behavior")
async def download_customer_behaviors(
    request: Request, current_user: User = Depends(get_current_active_user)
):
    csv = os.path.join(os.getcwd(), "src/data/customer_behaviors.csv")
    if not os.path.exists(csv):
        return JSONResponse(
            content={"error": "File not found"},
            status_code=404,
        )
    return FileResponse(
        csv,
        media_type="text/csv",
        filename="customer_behaviors.csv",
    )


@router.get("/new_product_forecasting")
async def new_product_forecasting(
    request: Request, current_user: User = Depends(get_current_active_user)
):
    template_vars = {
        "current_user": current_user,
        "new_product_forecasting": "active",
        "cusers": "active",
        "fields": ProductFeatures.__fields__.keys(),
        "ProductFeatures": ProductFeatures,
    }
    return templates.TemplateResponse(
        "users/new_product_forecasting.html", {"request": request, **template_vars}
    )
    
@router.post("/get_new_product_forecasting")
async def get_new_product_forecasting(
    request: Request,
    product: ProductFeatures,
    current_user: User = Depends(get_current_active_user),
):
    response = await new_product_forecasting_service.get_new_product_forecasting(product)

    return JSONResponse(content={
        **response
    })
