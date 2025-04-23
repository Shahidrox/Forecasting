import os
import pandas as pd
import numpy as np
import joblib
import warnings
import matplotlib


from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression

matplotlib.use('Agg')
warnings.filterwarnings("ignore", category=UserWarning)

BASE_PATH = "src/data"
LAPTOP_DATA = os.path.join(BASE_PATH, "Laptopsdata.csv")
CLUSTER_MODEL_PATH = os.path.join(BASE_PATH, "kmeans_model.pkl")
REGRESSION_MODELS_DIR = os.path.join(BASE_PATH, "regression_models")
os.makedirs(REGRESSION_MODELS_DIR, exist_ok=True)

async def get_new_product_forecasting(product):
    new_row = pd.DataFrame([product.dict()])

    # Validate inputs
    if not (0 < product.Battery_Life < 8 and -1 < product.Display_Size < 2 and
            0 < product.Price < 1500 and -1 < product.Weight < 2 and
            0.5 < product.Screen_Resolution < 3 and 0 < product.RAM < 16 and
            10 < product.Processor_Speed < 20 and 200 < product.Storage < 5000):
        return {"success": False, "error": "Invalid product features"}

    # Load models
    if not os.path.exists(CLUSTER_MODEL_PATH):
        train_model()

    kmeans = joblib.load(CLUSTER_MODEL_PATH)
    cluster_id = int(kmeans.predict(new_row)[0])

    reg_path = os.path.join(REGRESSION_MODELS_DIR, f"reg_model_cluster_{cluster_id}.pkl")
    if not os.path.exists(reg_path):
        return {"success": False, "error": "Regression model missing for cluster."}

    reg = joblib.load(reg_path)
    base_prediction = np.round(reg.predict(new_row)[0])

    return {
        "success": True,
        "cluster": cluster_id,
        "predicted_demand": int(base_prediction)
    }

def train_model():
    df = pd.read_csv(LAPTOP_DATA)
    X = df.iloc[:, :8]  # Use DataFrame with column names
    y = df.iloc[:, 8]

    # KMeans clustering
    kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42)
    clusters = kmeans.fit_predict(X)
    df['Cluster'] = clusters
    joblib.dump(kmeans, CLUSTER_MODEL_PATH)

    # Train one regression model per cluster
    for cluster_id in range(3):
        cluster_df = df[df['Cluster'] == cluster_id]
        a_train = cluster_df.iloc[:, :8]  # Use DataFrame
        b_train = cluster_df.iloc[:, 8]

        reg = LinearRegression()
        reg.fit(a_train, b_train)
        joblib.dump(reg, os.path.join(REGRESSION_MODELS_DIR, f"reg_model_cluster_{cluster_id}.pkl"))