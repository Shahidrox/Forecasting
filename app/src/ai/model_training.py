import os
import pandas as pd
import pickle
from sqlalchemy import func
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime

from src.ai.data_preparation import prepare_data_for_forecasting
from src.database.session import Session
from src.models import ModelInfo, PredictedSale



def forecast_product_sales(product_id, product_series, periods=90):
  model = ARIMA(product_series, order=(7,0,3))  # Adjust order as needed
  model_fit = model.fit()
  forecast = model_fit.forecast(steps=periods)
  forecast_index = pd.date_range(start=product_series.index[-1] + pd.DateOffset(1), periods=periods, freq='D')
  forecast_series = pd.Series(forecast, index=forecast_index, name='forecast')
  
  # Save model
  today = datetime.now().strftime('%Y-%m-%d')
  model_dir = 'src/data'
  model_path = os.path.join(model_dir, f'arima_model_{product_id}_{today}.pkl')
  
  with open(model_path, 'wb') as file:
    pickle.dump(model_fit, file)
    
  store_model_info('ARIMA', 'Time Series', model_path)

  return forecast_series

# Function to train the model
async def train_model(file):
  data = await prepare_data_for_forecasting(file)
  data.drop(['id'], axis=1, inplace=True)

  # Aggregate sales by date and product
  data_grouped = data.groupby(['date', 'product_id']).agg({'sales': 'sum'}).reset_index()
  
  # Pivot data to get sales for each product
  pivot_data = data_grouped.pivot(index='date', columns='product_id', values='sales').fillna(0)
  
  # Ensure the frequency is set (e.g., daily)
  pivot_data.index = pd.date_range(start=pivot_data.index.min(), end=pivot_data.index.max(), freq='D')
  delete_predictions()
  for product in pivot_data.columns:
    product_series = pivot_data[product]
    store_predictions(product, forecast_product_sales(product, product_series))
    
# Function to train and save the model
async def train_and_save_model(file):
  await train_model(file)

# Function to store model information in the database
def store_model_info(model_name, model_type, model_path):
  with Session() as db_session:
    today = datetime.now().date()
    model_info = db_session.query(ModelInfo).filter(func.date(ModelInfo.created_at) == today)
    if model_info:
      model_info.model_name = model_name
      model_info.model_type = model_type
      model_info.model_path = model_path
    else:
      model_info = ModelInfo(
        model_name=model_name,
        model_type=model_type,
        model_path=model_path
      )
      db_session.add(model_info)
    db_session.commit()

# Function to store predicted sales in the database
def store_predictions(product_id, forecast_series):
  with Session() as db_session:
    # Convert to DataFrame
    forecast_df = forecast_series.reset_index()
    forecast_df.columns = ['date', 'predicted_sales']
    for _, row in forecast_df.iterrows():
      existing_prediction = db_session.query(PredictedSale).filter(PredictedSale.product_id == product_id, PredictedSale.date == row['date']).first()
      if existing_prediction:
        existing_prediction.sales = row['predicted_sales']
      else:
        prediction = PredictedSale(
          product_id=product_id,
          date=row['date'],
          sales=row['predicted_sales']
        )
        db_session.add(prediction)
    db_session.commit()

# Function to delete existing predictions from the database
def delete_predictions():
  with Session() as db_session:
    db_session.query(PredictedSale).delete()
    db_session.commit()
