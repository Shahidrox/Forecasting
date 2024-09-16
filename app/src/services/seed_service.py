from sqlalchemy.sql.functions import current_timestamp
"""
Create seeds for users and products in the database.

This function creates seeds for users and products in the database. It checks if a user or product already exists in the database before creating a new entry.

Parameters:
  None

Returns:
  None
"""

from src.database.session import Session
from src.core.security import get_password_hash
from src.models import User, Product
from src.database import seeds

def create_seed():
  with Session() as db_session:
    # Create users
    for user in seeds.USERS_LIST:
      existing_user = db_session.query(User.id).filter(User.email == user['email']).first()

      if not existing_user:
          u = User(
              email= user['email'],
              hashed_password= get_password_hash(user['password']),
              username= user['username'],
              created_at=current_timestamp(),
              updated_at=current_timestamp()
          )
          db_session.add(u)
    db_session.commit()

    # Create products
    for product_data in seeds.PRODUCT_LIST:
      existingr = db_session.query(Product.id).filter(Product.name == product_data["name"]).first()
      if existingr is None:
          product = Product(
              name=product_data["name"],
              brand=product_data["brand"],
              price=product_data["price"],
              rating=int(product_data["rating"] * 10),
              category=product_data["category"],
              slug=product_data["slug"],
              image=product_data["image"]
          )
          db_session.add(product)
    db_session.commit()
