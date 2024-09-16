from src.ai.model_training import train_and_save_model
from src.models import PredictedSale, Product

async def forecasting(file):
  """
  Asynchronously performs forecasting based on the provided file.

  Parameters:
  - file: The file containing data for forecasting.

  Returns:
  - A dictionary with a message indicating the success of the forecasting process.
  """
  await train_and_save_model(file)
  return {"message": "Forecasting completed successfully."}


def forecasting_for_product(slug, db_session):
  """
  Retrieves the forecasted inventory for a given product.
  Args:
    slug (str): The slug of the product.
    db_session: The database session.
  Returns:
    dict: A dictionary containing the forecasted inventory for each month.
  Raises:
    None
  """
  product = db_session.query(Product.id).filter(Product.slug == slug).first()
  
  if not product:
    return {"message": "Product not found."}
  data = db_session.query(PredictedSale.date, PredictedSale.sales).filter(PredictedSale.product_id == product.id).all()
  monts = [ date.strftime("%Y-%m-%d") for date, _ in data ]
  forecasted_inventory = [ sales for _, sales in data ]
  return {"months": monts, "forecasted_inventory": forecasted_inventory}
