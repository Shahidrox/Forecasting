from sqlalchemy.orm import Session
"""
Retrieves details of all products from the database.

Parameters:
- db (Session): The database session object.

Returns:
- List[Product]: A list of all products in the database.
"""

from src.models import Product

def details(db: Session):
  return db.query(Product).all()
