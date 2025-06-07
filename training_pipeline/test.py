from fastapi import FastAPI
import mlflow
import numpy as np
import json
import pandas as pd

mlflow.set_tracking_uri("http://127.0.0.1:5000/")

model_uri = "models:/XGBoost/1"
model = mlflow.sklearn.load_model(model_uri)

app = FastAPI()

data = {
  "feature": [
    80, 123456, 10, 8, 500, 400, 60, 40, 50.0, 7.07, 55, 35, 45.0, 7.07,
    9000.0, 5.0, 1000.0, 100.0, 2000, 500, 5000, 1000.0, 200.0, 1500, 500,
    4000, 800.0, 150.0, 1200, 400, 0, 0, 0, 0, 120, 100, 2.0, 1.5, 35, 65,
    50.0, 10.0, 100.0, 0, 1, 0, 0, 1, 0, 0, 0, 1.2, 52.0, 50.0, 45.0, 120,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10, 500, 8, 400, 256, 256, 1, 20,
    3000.0, 400.0, 4000, 2000, 10000.0, 500.0, 11000
  ]
}
# with open('input.json', 'r') as f:
#     data = json.load(f)
df_2 = pd.read_parquet(f'training_pipeline/data/DDoS-Friday-no-metadata.parquet')
df_ddos = df_2[df_2["Label"] != "Benign"]

row = df_ddos.iloc[0]
label = row["Label"]
features_1 = row.drop("Label").astype(float).values
features_1_new = np.array(features_1).reshape(1, -1)
print(features_1_new)

features_2 = np.array(data["feature"]).reshape(1, -1)
print(len(features_2))
prediction = model.predict(features_2)
print(f"Actual label: Benign, Pred label: {'Benign' if prediction[0] == 0 else 'DDOS'}")

prediction_2 = model.predict(features_1_new)
print(f"Actual label: DDos, Pred label: {'Benign' if prediction_2[0] == 0 else 'DDOS'}")
