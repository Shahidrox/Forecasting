import random
"""
Generate sample sales data as a pandas DataFrame.
Returns:
  pandas.DataFrame: DataFrame containing the generated sales data.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.database.session import Session
from src.models import Product



def products():
  with Session() as db_session:
    return db_session.query(Product).all()

def generate_csv():
  past_year = datetime.now().year - 4
  start_date = datetime(past_year, 1, 1)
  end_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
  date_range = (end_date - start_date).days

  # Generate random sales data
  np.random.seed(0)  # For reproducibility

  dates = []
  product_ids = []
  sales = []

  # Generate daily data for each product
  for product in products():
    product_id = product.id
    for single_date in (start_date + timedelta(n) for n in range(date_range)):
      dates.append(single_date)
      product_ids.append(product_id)
      sales.append(round(random.uniform(10.0, 500.0), 2))  # Generating random sales numbers
      
  # Create DataFrame
  sales_data = pd.DataFrame({
      'date': dates,
      'product_id': product_ids,
      'sales': sales
  })

  return sales_data
  # # Path to the CSV file
  # csv_file_path = 'src/data/sales_data.csv'

  # # Delete the CSV file if it exists
  # if os.path.exists(csv_file_path):
  #     os.remove(csv_file_path)

  # # Save to CSV
  # sales_data.to_csv(csv_file_path, index=False)
  
  # return csv_file_path
