from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.services import inventory_forecasting_service
from src.database import get_db
"""
Endpoint for retrieving inventory forecasting data for a specific product.

Parameters:
- slug (str): The slug of the product.

Returns:
- data: The inventory forecasting data for the specified product.

Dependencies:
- db (Session): The database session.

Example:
GET /forecasting/{slug}
"""

router = APIRouter()


@router.get("/forecasting/{slug}")
async def root(
  slug: str = None,
  db: Session = Depends(get_db)
):
  data = inventory_forecasting_service.forecasting_for_product(slug, db)
  return data