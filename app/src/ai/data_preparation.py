import pandas as pd
from src.database.session import Session
from src.models import Product
import io

"""
Prepare data for forecasting.
This function prepares data for forecasting by merging sales data with product information.
It takes a file as input and returns a merged DataFrame.
Parameters:
- file: The file containing sales data.
Returns:
- data: The merged DataFrame containing sales data with product information.
Raises:
- FileNotFoundError: If the sales data file is not found.
Example Usage:
file_path = "/path/to/sales_data.csv"
data = await prepare_data_for_forecasting(file_path)
"""

def product_to_dict(product):
  return {
    'id': product.id,
    'name': product.name,
    'brand': product.brand,
    'price': product.price
  }

def products():
  with Session() as db_session:
    return db_session.query(Product).all()

async def prepare_data_for_forecasting(file):
  products_list = [product_to_dict(product) for product in products()]
  # Convert to DataFrame
  products_df = pd.DataFrame(products_list)

  # Load sales data
  sales_data = None
  try:
    # Read the file content
    content = await file.read()
    file_like = io.StringIO(content.decode('utf-8'))

    # Load sales data into DataFrame
    sales_data = pd.read_csv(file_like, parse_dates=['date'])
  except FileNotFoundError:
      raise FileNotFoundError("Sales data file not found. Please check the file path.")
    
  data = sales_data.merge(products_df, left_on='product_id', right_on='id')
  
  return data