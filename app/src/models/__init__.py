from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import String, Boolean, Integer, TIMESTAMP
from sqlalchemy.sql.functions import current_timestamp

"""
This module contains the SQLAlchemy models for the application.
The models define the structure of the database tables and their columns.
Classes:
- User: Represents a user in the application.
- Product: Represents a product in the application.
- ModelInfo: Represents information about a machine learning model.
- PredictedSale: Represents predicted sales data.
Each class corresponds to a table in the database and defines the columns using SQLAlchemy's Column class.
Attributes:
- id: The primary key of the table.
- created_at: The timestamp when the record was created.
- updated_at: The timestamp when the record was last updated.
For more information on SQLAlchemy, refer to the official documentation: https://docs.sqlalchemy.org/
"""

Base = declarative_base()

class User(Base):
  __tablename__         = 'users'

  id                    = Column(Integer, primary_key=True, index=True, autoincrement=True)
  username              = Column(String)
  email                 = Column(String,  nullable=False, index=True)
  hashed_password       = Column(String,  nullable=False)
  is_active             = Column(Boolean, default=True)
  created_at            = Column(TIMESTAMP(timezone=True), server_default=current_timestamp(), nullable=False)
  updated_at            = Column(TIMESTAMP(timezone=True), server_default=current_timestamp(), onupdate=current_timestamp(), nullable=False)

class Product(Base):
  __tablename__         = 'products'
  
  id                    = Column(Integer, primary_key=True, index=True, autoincrement=True)
  name                  = Column(String, nullable=False)
  brand                 = Column(String, nullable=False)
  price                 = Column(Integer, nullable=False)
  rating                = Column(Integer, nullable=False)
  category              = Column(String, nullable=False)
  slug                  = Column(String, nullable=False)
  image                 = Column(String, nullable=False)

class ModelInfo(Base):
  __tablename__         = 'model_info'

  id                    = Column(Integer, primary_key=True, index=True, autoincrement=True)
  model_name            = Column(String, nullable=False)
  model_type            = Column(String, nullable=False)
  model_path            = Column(String, nullable=False)
  created_at            = Column(TIMESTAMP(timezone=True), server_default=current_timestamp(), nullable=False)
  updated_at            = Column(TIMESTAMP(timezone=True), server_default=current_timestamp(), onupdate=current_timestamp(), nullable=False)

class PredictedSale(Base):
  __tablename__         = 'predicted_sales'
  
  id                    = Column(Integer, primary_key=True, index=True, autoincrement=True)
  product_id            = Column(Integer, nullable=False)
  date                  = Column(TIMESTAMP(timezone=True), nullable=False)
  sales                 = Column(Integer, nullable=False)
  created_at            = Column(TIMESTAMP(timezone=True), server_default=current_timestamp(), nullable=False)
  updated_at            = Column(TIMESTAMP(timezone=True), server_default=current_timestamp(), onupdate=current_timestamp(), nullable=False)
